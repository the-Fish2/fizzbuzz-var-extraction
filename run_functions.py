import ast
from state_injection import recursive_injection

# Currently still working on this code for pulling intermediary function states
# Does not need to be reviewed!


def find_function_definitions(tree):
    func_defs = {}
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            func_defs[node.name] = node

        if isinstance(node, ast.Call):
            func_defs[node.func.id] = node.func
            print(node.func.id)
    return func_defs


def inject_in_functions(tree, func_defs):
    """
    Injects `state_output` calls into function definitions referenced by `ast.Call` nodes.
    If a function is called within another function, inject state_output into both.
    """

    class FunctionCallInjector(ast.NodeTransformer):
        def visit_Call(self, node):
            # Get the function name being called
            if isinstance(node.func, ast.Name):
                func_name = node.func.id
                if func_name in func_defs:
                    # Inject into the called function (callee)
                    called_func = func_defs[func_name]
                    func_defs[func_name] = recursive_injection(
                        called_func
                    )  # Modify callee

                    # Optionally, pass the function itself for further injection
                    node = ast.Call(
                        func=node.func,
                        args=node.args
                        + [
                            ast.Name(id=func_name, ctx=ast.Load())
                        ],  # Pass the function name
                        keywords=node.keywords,
                    )
            return self.generic_visit(node)

    # Traverse the tree and inject state_output where necessary
    injector = FunctionCallInjector()
    modified_tree = injector.visit(tree)

    return modified_tree
