import os


class Menu:
    def __init__(self):
        self.options = {}
        self.component = None

    def run(self):
        return

    def clear(self):
        os.system('cls' if os.name == 'nt' else 'clear')

    def display(self, menu: dict):
        for key in menu:
            print(f"{key}: {menu[key]}")

    def get_actions(self):
        return {}

