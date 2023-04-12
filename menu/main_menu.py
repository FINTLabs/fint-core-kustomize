from menu.menu import Menu
from menu.traefik_menu import TraefikMenu


class MainMenu(Menu):
    def __init__(self, component: str):
        super().__init__()
        self.options = {
            "1": "Modify traefik path in overlays",
            "2": "Change component"
        }
        self.component = component
        self.traefik_menu = TraefikMenu(self)

    def _update_component(self):
        self.clear()
        self.component = input("fint-core-consumer-")

    def get_actions(self):
        return {
            "1": self.traefik_menu.traverse_kustomize_overlays,
            "2": self._update_component
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

