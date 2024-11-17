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

FILEPATH = 'my_folder'
#FILEPATH = os.path.dirname(os.path.abspath(__file__))

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
        with open(f"{FILEPATH}/state_output.py", "r") as f:
            self.state_output_code = textwrap.dedent(f.read())


    def find_python_files(self, current_dir: Path = None) -> List[Path]:
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
            elif item.is_file() and item.suffix == '.py':
                python_files.append(item)
                
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
        import_statement = f"from my_folder.state_output import state_output\n"
        
        final_source = import_statement + "\n\n" + new_source
        #self.state_output_code + "\n\n" + new_source
        
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
        python_files = self.find_python_files(self.root_dir)
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