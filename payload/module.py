from .core.core import BasePayload


# noinspection PyPep8Naming
class ModulePayload(BasePayload):
    RELATIONAL_PROPS = ['belongsToFurniture']
    RESOURCE = 'module/'

    def __init__(self, **kwargs):
        super(ModulePayload, self).__init__(**kwargs)
        self.type = kwargs.get('type', 'Module')
        self.name = kwargs.get('name', '')
        self.belongsToFurniture = kwargs.get("belongsToFurniture", "")

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, name: str) -> None:
        self._name = name

    @property
    def belongsToFurniture(self) -> str:
        return self._belongsToFurniture

    @belongsToFurniture.setter
    def belongsToFurniture(self, belongsToFurniture: str) -> None:
        self._belongsToFurniture = belongsToFurniture
