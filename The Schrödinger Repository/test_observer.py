import pytest
import importlib
from hypothesis import given, settings, strategies as st
from typing import Any
from pathlib import Path
from types import ModuleType

# Modules that we wrote
import target
import ast_manager

@pytest.fixture(scope="module")
def mutated_module() -> Any:
    """
    Runs one time before tests running:
    1. creates mutated_target.py after mutating target.py
    2. Loads it into memory and gives it to tests 
    """
    script_location: Path = Path(__file__).absolute().parent
    file_location: Path = script_location / "target.py"
    new_file_location: Path = script_location / "mutated_target.py"
    
    logs: list[str] = ast_manager.mutate_file(file_location, new_file_location)

    print("-----------------------------------------------\n")
    print("MUTATION GENERATE PROCESS STARTED")
    print("-----------------------------------------------\n")

    if logs:
        for log in logs:
            print(f"Change: {log}")
    else:
        print("This time nothing happened")

    print("-----------------------------------------------\n")
    
    # Import mutated file
    import mutated_target # type ignore
    importlib.reload(mutated_target)
    
    return mutated_target
    
    
# Hypothesis creates variables automatically
@given(
    price=st.integers(min_value=-100, max_value=10000),
    tax_rate=st.integers(min_value=-20, max_value=200)
)
@settings(max_examples=500) # stress testing using 500 random numbers
def test_schrodinger_behavior(mutated_module: ModuleType, price: int, tax_rate: int) -> None:
    """
    Checks whether both codes return same results or not
    """
    # Result of clean, reliable, original code
    original_result: int = target.calc_total(price, tax_rate)
    
    # Result of mutated code
    mutated_result: int = mutated_module.calc_total(price, tax_rate)
    
    # Comparision. If there is a diff, Hypothesis shrinks and finds
    # the smallest input data with error
    assert original_result == mutated_result, (
        f"\n ERROR FOUND!\n"
        f"Original result: {original_result}\n"
        f"Mutated result: {mutated_result}\n"
    )
    