import ast
import inspect
import os
import sys
import textwrap
from typing import List, Set, Callable, Optional
from importlib import util, import_module
from pathlib import Path
import subprocess

class CodeInjector:
    """
    A class that handles module-wide code injection for state output tracking.
    """
    def __init__(self, root_dir: str, exclude_dirs: Optional[List[str]] = None):
        self.root_dir = Path(root_dir)
        self.exclude_dirs = set(exclude_dirs or [])
        self.exclude_dirs.add('__pycache__')
        self.processed_files: Set[str] = set()
        
        # Load state output code
        with open("state_output.py", "r") as f:
            self.state_output_code = textwrap.dedent(f.read())

    def find_python_files(self) -> List[Path]:
        """Find all Python files in the directory tree."""
        python_files = []
        for root, dirs, files in os.walk(self.root_dir):
            # Remove excluded directories
            dirs[:] = [d for d in dirs if d not in self.exclude_dirs]
            
            for file in files:
                if file.endswith('.py'):
                    file_path = Path(root) / file
                    python_files.append(file_path)
        return python_files

    def process_module(self, module_path: Path) -> None:
        """Process a single Python module file."""
        if str(module_path) in self.processed_files:
            return

        # Read the source code
        with open(module_path, 'r') as f:
            source = f.read()

        # Parse and modify the AST
        tree = ast.parse(source)
        modified_tree = self.recursive_injection(tree, filepath=module_path)
        
        # Generate new source code
        new_source = ast.unparse(modified_tree)
        
        # Add state output code
        final_source = self.state_output_code + "\n\n" + new_source
        
        # Create backup of original file
        backup_path = module_path.with_suffix('.py.bak')
        if not backup_path.exists():
            module_path.rename(backup_path)
        
        # Write modified code
        with open(module_path, 'w') as f:
            f.write(final_source)
        
        self.processed_files.add(str(module_path))

    def recursive_injection(self, node: ast.AST, filepath: Path) -> ast.AST:
        """Recursively inject state output calls after each statement."""
        if isinstance(node, (ast.FunctionDef, ast.Module, ast.If, ast.For, ast.While)):
               # Create new function body with state output calls
            new_body = []
            for stmt in node.body:

                # Create state output call
                state_output_call = ast.Expr(
                    value=ast.Call(
                        func=ast.Name(id='state_output', ctx=ast.Load()),
                        args=[
                            ast.Name(id='locals()', ctx=ast.Load()),
                            ast.Constant(value=ast.unparse(stmt)),
                            ast.Constant(value=stmt.lineno),
                            ast.Constant(value=filepath.stem)
                        ],
                        keywords=[]
                    )
                )
                new_body.append(state_output_call)
                new_body.append(stmt)
                
            
            node.body = new_body

        # Recursively process all child nodes
        for child in ast.iter_child_nodes(node):
            self.recursive_injection(child, filepath)
            
        return node

    def process_all_files(self) -> None:
        """Process all Python files in the module."""
        python_files = self.find_python_files()
        for file_path in python_files:
            self.process_module(file_path)

    def restore_backups(self) -> None:
        """Restore all backed up Python files."""
        for processed_file in self.processed_files:
            path = Path(processed_file)
            backup_path = path.with_suffix('.py.bak')
            if backup_path.exists():
                if path.exists():
                    path.unlink()
                backup_path.rename(path)

def inject_codebase(root_dir: str, exclude_dirs: Optional[List[str]] = None) -> CodeInjector:
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
        print("Usage: python code_injector.py <root_directory> [exclude_dir1,exclude_dir2,...]")
        sys.exit(1)
        
    root_dir = sys.argv[1]
    exclude_dirs = sys.argv[2].split(',') if len(sys.argv) > 2 else None
    
    injector = inject_codebase(root_dir, exclude_dirs)
    print(f"Successfully processed files: {len(injector.processed_files)}")

    try:
        result = subprocess.run(["python", "run_tests.py"], check=True, capture_output=True, text=True)
        print("Test results:\n", result.stdout)
    except subprocess.CalledProcessError as e:
        print("An error occurred while running tests:\n", e.stderr)

    input(" :) ")

    injector.restore_backups()