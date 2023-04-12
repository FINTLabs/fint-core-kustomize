from menu import MainMenu


def main():
    component = input("Project: fint-core-consumer-")
    menu = MainMenu(component)
    menu.run()


if __name__ == "__main__":
    main()
