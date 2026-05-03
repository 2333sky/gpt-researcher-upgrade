from pathlib import Path
import subprocess
import sys


def run_cli(tmp_path: Path, *args: str) -> subprocess.CompletedProcess[str]:
    env = None
    return subprocess.run(
        [sys.executable, "-m", "gptr_upgrade", "--root", str(tmp_path / "workspace"), *args],
        text=True,
        capture_output=True,
        check=True,
        env=env,
    )


def test_cli_happy_path(tmp_path: Path) -> None:
    init = run_cli(tmp_path, "init", "--title", "Test Project", "--project-id", "test-project")
    assert "Initialized project: test-project" in init.stdout

    run_cli(tmp_path, "add-topic", "test-project", "--title", "Memory architectures", "--priority", "0.9")
    run_cli(tmp_path, "add-source", "test-project", "--url", "https://example.com", "--title", "Example")
    run_cli(tmp_path, "add-checkpoint", "test-project", "--kind", "outline_approval", "--prompt", "Approve?")
    run_cli(tmp_path, "add-artifact", "test-project", "--type", "report", "--path", "reports/v1.md")
    run_cli(tmp_path, "add-memory", "test-project", "--level", "project", "--summary", "Prefer deeper source review")

    exported = run_cli(tmp_path, "export", "test-project")
    export_path = Path(exported.stdout.strip())
    assert export_path.exists()
    assert "test-project.md" in export_path.name
