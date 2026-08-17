#!/usr/bin/env python3
"""S0 T0-4 — 가드 6종 일괄 실행.

    python3 build/guards/run_all.py            # 실패 시 exit 1
    python3 build/guards/run_all.py --report   # 전부 실행하고 요약만 (exit 0)
    python3 build/guards/run_all.py --strict   # G3 도 실패로 취급
"""
import argparse
import pathlib
import subprocess
import sys

HERE = pathlib.Path(__file__).resolve().parent
GUARDS = [("G1", "guard_weekday.py"), ("G2", "guard_hardcode.py"),
          ("G3", "guard_required_fields.py"), ("G4", "guard_conflict.py"),
          ("G5", "guard_decisions.py"), ("G6", "guard_freshness.py")]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--report", action="store_true")
    ap.add_argument("--strict", action="store_true")
    a = ap.parse_args()

    results = {}
    for gid, script in GUARDS:
        r = subprocess.run([sys.executable, str(HERE / script)],
                           capture_output=True, text=True, cwd=str(HERE))
        print(r.stdout.rstrip())
        if r.stderr.strip():
            print(r.stderr.rstrip())
        results[gid] = r.returncode

    print("=" * 60)
    failed = [g for g, rc in results.items() if rc != 0]
    if a.strict:
        pass
    print("가드 종합: " + ("ALL GREEN" if not failed else f"FAIL {failed}"))
    if a.report:
        return 0
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
