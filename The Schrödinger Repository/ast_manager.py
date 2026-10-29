import ast
import random
from typing import Optional
from pathlib import Path

class ChaosMutator(ast.NodeTransformer):
    """
    Creates random mutations to nodes which are met while getting around AST tree
    """
    def __init__(self, seed: Optional[int]=None) -> None:
        self.mutations_log: list[str] = []
        if seed is not None:
            random.seed(seed)
    
    
    def visit_BinOp(self, node: ast.BinOp) -> ast.BinOp:
        # In order to check bottom sides of tree
        self.generic_visit(node)
        
        # Swapping math opers by 20% probability
        if random.random() < 0.20:
            old_op: str = type(node.op).__name__
            
            if isinstance(node.op, ast.Add):
                node.op = ast.Sub()
            elif isinstance(node.op, ast.Sub):
                node.op = ast.Add()
            elif isinstance(node.op, ast.Mult):
                node.op = ast.FloorDiv()
            elif isinstance(node.op, ast.FloorDiv):
                node.op = ast.Mult()
            
            new_op: str = type(node.op).__name__
            if old_op != new_op:
                self.mutations_log.append(f"MATH OPER HAS CHANGED: {old_op} -> {new_op}")
        
        return node
    
    
    def visit_Compare(self, node: ast.Compare) -> ast.Compare:
        self.generic_visit(node)
        
        # Swapping comparition opers by 20% probability
        if random.random() < 0.2 and len(node.ops) > 0:
            old_op: str = type(node.ops[0]).__name__
            
            if isinstance(node.ops[0], ast.Lt):
                node.ops[0] = ast.LtE()
            elif isinstance(node.ops[0], ast.LtE):
                node.ops[0] = ast.Lt()
            
            new_op: str = type(node.ops[0]).__name__
            if old_op != new_op:
                self.mutations_log.append(f"COMPARISION OPERATOR HAS CHANGED: {old_op} -> {new_op}")
        
        return node
        

def mutate_file(source_path: Path, dest_path: Path, seed: None | int=None) -> list[str]:
    """Reads code, converts into a tree, makes mutations and saves to a new file"""
    
    # Reading source code (file_location -> source_path ga o'zgardi)
    with open(source_path, "r", encoding='utf-8') as f:
        source_code: str = f.read()
    
    # Making AST tree from string code
    tree: ast.Module = ast.parse(source_code)

    # Applying mutation
    mutator: ChaosMutator = ChaosMutator(seed)
    mutated_tree = mutator.visit(tree)
    
    # Must fix row numbers if there is a change in AST
    ast.fix_missing_locations(mutated_tree)
    
    # Creating Python code back again using mutated tree
    mutated_code: str = ast.unparse(mutated_tree)
    
    # Saving new mutated-file (new_file_location -> dest_path ga o'zgardi)
    with open(dest_path, 'w', encoding='utf-8') as f:
        f.write(mutated_code)

    return mutator.mutations_log

if __name__ == "__main__":
    script_location: Path = Path(__file__).absolute().parent
    file_location: Path = script_location / "target.py"    
    new_file_location: Path = script_location / "mutated_target.py"
    
    logs: list[str] = mutate_file(file_location, new_file_location)
    print("History of input mutations")
    for log in logs:
        print("-", log)
    if not logs:
        print("Any of mutations proceed successfully")