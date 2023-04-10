import os
from menu import Menu
from kustomize_menu import KustomizeMenu
from traefik_menu import TraefikMenu


class MainMenu(Menu):
    def __init__(self, component: str):
        super().__init__()
        self.options = {
            "1": "Create new kustomize overlays",
            "2": "Modify traefik path in overlays",
            "3": "Change component"
        }
        self.component = component
        self.kustomize_menu = KustomizeMenu(self)
        self.traefik_menu = TraefikMenu(self)

    def _update_component(self):
        self.clear()
        self.component = input("fint-core-consumer-")

    def get_actions(self):
        return {
            "1": self.kustomize_menu.run,
            "2": self.traefik_menu.traverse_kustomize_overlays,
            "3": self._update_component
        }

    def run(self):
        actions = self.get_actions()
        while True:
            self.clear()
            self.display(self.options)
            choice = input("Choice: ")
            if choice in actions.keys():
                actions[choice]()
            elif choice == "":
                exit()

