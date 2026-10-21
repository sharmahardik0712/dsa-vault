"""Run every pattern file (patterns/**/*.py, skipping _helpers) and report PASS/FAIL. Exits 1 if any fail."""
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).parent


def main() -> int:
    patterns = [p for p in (ROOT / "patterns").rglob("*.py") if not p.name.startswith("_")]
    files = sorted(patterns) + [ROOT / "python_toolbox.py"]
    failed = []
    for path in files:
        result = subprocess.run([sys.executable, str(path)], capture_output=True, text=True)
        ok = result.returncode == 0 and result.stdout.strip().endswith("ok")
        print(f"{'PASS' if ok else 'FAIL'}  {path.relative_to(ROOT).as_posix()}")
        if not ok:
            failed.append(path.name)
            print("      " + (result.stderr.strip() or result.stdout.strip()).replace("\n", "\n      "))
    print(f"\n{len(files) - len(failed)}/{len(files)} passed")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
