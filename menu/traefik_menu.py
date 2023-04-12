import os
import re
from menu.menu import Menu
from scraper.kustomize_scraper import KustomizeScraper
from scraper import ModelScraper


class TraefikMenu(Menu):
    def __init__(self, main_menu: Menu):
        super().__init__()
        self.options = {
            "1": "Choose environment"
        }
        self.main_menu = main_menu
        self.kustomize_scraper = KustomizeScraper()
        self.current_path = ""
        self.model_scraper = ModelScraper()
        self.admin_endpoints = ["admin/organisations", "admin/assets", "admin/caches", "admin/cache/status", "admin/cache/rebuild"]

    def _get_directories_in_current_path(self):
        directories = {}
        files = os.listdir(self.current_path)
        folders = [folder for folder in files
                   if os.path.isdir(os.path.join(self.current_path, folder))]
        for index, folder in enumerate(folders):
            directories[str(index + 1)] = folder
        return directories

    def traverse_kustomize_overlays(self):
        self.current_path = self.kustomize_scraper.get_overlays_path(self.main_menu.component)
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
        ingress_route_file_name = "ingress-route.yaml"
        ingress_route_path = os.path.join(self.current_path, ingress_route_file_name)
        if not os.path.exists(ingress_route_path):
            raise NotADirectoryError(f"Ingress route not found at: {ingress_route_path}")

        domain, package = self.main_menu.component.split("-")
        self.model_scraper.fetch_models("master", domain, package)
        models = self.model_scraper.get_main_model_names()
        host_line = self._get_host_line(ingress_route_path)
        used_endpoints = self._get_endpoints_from_host_line(host_line)
        while True:
            unused_endpoints = [endpoint.lower() for endpoint in models
                                if endpoint.lower() not in used_endpoints]
            unused_admin_endpoints = [endpoint.lower() for endpoint in self.admin_endpoints
                                      if endpoint.lower() not in used_endpoints]
            unused_endpoints_dict = self._get_dict_from_list(unused_endpoints + unused_admin_endpoints)
            self.clear()
            print(used_endpoints)
            self.display(unused_endpoints_dict)
            choice = input("Choice: ")
            if choice in unused_endpoints_dict.keys():
                used_endpoints.append(unused_endpoints_dict[choice])
            elif choice.lower() in used_endpoints:
                used_endpoints.remove(choice.lower())
            elif choice == "":
                self._generate_ingress_route(ingress_route_path, host_line, used_endpoints)
                return self.traverse_kustomize_overlays()

    @staticmethod
    def _get_dict_from_list(list_of_str: list[str]):
        test = {}
        for index, string in enumerate(list_of_str):
            test[str(index + 1)] = string
        return test

    @staticmethod
    def _get_endpoints_from_host_line(host_line: str):
        pattern = r"`(.*?)`"
        matches = re.findall(pattern, host_line)
        endpoints = []
        for endpoint in matches:
            endpoint_split = endpoint.split("/")
            length_of_endpoint = len(endpoint_split)
            if 'admin' in endpoint:
                if length_of_endpoint == 4:
                    endpoints.append("admin/*")
                elif length_of_endpoint == 5:
                    endpoints.append("admin/" + endpoint_split[4].lower())
            else:
                if length_of_endpoint == 3:
                    endpoints.append(endpoint_split[2] + "/*")
                elif length_of_endpoint == 4:
                    endpoints.append(endpoint_split[3].lower())
        return endpoints

    @staticmethod
    def _get_host_line(path_to_ingress_route_file: str):
        with open(path_to_ingress_route_file, 'r') as file:
            lines = file.readlines()
            for line in lines:
                if 'Host' in line:
                    return line

    def _generate_ingress_route(self, ingress_route_path: str, host_line: str, used_endpoints: list[str]):
        domain, package = self.main_menu.component.split("-")
        prefix = f"/{domain}/{package}/*"
        new_path_prefix = "(" if len(used_endpoints) > 1 else ""
        for endpoint in used_endpoints:
            if endpoint == used_endpoints[-1]:
                new_path_prefix += f"PathPrefix( `{prefix.replace('*', endpoint)}` )) " if len(used_endpoints) > 1 \
                    else f"PathPrefix( `{prefix.replace('*', endpoint)}` ) "
                continue
            new_path_prefix += f"PathPrefix( `{prefix.replace('*', endpoint)}` ) || "

        first_and_index = host_line.find("&&")
        second_and_index = host_line.find("&&", first_and_index + 1)

        before_string = host_line[:first_and_index + 3]
        after_string = host_line[second_and_index:]

        new_host_line = before_string + new_path_prefix + after_string
        self.clear()
        print(f"Do you want to update the traefik in this path: \n{ingress_route_path}")
        print(new_host_line)
        choice = input("Choice y/n (n): ")
        if choice.lower() in ["y", "ye", "yes"]:
            with open(ingress_route_path, "r") as file:
                lines = file.readlines()

            host_index = None
            for i, line in enumerate(lines):
                if "Host" in line:
                    host_index = i
                    break

            lines[host_index] = new_host_line + "\n" if host_index else host_line + "\n"

            with open(ingress_route_path, "w") as file:
                file.writelines(lines)

