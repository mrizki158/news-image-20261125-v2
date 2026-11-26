#!/usr/bin/env python3
"""Copy entry.png to the output directory (MAKEFUN_OUTPUT_DIR, default /output).

Stdlib only. Deterministic: the output bytes are exactly the committed
entry.png bytes, so repeated runs are byte-identical.
"""
import os
import shutil

HERE = os.path.dirname(os.path.abspath(__file__))


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    shutil.copyfile(
        os.path.join(HERE, "entry.png"),
        os.path.join(out_dir, "entry.png"),
    )


if __name__ == "__main__":
    main()
