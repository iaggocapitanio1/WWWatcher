import logging
from pathlib import Path
from typing import Union

import requests
from watchdog.events import PatternMatchingEventHandler, FileSystemEvent

from handlers.core.excel import ExcelHandler
from handlers.functions import get_file_name, generate_id
from settings import settings

logger = logging.getLogger(__name__)


class ExcelEventHandler(PatternMatchingEventHandler):
    def __init__(self, *args, **kwargs):
        super(ExcelEventHandler, self).__init__(patterns=['*.xlsx'], ignore_directories=True, case_sensitive=False)
        self.excelHandler = ExcelHandler()
        self.path = kwargs.get('path', settings.PROJECTS_DIR)

    @staticmethod
    def get_customer(user):
        if user is not None:
            logger.info(msg=f"Trying to get the customer id")
            logger.info(msg=f"url: {settings.WW4_GET_CUSTOMER_URL}")
            logger.info(msg=f"data: {user}")
            response = requests.post(url=settings.WW4_GET_CUSTOMER_URL, data={"user_id": user})
            logger.info(msg=f"Response: {response.text}, Status Code: {response.status_code}")
            if response.status_code == 200:
                customer = response.json().get("customer")
                logger.info(msg=f"Customer id found: {customer}")
                return customer
        logger.warning(msg=f"Fail to get customer id. ")
        return "undefined"

    @staticmethod
    def get_user(event):
        for directory in event.src_path.__str__().split('/'):
            logger.info(msg=f"trying to find user id in directory: {directory}")
            if directory.startswith('user_'):
                logger.info(msg=f"found user id in event path, user id is {directory}")
                return directory
        logger.warning(msg="Fail to get user id from event path.")
        return None

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
        name = get_file_name(event.src_path).replace("LISTA_DE_CORTE", "").lstrip("_")
        belongs_to = generate_id(name=name, object_type='Project')
        order_by = generate_id(name=self.get_customer(user=self.get_user(event)), object_type='Owner')
        self.excelHandler(path=event.src_path, belongs_to=belongs_to, orderBy=order_by)
