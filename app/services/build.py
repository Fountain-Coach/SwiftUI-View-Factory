"""Utilities for compiling Swift code snippets."""

from __future__ import annotations

import os
import subprocess
import tempfile
from typing import Tuple, Union


def test_build(
    swift: str, output_binary: bool = False
) -> Union[Tuple[bool, str], Tuple[bool, str, str]]:
    """Compile Swift source code using ``swiftc``.

    Parameters
    ----------
    swift:
        Swift source code to compile.
    output_binary:
        If ``True`` and compilation succeeds, the path to the compiled binary
        is returned as a third tuple element.

    Returns
    -------
    Tuple
        ``(success, log)`` or ``(success, log, artifact_path)`` when
        ``output_binary`` is ``True`` and the compilation succeeded.
    """

    # Create temporary files for the Swift source and the resulting binary.
    src_fd, src_path = tempfile.mkstemp(suffix=".swift")
    bin_fd, bin_path = tempfile.mkstemp()

    try:
        with os.fdopen(src_fd, "w") as f:
            f.write(swift)

        os.close(bin_fd)  # close so swiftc can write the file

        try:
            result = subprocess.run(
                ["swiftc", src_path, "-o", bin_path, "--emit-executable"],
                capture_output=True,
                text=True,
            )
            success = result.returncode == 0
            log = f"{result.stdout}{result.stderr}".strip()
            if not success:
                err_lines = [l for l in log.splitlines() if "error:" in l]
                if err_lines:
                    log = "\n".join(err_lines)
        except FileNotFoundError as e:
            # swiftc not available
            success = False
            log = str(e)

    finally:
        # Source file is always removed
        try:
            os.remove(src_path)
        except OSError:
            pass

        # Remove binary if caller doesn't want it or compilation failed
        if not output_binary or not success:
            try:
                os.remove(bin_path)
            except OSError:
                pass

    if output_binary and success:
        return success, log, bin_path

    return success, log


# Prevent pytest from treating this function as a test case when imported.
test_build.__test__ = False
