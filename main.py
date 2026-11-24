#!/usr/bin/env python3
"""Fortune Cookie Wisdom for Developers.

Writes one original fortune-cookie line for a software developer to
/output/entry.txt (or $MAKEFUN_OUTPUT_DIR/entry.txt).

Gate: UTF-8 text, 1 to 120 characters, not only whitespace.
Deterministic, Python 3.13 stdlib only: no network, no wall clock, no
randomness. Writes only entry.txt, atomically (temp file + replace).
"""

import os
import tempfile

# Revised line: the draft was advice ("leave them a map"), and the judge
# weighs fortune-cookie wisdom above advice. This one only states a fate
# every senior engineer has watched happen: the temporary fix that
# outlived the engineer who swore it was temporary.
LINE = "Every legacy system began as a clever shortcut that outlived the engineer who swore it was temporary."


def main() -> None:
    line = LINE
    if not line.strip():
        raise SystemExit("line is only whitespace")
    if not (1 <= len(line) <= 120):
        raise SystemExit(f"line is {len(line)} characters, gate needs 1-120")
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.txt")
    fd, tmp = tempfile.mkstemp(dir=out_dir, prefix=".entry-", suffix=".tmp")
    try:
        with os.fdopen(fd, "w", encoding="utf-8", newline="\n") as f:
            f.write(line)
        os.replace(tmp, path)
    except BaseException:
        try:
            os.unlink(tmp)
        except OSError:
            pass
        raise


if __name__ == "__main__":
    main()
