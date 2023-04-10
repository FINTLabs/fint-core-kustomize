from menu import Menu


class KustomizeMenu(Menu):
    def __init__(self, main_menu: Menu):
        super().__init__()
        self.options = {
            "1": "Generate overlays",
            "2": "Modify all",
            "3": "Modify Api",
            "4": "Modify Beta",
            "5": "Modify Alpha"
        }
        self.main_menu = main_menu

    def get_actions(self):
        return {
            "1": exit
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

                self.main_menu.run()

