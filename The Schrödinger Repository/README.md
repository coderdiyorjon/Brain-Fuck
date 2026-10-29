```markdown
# The Schrödinger Repository 📦🐈

A chaotic mini-project that randomly destroys its own rules while trying to remain executable. 

This program takes a tiny Python codebase, introduces random structural mutations (changing operators, conditions, and math), and uses property-based testing to determine if the mutated program still behaves identically to the original. 

The goal isn't to build something useful. It's to build something that makes you question whether your own testing strategy is actually correct.

## 🧠 The Concept

You cannot simply compare outputs from one test case. Two programs can produce identical outputs for a thousand inputs and still differ on the thousand-and-first. 
This project uses **AST (Abstract Syntax Tree)** for safe code mutation and **Hypothesis** to relentlessly generate edge cases until it finds the smallest counterexample that breaks the illusion of equivalence.

### Core Constraints (Achieved):
- No LLMs or external AI APIs.
- No `eval()` or `exec()`.
- Generates random mutations on the syntax tree.
- Detects behavioral differences using automatically generated inputs.
- Minimizes a failing input until it finds the smallest counterexample (Shrinking).
- Keeps a history of mutations to reproduce every failure.

## 📂 Project Structure

- **`target.py`** — The "Victim". A simple, pure Python module that calculates taxes.
- **`ast_manager.py`** — The Chaos Engine. Parses `target.py` into an AST, injects random logical bugs (e.g., swapping `<` to `<=`, `//` to `*`), and safely writes it to `mutated_target.py`.
- **`test_observer.py`** — The Observer. Uses `pytest` and `Hypothesis` to compare the original and mutated code using hundreds of random inputs.
- **`final_boss.py`** — The Orchestrator. Runs the entire pipeline in a loop until it successfully finds a mutation that breaks the logic, then prints a clean post-mortem report.

## 🚀 Installation & Setup

1. **Clone the repository and enter the directory:**
   ```bash
   cd "The Schrödinger Repository"

```

2. **Create a virtual environment:**
```bash
python -m venv venv
# On Windows:
venv\Scripts\activate
# On Mac/Linux:
source venv/bin/activate

```


3. **Install the required testing libraries:**
```bash
pip install -r requirements.txt

```



## 🎮 How to Run

### Method 1: The Final Boss (Automated Loop)

The easiest way to see the chaos in action. It loops the mutation engine and testing suite until a bug is successfully injected and caught by Hypothesis.

```bash
python final_boss.py

```

### Method 2: Manual Step-by-Step

If you want to see the underlying process of Hypothesis shrinking the counterexample:

```bash
pytest test_observer.py -s -v

```

## 🔬 Example Output (The Final Boss)

```text
Attempt #1: Trying to mutate code...

-------------------------------------------------------
TEST RUN FAILED
-------------------------------------------------------
-----------------------------------------------

MUTATION GENERATE PROCESS STARTED
-----------------------------------------------

Change: COMPARISION OPERATOR HAS CHANGED: Lt -> LtE
-----------------------------------------------

F
================================== FAILURES ===================================
__________________________ test_schrodinger_behavior __________________________

mutated_module = <module 'mutated_target' from 'D:\\\\Projects\\\\Brain Fuck\\\\The Schr\xf6dinger Repository\\\\mutated_target.py'>

    @given(
>       price=st.integers(min_value=-100, max_value=10000),
                   ^^^^^^^^^^^^^^^^^
        tax_rate=st.integers(min_value=-20, max_value=200)
    )

test_observer.py:46: 
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _

mutated_module = <module 'mutated_target' from 'D:\\\\Projects\\\\Brain Fuck\\\\The Schr\xf6dinger Repository\\\\mutated_target.py'>
price = 1, tax_rate = 0

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
>       assert original_result == mutated_result, (
            f"\n ERROR FOUND!\n"
            f"Original result: {original_result}\n"
            f"Mutated result: {mutated_result}\n"
        )
E       AssertionError: 
E          ERROR FOUND!
E         Original result: 1
E         Mutated result: 0
E         
E       assert 1 == 0
E       Failing test case: test_schrodinger_behavior(
E           mutated_module=<module 'mutated_target' from 'D:\\\\Projects\\\\Brain Fuck\\\\The Schr\xf6dinger Repository\\\\mutated_target.py'>,
E           price=1,
E           tax_rate=0,
E       )

test_observer.py:62: AssertionError
=========================== short test summary info ===========================
FAILED test_observer.py::test_schrodinger_behavior - AssertionError: 
1 failed in 0.28s



The test run failed, but this does not necessarily mean a mutation was detected.

Chaos engine stopped after 1 attempt(s).

```

## 🛠 Tech Stack

* **Python 3.11+** (Built-in `ast` module)
* **Pytest** (Test execution)
* **Hypothesis** (Property-based testing & shrinking)