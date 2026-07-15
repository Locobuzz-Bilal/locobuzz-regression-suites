# import os, sys, time, subprocess, pathlib

# ROOT = pathlib.Path(__file__).resolve().parents[1]

# SUITES = [
#     ("twitter",  [sys.executable, str(ROOT / "Suites" / "test_twitter_suite.py")]),
#     ("facebook", [sys.executable, str(ROOT / "Suites" / "test_facebook_suite.py")]),
# ]

# def stream_prefixed(name, pipe):
#     for line in iter(pipe.readline, ''):
#         if not line:
#             break
#         print(f"[{name}] {line.rstrip()}")

# def main():
#     print("Starting parallel suites...\n")
#     procs = []
#     for name, cmd in SUITES:
#         print(f"Spawn: {name} -> {' '.join(cmd)}")
#         p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, bufsize=1)
#         procs.append((name, p))
#     start = time.time()
#     # Loop until all finish
#     while procs:
#         for name, p in list(procs):
#             if p.poll() is None:
#                 stream_prefixed(name, p.stdout)
#             else:
#                 # Drain remaining
#                 stream_prefixed(name, p.stdout)
#                 procs.remove((name, p))
#         time.sleep(0.3)
#     print("\nSummary:")
#     overall_pass = True
#     for name, p in SUITES:
#         rc = p[1] if isinstance(p, int) else None  # unused
#     for name, cmd in SUITES:
#         # Quick status re-run not needed; just trust earlier output
#         pass
#     # Better: re-run collection of exit codes
#     # (Rebuild for clarity)
#     exit_codes = []
#     for name, cmd in SUITES:
#         # Can't get exit direct now; restructure earlier:
#         pass

# if __name__ == "__main__":
#     # Improved version with proper exit codes
#     ROOT = pathlib.Path(__file__).resolve().parents[1]
#     SUITES = [
#         ("twitter",  [sys.executable, str(ROOT / "Suites" / "test_twitter_suite.py")]),
#         ("facebook", [sys.executable, str(ROOT / "Suites" / "test_facebook_suite.py")]),
#     ]
#     procs = []
#     print("Starting parallel suites...\n")
#     start = time.time()
#     for name, cmd in SUITES:
#         print(f"Spawn: {name} -> {' '.join(cmd)}")
#         p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, bufsize=1)
#         procs.append((name, p))

#     alive = True
#     while alive:
#         alive = False
#         for name, p in procs:
#             if p.poll() is None:
#                 alive = True
#                 while True:
#                     line = p.stdout.readline()
#                     if not line:
#                         break
#                     print(f"[{name}] {line.rstrip()}")
#         time.sleep(0.25)

#     # Drain remaining
#     for name, p in procs:
#         for line in p.stdout.readlines():
#             if line.strip():
#                 print(f"[{name}] {line.rstrip()}")

#     print("\nSummary:")
#     overall_ok = True
#     for name, p in procs:
#         rc = p.wait()
#         print(f"  {name}: exit {rc}")
#         if rc != 0:
#             overall_ok = False

#     print(f"\nOverall: {'PASS' if overall_ok else 'FAIL'}  Elapsed: {time.time()-start:.1f}s")
#     sys.exit(0 if overall_ok else 1)



#--------------------------------Copilot----------------------------------------------------







import os
import sys
import time
import subprocess
import pathlib

ROOT = pathlib.Path(__file__).resolve().parents[1]

SUITES = [
    ("twitter",  [sys.executable, str(ROOT / "Suites" / "test_twitter_suite.py")]),
    ("facebook", [sys.executable, str(ROOT / "Suites" / "test_facebook_suite.py")]),
]

def stream_prefixed(name, pipe):
    """Stream lines from subprocess pipe with suite prefix."""
    for line in iter(pipe.readline, ''):
        if not line:
            break
        print(f"[{name}] {line.rstrip()}")

def main():
    print("Starting parallel suites...\n")

    procs = []
    # Force UTF-8 for child processes
    env = os.environ.copy()
    env["PYTHONUTF8"] = "1"

    # Spawn all suites
    for name, cmd in SUITES:
        print(f"Spawn: {name} -> {' '.join(cmd)}")
        p = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            bufsize=1,
            env=env,
            encoding='utf-8'
        )
        procs.append((name, p))

    start_time = time.time()
    alive = True

    # Stream output until all finish
    while alive:
        alive = False
        for name, p in procs:
            if p.poll() is None:
                alive = True
                while True:
                    line = p.stdout.readline()
                    if not line:
                        break
                    print(f"[{name}] {line.rstrip()}")
        time.sleep(0.25)

    # Drain remaining output
    for name, p in procs:
        for line in p.stdout.readlines():
            if line.strip():
                print(f"[{name}] {line.rstrip()}")

    # Summary of exit codes
    print("\nSummary:")
    overall_ok = True
    for name, p in procs:
        rc = p.wait()
        print(f"  {name}: exit {rc}")
        if rc != 0:
            overall_ok = False

    elapsed = time.time() - start_time
    print(f"\nOverall: {'PASS' if overall_ok else 'FAIL'}  Elapsed: {elapsed:.1f}s")
    sys.exit(0 if overall_ok else 1)


if __name__ == "__main__":
    main()
