from tools.translator import Translator
from scraper.model import Model
import xml.etree.ElementTree as Et
import urllib.request


XML_BASE_URL = "https://raw.githubusercontent.com/FINTLabs/fint-informasjonsmodell"


class ModelScraper:
    def __init__(self):
        self.translator = Translator()
        self.models = list()
        self.common_models = list()

    def get_common_model_names(self):
        return [model.name for model in self.common_models if not model.deprecated]

    def get_main_model_names(self):
        return [model.name for model in self.models if not model.deprecated]

    def get_main_models(self):
        return [model for model in self.models if not model.deprecated]

    def get_deprecated_models(self):
        return [model for model in self.models if model.deprecated]

    def fetch_models(self, version: str, domain: str, package: str):
        root = self.get_xml_root(version)
        valid_ids = self._get_valid_ids(root)

        self._fetch_common_models(root)
        self._update_common_models(valid_ids)

        domain = self._get_domain(root, domain)
        package = self._get_package(domain, package)

        self._fetch_models_from_package(package)
        self._update_models(valid_ids)

    def _get_domain(self, root, input_domain: str):
        for domain in root[1][0][0]:
            if input_domain.capitalize() in self.translator.replace(domain.attrib["name"]):
                return domain
            continue
        raise ValueError(f"Domain not found: {input_domain}")

    def _update_models(self, valid_ids: set[str]):
        for model in self.models:
            if model.id not in valid_ids:
                model.deprecated = True
            model.name = self.translator.replace(model.name)

    @staticmethod
    def _get_package(domain, input_package: str):
        for package in domain:
            if "name" in package.attrib.keys():
                if input_package.capitalize() in package.attrib["name"]:
                    return package
        raise ValueError(f"Package not found: {input_package}")

    @staticmethod
    def _get_valid_ids(root):
        """Returns all ids that are marked as main class."""
        main_ids = set()
        for model in root[1]:
            if "hovedklasse" in model.tag:
                main_ids.add(model.attrib["base_Class"])
        return main_ids

    def get_xml_root(self, version: str):
        """Fetches XML content from the URL and returns its root element."""
        xml_content = self._fetch_xml_content(version)
        return Et.fromstring(xml_content)

    def _fetch_models_from_package(self, package):
        for model in package:
            is_uml_class = "uml:Class" in model.attrib.values()
            is_abstract = "isAbstract" in model.attrib.keys()
            if is_uml_class and not is_abstract:
                for relation in model:
                    has_name = "name" in relation.attrib.keys()
                    if has_name:
                        relation_name = relation.attrib["name"].capitalize()
                        is_common_model_name = has_name and relation_name in self.get_common_model_names()
                        if has_name and is_common_model_name and relation_name not in self.get_main_model_names():
                            common_model = next((model for model in self.common_models if model.name == relation_name), None)
                            self.models.append(common_model)
                model_name = model.attrib["name"]
                model_id = list(model.attrib.values())[1]
                new_model = Model(model_name, model_id)
                self.models.append(new_model)

    @staticmethod
    def _fetch_xml_content(version: str):
        """Fetches XML content from the URL based on the given version."""
        if version in ["master", "main"]:
            url = f"{XML_BASE_URL}/{version}/FINT-informasjonsmodell.xml"
        else:
            url = f"{XML_BASE_URL}/v{version}/FINT-informasjonsmodell.xml"
        response = urllib.request.urlopen(url)
        if response.status == 200:
            return response.read().decode('windows-1252', 'replace')
        else:
            raise ValueError(f"Invalid version: {version} got status code: {response.status}")

    def _fetch_common_models(self, root):
        # [1][0][0][4] = EA_model -> Model -> FINT -> Felles
        for common_model in root[1][0][0][4]:
            if "uml:Class" in common_model.attrib.values():
                model = Model(common_model.attrib["name"], list(common_model.attrib.values())[1])
                self.common_models.append(model)

    def _update_common_models(self, valid_ids):
        self.common_models = [model for model in self.common_models if model.id in valid_ids]
