import os
from menu import Menu
from kustomize_scraper import KustomizeScraper


class TraefikMenu(Menu):
    def __init__(self, main_menu: Menu):
        super().__init__()
        self.options = {
            "1": "Choose environment"
        }
        self.main_menu = main_menu
        self.kustomize_scraper = KustomizeScraper(main_menu.component)
        self.base_path = self._get_kustomize_path()
        self.current_path = self.base_path

    def get_actions(self):
        return {
            "1": exit
        }

    def _get_directories_in_current_path(self):
        directories = {}
        files = os.listdir(self.current_path)
        folders = [folder for folder in files if os.path.isdir(os.path.join(self.current_path, folder))]
        for index, folder in enumerate(folders):
            directories[str(index + 1)] = folder
        return directories

    def traverse_kustomize_overlays(self):
        self.current_path = self.base_path
        folder_depth = 0

        while folder_depth >= 0:
            current_directories = self._get_directories_in_current_path()
            self.clear()
            self.display(current_directories)
            choice = input("Choice: ")
            if choice in current_directories.keys():
                folder_depth += 1
                self.current_path = os.path.join(self.current_path, current_directories[choice])
                if folder_depth >= 2:
                    return self._edit_traefik_path()
            elif choice == "":
                folder_depth -= 1
                self.current_path = os.path.abspath(os.path.join(self.current_path, os.pardir))


    def _edit_traefik_path(self):


    def _get_kustomize_path(self):
        kustomize_path = os.path.join(self.kustomize_scraper.project_path, 'kustomize', 'overlays')
        if not os.path.exists(kustomize_path):
            raise NotADirectoryError(f"Kustomize folder missing: {kustomize_path}")
        return kustomize_path

## Example of menu
# Display and select environments in kustomize folder
# Display and select the different orgs
# Display all endpoints that's in the path
# Add or remove options
