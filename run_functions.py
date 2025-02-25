import ast
import inspect
import os
import sys
import textwrap
from typing import List, Set, Callable, Optional
from importlib import util, import_module
from pathlib import Path
import subprocess
import os

FILEPATH = "internal_code"
# FILEPATH = os.path.dirname(os.path.abspath(__file__))


class CodeInjector:
    """
    A class that handles module-wide code injection for state output tracking.
    """

    def __init__(self, root_dir: str, exclude_dirs: Optional[List[str]] = None):
        self.root_dir = Path(root_dir)
        self.exclude_dirs = set(exclude_dirs or [])
        self.exclude_dirs.add("__pycache__")
        self.processed_files: Set[str] = set()

        # Load state output code
        with open(f"{FILEPATH}/state_output.py", "r") as f:
            self.state_output_code = textwrap.dedent(f.read())

    def find_python_files(self, current_dir: Path) -> List[Path]:
        """Find all Python files in the directory tree recursively.

        Args:
            current_dir (Path, optional): Current directory being processed.
                Defaults to None (uses root_dir on first call).

        Returns:
            List[Path]: List of paths to Python files found
        """

        python_files = []

        # Process all files in current directory
        for item in current_dir.iterdir():
            if item.is_dir() and item.name not in self.exclude_dirs:
                next_files = self.find_python_files(item)
                python_files.extend(next_files)
            elif item.is_file() and item.suffix == ".py":
                python_files.append(item)

        return python_files

    def process_module(self, module_path: Path) -> None:
        """Process a single Python module file."""
        if str(module_path) in self.processed_files:
            return

        # Read the source code
        with open(module_path, "r") as f:
            source = f.read()

        # Parse and modify the AST
        tree = ast.parse(source)
        modified_tree = self.recursive_injection(tree, filepath=module_path)

        # Generate new source code
        new_source = ast.unparse(modified_tree)

        # Add state output code
        import_statement = f"from internal_code.state_output import state_output\n"

        final_source = import_statement + "\n\n" + new_source
        # self.state_output_code + "\n\n" + new_source

        # Create backup of original file
        backup_path = module_path.with_suffix(".py.bak")
        if not backup_path.exists():
            module_path.rename(backup_path)

        # Write modified code
        with open(module_path, "w") as f:
            f.write(final_source)

        self.processed_files.add(str(module_path))

    def recursive_injection(self, node: ast.AST, filepath: Path) -> ast.AST:
        """Recursively inject state output calls after each statement."""
        if isinstance(node, (ast.FunctionDef, ast.Module, ast.If, ast.For, ast.While)):
            # Create new function body with state output calls
            new_body = []
            prev_stmt = ""
            for stmt in node.body:
                if prev_stmt != "":
                    prev_stmt = ast.unparse(prev_stmt)
                # Create state output call
                state_output_call = ast.Expr(
                    value=ast.Call(
                        func=ast.Name(id="state_output", ctx=ast.Load()),
                        args=[
                            ast.Name(id="locals()", ctx=ast.Load()),
                            ast.Constant(
                                value=prev_stmt
                            ),  # changing the code line up one
                            ast.Constant(value=stmt.lineno),
                            ast.Constant(value=filepath.stem),
                        ],
                        keywords=[],
                    )
                )
                prev_stmt = stmt  # trying out this change instead for alignment up.

                new_body.append(
                    state_output_call
                )  # trying out this change to see if aligns better to llm output? if not can change the llm prompting but this seems better. issue -> return functions for example do not have state output call at the end. or how about end of if block. changing with prev_statmt instead

                new_body.append(stmt)

            node.body = new_body

        # Recursively process all child nodes
        for child in ast.iter_child_nodes(node):
            self.recursive_injection(child, filepath)

        return node

    def process_all_files(self) -> None:
        """Process all Python files in the module."""
        python_files = self.find_python_files(self.root_dir)
        for file_path in python_files:
            self.process_module(file_path)

    def restore_backups(self) -> None:
        """Restore all backed up Python files."""
        for processed_file in self.processed_files:
            path = Path(processed_file)
            backup_path = path.with_suffix(".py.bak")
            if backup_path.exists():
                if path.exists():
                    path.unlink()
                backup_path.rename(path)


def inject_codebase(
    root_dir: str, exclude_dirs: Optional[List[str]] = None
) -> CodeInjector:
    """
    Main function to inject state output tracking into an entire codebase.

    Args:
        root_dir: Root directory of the codebase
        exclude_dirs: List of directory names to exclude from processing

    Returns:
        CodeInjector instance that can be used to restore backups if needed
    """
    injector = CodeInjector(root_dir, exclude_dirs)
    injector.process_all_files()
    return injector


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(
            "Usage: python run_functions.py <root_directory> [exclude_dir1,exclude_dir2,...]"
        )
        sys.exit(1)

    root_dir = sys.argv[1]
    remove_arg = True if len(sys.argv) > 2 and sys.argv[2] == "remove" else False
    skip_tests = True if len(sys.argv) > 2 and sys.argv[2] == "skip_tests" else False

    if len(sys.argv) > 3 and skip_tests:
        exclude_dirs = sys.argv[4].split(",")
    else:
        if len(sys.argv) > 2 and not remove_arg:
            exclude_dirs = sys.argv[2].split(",")
        else:
            exclude_dirs = None

    if remove_arg:
        injector = CodeInjector(root_dir, exclude_dirs)
        injector.processed_files = injector.find_python_files(Path(root_dir))
        injector.restore_backups()
    else:

        if not skip_tests:
            injector = inject_codebase(root_dir, exclude_dirs)
            print(f"Successfully processed files: {len(injector.processed_files)}")

        try:
            result = subprocess.run(
                ["python", "run_tests.py", root_dir], check=True, text=True
            )
            print("Test results:\n", result.stdout)
        except subprocess.CalledProcessError as e:
            print("An error occurred while running tests:\n", e.stderr)

        input(" :) ")

        injector.restore_backups()
