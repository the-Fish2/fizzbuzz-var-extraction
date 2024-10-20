import ast
import textwrap
import inspect

def has_body(node):
    return hasattr(node, 'body')

def is_statement(node):
    return isinstance(node, ast.stmt)

def gen_output(b):
  line_number = getattr(b, 'lineno', 'No line number')
  inject_func = ast.parse(f"state_output(locals(), \"{b}\", {line_number})")
  return inject_func

def recursive_injection(callstack):
    body2 = []

    for b in callstack.body:
        if has_body(b):
            recursive_injection(b)
            
        body2.append(gen_output(b))
        body2.append(b)

    callstack.body = body2
    
    if hasattr(callstack, 'orelse'):
        orelse2 = []
        
        for b in callstack.orelse:
            if has_body(b):
                recursive_injection(b)

            orelse2.append(gen_output(b))
            orelse2.append(b)

        callstack.orelse = orelse2

    return callstack

def function_injection(unit_test_method):
    string_test = inspect.getsource(unit_test_method)
    string_test = textwrap.dedent(string_test)
    
    tree = ast.parse(string_test)
    tr2 = recursive_injection(tree)
    tree = ast.unparse(tr2)
    
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
    
    # state_output_code = textwrap.dedent(""" 
    # def state_output(local_vars, codeLine, loc): 
    #     print("Counter") 
    # """)

    tree = state_output_code + "\n" + tree
    return tree