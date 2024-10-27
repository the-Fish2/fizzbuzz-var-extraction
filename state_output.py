"""
This is the file for the state output function, which is used to print out the variables in the local scope of a function. This file is imported as text into every unit tests so that the test can run state_output calls.
"""

from typing import Any, Dict, List


def state_output(local_vars: Dict[str, Any], codeLine: str, loc: int) -> None:

    # This is a helper function for determining if a variable is a user-defined variable.
    def testName(name: str, value: Any) -> bool:
        exclude_sections = [
            "In",
            "Out",
            "requests",
            "json",
            "os",
            "subprocess",
            "tempfile",
            "shutil",
            "re",
            "ast",
        ]
        if (
            not name.startswith("_")
            and name not in dir(__builtins__)
            and not callable(value)
            and not isinstance(value, type)
            and name not in exclude_sections
        ):
            return True
        return False

    # Here, obj is any object that is defined with a class. This is basically a way of outputting any such user-defined object. Max-depth refers to if an object is defined with a reference to another class, and so forth, for determining the number of nested classes that will be iterated through before stopping.
    def custom_repr(obj: Any, depth: int = 0, max_depth: int = 10) -> str:
        if depth > max_depth:
            return ""

        if hasattr(obj, "__class__") and not isinstance(
            obj, (str, int, float, bool, list, dict, tuple)
        ):
            attrs: List[str] = []
            for k in dir(obj.__class__):
                if testName(k, getattr(obj, k)):
                    v = getattr(obj, k)
                    v_repr = custom_repr(v, depth + 1, max_depth)
                    attrs.append(f"{k}: {v_repr}")
            return f"{obj.__class__.__name__}" + "{" + ", ".join(attrs) + "}"

        return repr(obj)

    all_vars = local_vars

    user_defined_vars = {
        name: custom_repr(value)
        for name, value in all_vars.items()
        if testName(name, value)
    }

    # Printing variable extraction!
    print(codeLine, "Line number: ", loc)

    for var_name, var_value in user_defined_vars.items():
        print(f"{var_name}: {var_value}")

    print()
