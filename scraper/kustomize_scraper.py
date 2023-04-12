import os


class KustomizeScraper:
    def __init__(self):
        self.idea_path = self._get_idea_path()

    @staticmethod
    def _get_idea_path():
        home_dir = os.path.expanduser('~')
        idea_projects_dir = os.path.join(home_dir, 'IdeaProjects')
        while not os.path.exists(idea_projects_dir) and 'IdeaProjects' in idea_projects_dir:
            print(f"IdeaProjects folder not found at: {idea_projects_dir}")
            idea_projects_dir = input("Full path to IdeaProjects: ")
        return idea_projects_dir

    def get_project_path(self, component: str):
        project_name = f"fint-core-consumer-{component}"
        project_path = os.path.join(self.idea_path, project_name)
        if not os.path.exists(project_path):
            raise NotADirectoryError(f"No directory at: {project_path}")
        return project_path

    def get_kustomize_path(self, component: str):
        kustomize_path = os.path.join(self.get_project_path(component), "kustomize")
        if not os.path.exists(kustomize_path):
            raise NotADirectoryError(f"Kustomize folder missing: {kustomize_path}")
        return kustomize_path

    def get_overlays_path(self, component: str):
        overlays_path = os.path.join(self.get_kustomize_path(component), "overlays")
        if not os.path.exists(overlays_path):
            raise NotADirectoryError(f"Overlays folder missing: {overlays_path}")
        return overlays_path
