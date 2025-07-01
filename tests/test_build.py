import os
import subprocess
from app.services.build import test_build


def test_test_build_success(monkeypatch):
    def fake_run(cmd, capture_output, text):
        # create dummy binary file
        out_index = cmd.index("-o") + 1
        with open(cmd[out_index], "w") as f:
            f.write("binary")

        class Result:
            returncode = 0
            stdout = "ok"
            stderr = ""

        return Result()

    monkeypatch.setattr(subprocess, "run", fake_run)
    success, log, artifact = test_build('print("hi")', output_binary=True)
    assert success
    assert "ok" in log
    assert os.path.exists(artifact)
    os.remove(artifact)


def test_test_build_failure(monkeypatch):
    def fake_run(cmd, capture_output, text):
        class Result:
            returncode = 1
            stdout = ""
            stderr = "error"

        return Result()

    monkeypatch.setattr(subprocess, "run", fake_run)
    success, log = test_build("bad swift")
    assert not success
    assert "error" in log
