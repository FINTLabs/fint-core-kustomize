class Model:
    def __init__(self, name: str, id: str, deprecated: bool = False):
        self.name = name
        self.id = id
        self.deprecated = deprecated
