from __future__ import annotations

from dataclasses import asdict
from pathlib import Path

from gptr_upgrade.common import load_json, save_json
from gptr_upgrade.workspace.models import ResearchProject


class WorkspaceStore:
    def __init__(self, root: str | Path):
        self.root = Path(root)

    def project_dir(self, project_id: str) -> Path:
        return self.root / "projects" / project_id

    def project_path(self, project_id: str) -> Path:
        return self.project_dir(project_id) / "project.json"

    def init_project(self, project: ResearchProject) -> Path:
        project_dir = self.project_dir(project.project_id)
        for rel in ["reports", "drafts", "traces", "memory", "exports"]:
            (project_dir / rel).mkdir(parents=True, exist_ok=True)
        (project_dir / "notes.md").touch(exist_ok=True)
        self.save_project(project)
        return project_dir

    def save_project(self, project: ResearchProject) -> Path:
        project.touch()
        return save_json(self.project_path(project.project_id), asdict(project))

    def load_project(self, project_id: str) -> ResearchProject:
        payload = load_json(self.project_path(project_id), None)
        if not payload:
            raise FileNotFoundError(f"Project not found: {project_id}")
        return ResearchProject(**payload)

    def list_projects(self) -> list[ResearchProject]:
        projects_dir = self.root / "projects"
        if not projects_dir.exists():
            return []
        results: list[ResearchProject] = []
        for path in sorted(projects_dir.glob("*/project.json")):
            payload = load_json(path, None)
            if payload:
                results.append(ResearchProject(**payload))
        return results
