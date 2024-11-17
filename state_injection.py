# """
# This is the file for injecting state output calls into a piece of code using the AST. 
# """

# import ast
# import textwrap
# import inspect
# from typing import List, Callable, Union, Sequence

# # ASTNode = Union[ast.stmt, ast.AST, ast.Module, ast.Expr]

# # Helper functions: checking for ast.stmt types, and if a node has a body
# def has_body(node: ast.AST) -> bool:
#     return hasattr(node, "body")


# def is_statement(node: ast.AST) -> bool:
#     return isinstance(node, ast.stmt)


# # Returning the state output function call and also the line number of the call
# def gen_output(node: ast.AST) -> ast.Module:
#     line_number = getattr(node, "lineno", "No line number")
#     inject_func = ast.parse(f'state_output(locals(), "{node}", {line_number})')
#     return inject_func


# # Checks for if b has a body, and if os, continues recursion
# # Also appends the state output call to the end of every section with a body
# def add_to_ast(
#     node: Union[ast.AST, ast.Module], body2: List[ast.AST]
# ) -> List[ast.stmt]:
#     if has_body(node):
#         recursive_injection(node)

#     body2.append(gen_output(node))
#     body2.append(node)

#     return body2


# # The two main types that I need to recurse through, from the python ast documentation, is .body and .orelse
# # This handles both the .body and the .orelse separately. It is slightly asymmetric because an .orelse can occur in addition to a body, and an orelse has it's own body inside it, so I need to go through the orelse layer for my recursive call to the function
# def recursive_injection(callstack: ast.Module) -> ast.AST:
#     body2: Sequence[ast.AST] = []
#     if hasattr(callstack, "body"):
#         for b in callstack.body:
#             body2 = add_to_ast(b, body2)
#         callstack.body = body2

#     if hasattr(callstack, "orelse"):
#         orelse2 = []
#         for b in callstack.orelse:
#             body2 = add_to_ast(b, orelse2)
#         callstack.orelse = orelse2

#     return callstack


# # This is inserting the state output calls and combining the previous methods
# def function_injection(unit_test_method: Callable) -> str:
#     string_test = inspect.getsource(unit_test_method)
#     string_test = textwrap.dedent(string_test)

#     # Directly inserting state output calls
#     tree = ast.parse(string_test)

#     print(tree)
#     #tree = recursive_injection(tree)
#     tree = ast.unparse(tree)

#     # Necessary state output context for the function to run.
#     # with open("state_output.py", "r") as f:
#     #     state_output_code = textwrap.dedent(f.read())

#     # # Prepending the necessary context to each test case that is being run.
#     # tree = state_output_code + "\n" + tree
#     return tree
