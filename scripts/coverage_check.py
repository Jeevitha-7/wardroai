import argparse
import sys
import trace
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

TRACKED_FILES = [
    ROOT / "backend" / "analyzer.py",
    ROOT / "backend" / "catalog_matcher.py",
    ROOT / "backend" / "database.py",
    ROOT / "backend" / "main.py",
    ROOT / "scripts" / "start_streamlit.py",
]


def executable_lines(path):
    lines = set()
    for number, line in enumerate(path.read_text().splitlines(), start=1):
        stripped = line.strip()
        if stripped and not stripped.startswith("#"):
            lines.add(number)
    return lines


def run_tests():
    loader = unittest.TestLoader()
    suite = loader.discover(str(ROOT / "tests"))
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    return result.wasSuccessful()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--fail-under", type=float, default=25.0)
    args = parser.parse_args()

    tracer = trace.Trace(count=True, trace=False, ignoredirs=[sys.prefix, sys.exec_prefix])
    success = tracer.runfunc(run_tests)
    if not success:
        return 1

    counts = tracer.results().counts
    total = 0
    covered = 0

    print("\nCoverage report")
    for path in TRACKED_FILES:
        lines = executable_lines(path)
        hit = {line for (filename, line), count in counts.items() if Path(filename).resolve() == path and count}
        file_total = len(lines)
        file_covered = len(lines & hit)
        percent = 100.0 if file_total == 0 else (file_covered / file_total) * 100
        print(f"{path.relative_to(ROOT)}: {percent:.1f}% ({file_covered}/{file_total})")
        total += file_total
        covered += file_covered

    overall = 100.0 if total == 0 else (covered / total) * 100
    print(f"TOTAL: {overall:.1f}% ({covered}/{total})")

    if overall < args.fail_under:
        print(f"Coverage failed: {overall:.1f}% is below {args.fail_under:.1f}%", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
