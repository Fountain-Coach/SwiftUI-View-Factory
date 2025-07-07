import subprocess
import uuid
import shutil
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
DISPATCH = REPO_ROOT / "scripts" / "dispatch.sh"


def _run_cli(*args):
    return subprocess.run(
        [str(DISPATCH), *args],
        cwd=REPO_ROOT,
        text=True,
        capture_output=True,
        check=True,
    )


def _clean_dirs():
    for name in ("requests", "logs", "processed"):
        p = REPO_ROOT / name
        if p.exists():
            shutil.rmtree(p)
        p.mkdir()


def test_version():
    result = _run_cli("--version")
    assert result.stdout.strip() == "0.1.0"


def test_selftest():
    result = _run_cli("--selftest")
    assert "Dispatcher OK" in result.stdout


def test_deploy_request():
    _clean_dirs()
    req_dir = REPO_ROOT / "requests"
    fixture = REPO_ROOT / "tests" / "fixtures" / "deploy_request.yml"
    req_file = req_dir / f"{uuid.uuid4()}.yml"
    shutil.copyfile(fixture, req_file)

    _run_cli()

    assert (REPO_ROOT / "processed" / req_file.name).exists()
    log_dir = REPO_ROOT / "logs" / req_file.stem
    expected_log = f"Deploy handler executed for requests/{req_file.name}"
    assert (log_dir / "deploy.log").read_text().strip() == expected_log
    assert (log_dir / "status.yml").read_text().strip() == "status: success"

    _clean_dirs()
