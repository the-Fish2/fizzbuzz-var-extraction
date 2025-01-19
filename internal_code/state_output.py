"""
this is the file for the state output function, which is used to print out the variables in the local scope of a function. this file is imported as text into every unit tests so that the test can run state_output calls.
"""

from typing import Any, Dict, List
import os
import json
import inspect


def state_output(
    local_vars: Dict[str, Any], code_line: str, loc: int, filepath: str
) -> None:

    # this is a helper function for determining if a variable is a user-defined variable.
    def test_name(name: str, value: Any) -> bool:
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
            # removing __name__, __doc__, __package__, __loader__, __spec__, __file__, __cached__, and __builtins__
            not name.startswith("__")
            and name not in dir(__builtins__)
            and not callable(value)
            and name not in exclude_sections
        ):
            return True
        return False

    def custom_repr(obj: Any, depth: int = 0, max_depth: int = 2) -> str:
        """
        here, obj is any object that is defined with a class. this is basically a way of outputting any such user-defined object. max-depth refers to if an object is defined with a reference to another class, and so forth, for determining the number of nested classes that will be iterated through before stopping.
        """
        if depth > max_depth:
            return ""

        if hasattr(obj, "__class__") and not isinstance(
            obj, (str, int, float, bool, list, dict, tuple)
        ):
            attrs: List[str] = []
            for k in dir(obj.__class__):
                if test_name(k, getattr(obj, k)):
                    v = getattr(obj, k)
                    v_repr = custom_repr(v, depth + 1, max_depth)
                    attrs.append(f"{k}: {v_repr}")
            return f"{obj.__class__.__name__}" + "{" + ", ".join(attrs) + "}"

        return repr(obj)

    all_vars = local_vars

    user_defined_vars = {
        name: custom_repr(value)
        for name, value in all_vars.items()
        if test_name(name, value)
    }

    output_entry = {
        "line_number": loc,
        "code_line": code_line,
        "variables": user_defined_vars,
        "file": filepath,
    }

    json_output_entry = json.dumps(output_entry)

    # print(json_output_entry)

    # SPLIT FOR NEW FUNCTION VARIABLES

     # Get the current frame and its caller
    current_frame = inspect.currentframe()
    if current_frame is None:
        return
    
    caller_frame = current_frame.f_back
    if caller_frame is None:
        return

    # Get the function name if we're inside a function
    function_name = None
    if code_line.strip().startswith('def '):
        # This is a function definition
        function_name = code_line.split('def ')[1].split('(')[0].strip()
    else:
        # We're inside a function
        function_code = caller_frame.f_code
        if function_code.co_name != '<module>':
            function_name = function_code.co_name

    # Get all variables
    all_vars = local_vars.copy()
    
    # Separate function variables from global variables
    function_vars = {}
    global_vars = {}
    
    if function_name:
        # Get the globals that existed before the function call
        global_vars = {
            name: custom_repr(value)
            for name, value in caller_frame.f_globals.items()
            if test_name(name, value)
        }
        
        # Get the local variables specific to this function
        function_vars = {
            name: custom_repr(value)
            for name, value in all_vars.items()
            if test_name(name, value) and name not in global_vars
        }
    else:
        # If we're not in a function, all variables are considered global
        global_vars = {
            name: custom_repr(value)
            for name, value in all_vars.items()
            if test_name(name, value)
        }

    # Create the output entry
    output_entry = {
        "line_number": loc,
        "code_line": code_line,
        "variables": global_vars,  # This now contains only global variables
        "file": filepath,
    }

    # Add function-specific variables if we're in a function
    if function_name:
        output_entry[f"{function_name}_variables"] = function_vars

    json_output_entry = json.dumps(output_entry)
    print(json_output_entry)

    # Clean up the frame references
    del current_frame
    del caller_frame
