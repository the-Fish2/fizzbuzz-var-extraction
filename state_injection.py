import ast
import textwrap
import inspect

#Helper functions: checking for ast.stmt types, and if a node has a body
def has_body(node):
    return hasattr(node, 'body')

def is_statement(node):
    return isinstance(node, ast.stmt)

#Returning the state output function call and also the line number of the call
def gen_output(b):
  line_number = getattr(b, 'lineno', 'No line number')
  inject_func = ast.parse(f"state_output(locals(), \"{b}\", {line_number})")
  return inject_func

#Checks for if b has a body, and if os, continues recursion
# Also appends the state output call to the end of every section with a body
def add_to_ast(b, body2):
    if has_body(b):
        recursive_injection(b)
    
    body2.append(gen_output(b))
    body2.append(b)
    
    return body2

#The two main types that I need to recurse through, from the python ast documentation, is .body and .orelse
# This handles both the .body and the .orelse separately. It is slightly asymmetric because an .orelse can occur in addition to a body, and an orelse has it's own body inside it, so I need to go through the orelse layer for my recursive call to the function
def recursive_injection(callstack):
    body2 = []
    for b in callstack.body:
        body2 = add_to_ast(b, body2)
    callstack.body = body2
    
    if hasattr(callstack, 'orelse'):
        orelse2 = []
        for b in callstack.orelse:
            body2 = add_to_ast(b, orelse2)
        callstack.orelse = orelse2

    return callstack

# This is inserting the state output calls and combining the previous methods
def function_injection(unit_test_method):
    string_test = inspect.getsource(unit_test_method)
    string_test = textwrap.dedent(string_test)
    
    #Directly inserting state output calls
    tree = ast.parse(string_test)
    tr2 = recursive_injection(tree)
    tree = ast.unparse(tr2)
    
    #Necessary state output context for the function to run. 
    state_output_code = textwrap.dedent("""    
                                                                                            
        def state_output(local_vars, codeLine, loc):
                                        
            def testName(name, value=None):
                exclude_sections = ['In', 'Out', 'requests', 'json', 'os', 'subprocess', 'tempfile', 'shutil', 're', 'ast']
                if (not name.startswith('_') and name not in dir(__builtins__) and not callable(value) and not isinstance(value, type) and name not in exclude_sections):
                    return True
                return False
            
            def custom_repr(obj, depth=0, max_depth=10):
                if depth > max_depth:
                    return ""

                if hasattr(obj, '__class__') and not isinstance(obj, (str, int, float, bool, list, dict, tuple)):
                    attrs = []
                    for k in dir(obj.__class__):
                        if testName(k, getattr(obj, k)):
                            v = getattr(obj, k)
                            v_repr = custom_repr(v, depth + 1, max_depth)
                            attrs.append(f"{k}: {v_repr}")
                    return f"{obj.__class__.__name__}" + '{' + ', '.join(attrs) + '}'

                return repr(obj)

            exclude_sections = ['In', 'Out', 'requests', 'json', 'os', 'subprocess', 'tempfile', 'shutil', 're', 'ast']
    
            all_vars = local_vars
            
            user_defined_vars = {
                name: custom_repr(value) for name, value in all_vars.items()
                if testName(name, value)
            }

            print(codeLine, "Line number: ", loc)

            for var_name, var_value in user_defined_vars.items():
                print(f"{var_name}: {var_value}")
            
            print()
                                        
        """)

    #Prepending the necessary context to each test case that is being run. 
    tree = state_output_code + "\n" + tree
    return tree