from payload.core.core import BasePayload
from enum import Enum


# noinspection PyPep8Naming
class AssemblyPayload(BasePayload):
    RELATIONAL_PROPS = ['belongsTo']

    class Status(Enum):
        WAITING = 0
        ASSEMBLING = 1
        TESTING = 2
        PACKED = 3

    def __init__(self, **kwargs):
        super(AssemblyPayload, self).__init__(**kwargs)
        self.type = kwargs.get('type', 'Part')
        self.startTime = kwargs.get('startTime', '')
        self.finishTime = kwargs.get('finishTime', '')
        self.assemblyStatus = kwargs.get('assemblyStatus', 0)
        self.belongsTo = kwargs.get("belongsTo", "")
        self.orderBy = kwargs.get("orderBy", "")

    @property
    def belongsTo(self) -> str:
        return self._belongsTo

    @belongsTo.setter
    def belongsTo(self, belongsTo: str) -> None:
        self._belongsTo = belongsTo

    @property
    def startTime(self) -> str:
        return self._startTime

    @startTime.setter
    def startTime(self, startTime: str) -> None:
        self._startTime = startTime

    @property
    def finishTime(self) -> str:
        return self._finishTime

    @finishTime.setter
    def finishTime(self, finishTime: str) -> None:
        self._finishTime = finishTime

    @property
    def assemblyStatus(self) -> int:
        return self._assemblyStatus

    @assemblyStatus.setter
    def assemblyStatus(self, assemblyStatus: int) -> None:
        self._assemblyStatus = assemblyStatus

    @property
    def orderBy(self) -> bool:
        return self._orderBy

    @orderBy.setter
    def orderBy(self, orderBy: bool) -> None:
        self._orderBy = orderBy
