
import subprocess
import sys
import time


def run_chaos_engine(max_attempts: int | None = None) -> None:
    print("[FINAL BOSS] MUTATION PROCESS IS STARTING...")

    attempts = 0

    while max_attempts is None or attempts < max_attempts:
        attempts += 1

        print(f"\nAttempt #{attempts}: Trying to mutate code...")

        try:
            result = subprocess.run(
                [
                    sys.executable,
                    "-m",
                    "pytest",
                    "test_observer.py",
                    "-s",
                    "-q",
                ],
                capture_output=True,
                text=True,
                timeout=120,
            )
        except subprocess.TimeoutExpired:
            print("Test execution timed out.")
            continue
        except OSError as exc:
            print(f"Could not start pytest: {exc}")
            break

        output = result.stdout + "\n" + result.stderr

        if result.returncode != 0:
            print("\n" + "-" * 55)
            print("TEST RUN FAILED")
            print("-" * 55)

            print(output)

            if "MUTATION DETECTED!" in output:
                print("\nA mutation was detected by the test.")
            elif "Falsifying example:" in output:
                print("\nHypothesis reported a falsifying example.")
            else:
                print(
                    "\nThe test run failed, but this does not "
                    "necessarily mean a mutation was detected."
                )

            print(f"\nChaos engine stopped after {attempts} attempt(s).")
            return

        print("No failing tests detected in this attempt.")

        time.sleep(0.5)

    print(f"\nReached the attempt limit: {attempts}.")


if __name__ == "__main__":
    run_chaos_engine(max_attempts=100)
