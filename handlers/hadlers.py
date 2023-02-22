import logging
import os
from pathlib import Path
from typing import Union
from watchdog.events import PatternMatchingEventHandler, FileSystemEvent
from settings import settings
from handlers.core.excel import ExcelHandler
from handlers.functions import get_file_name, generate_id

logger = logging.getLogger(__name__)


class ExcelEventHandler(PatternMatchingEventHandler):
    def __init__(self, *args, **kwargs):
        super(ExcelEventHandler, self).__init__(patterns=['*.xlsx'], ignore_directories=True, case_sensitive=False)
        self.excelHandler = ExcelHandler()
        self.path = kwargs.get('path', settings.PROJECTS_DIR)

    def get_user(self):
        for directory in self.path.__str__().split('/'):
            if directory.startswith('user_'):
                return directory
        return 'No user'

    @property
    def path(self) -> Path:
        return self._path

    @path.setter
    def path(self, path: Union[Path, str]):
        if isinstance(path, str):
            path = Path(path)
        self._path = path.resolve()

    def on_created(self, event: FileSystemEvent):
        logger.info("Creation of object detected!")
        name = get_file_name(event.src_path).replace("LISTA_DE_CORTE", "")
        belongs_to = generate_id(name=name, object_type='Project')
        order_by = generate_id(name=self.get_user(), object_type='Owner')
        self.excelHandler(path=event.src_path, belongs_to=belongs_to, orderBy=order_by)
