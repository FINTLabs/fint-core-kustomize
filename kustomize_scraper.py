import os


class KustomizeScraper:
    def __init__(self, component: str):
        self.idea_path = self._get_idea_path()
        self.component = component
        self.project_path = self._get_project_path()

    @staticmethod
    def _get_idea_path():
        home_dir = os.path.expanduser('~')
        idea_projects_dir = os.path.join(home_dir, 'IdeaProjects')
        while not os.path.exists(idea_projects_dir) and 'IdeaProjects' in idea_projects_dir:
            print(f"IdeaProjects folder not found at: {idea_projects_dir}")
            idea_projects_dir = input("Full path to IdeaProjects: ")
        return idea_projects_dir

    def _get_project_path(self):
        project_name = f"fint-core-consumer-{self.component}"
        project_path = os.path.join(self.idea_path, project_name)
        if not os.path.exists(project_path):
            raise NotADirectoryError(f"No directory at: {project_path}")
        return project_path


t = KustomizeScraper("utdanning-vurdering")
print(t.project_path)
