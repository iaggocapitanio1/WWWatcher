import logging
from pathlib import Path
from typing import Union, Literal

from pandas import read_excel, DataFrame

from handlers.functions import consumable_accessories_payload, part_panels_payload, part_compact_panels_payload
from settings import settings

logger = logging.getLogger(__name__)

SHEETS = Literal["panels", "compact-panels", "accessories"]

URL = settings.ORION_HOST + "/ngsi-ld/v1/entities/"


class ExcelHandler(object):

    @staticmethod
    def get_sheet(name: str) -> int:
        """
        Retrieve the sheet name based on the given `name` from the settings file. The sheet name is obtained from the
        `settings.EXCEL_PATTERN` dictionary, which is expected to be stored in a file called `settings.json`. The
        `sheet_name` key is looked up in the dictionary using the `name` argument as the key. If the value of
        `sheet_name` is a list, the first element of the list is returned, otherwise, the value of `sheet_name` is
        returned as is.
        :param name: A string representing the name of the sheet to retrieve.
        :return: An int representing the name of the sheet.
        """

        sheet_name = settings.EXCEL_PATTERN.get(name).get('sheet_name')
        logger.info(msg=f"Getting sheet: {sheet_name}")
        if isinstance(sheet_name, list):
            return sheet_name[0]
        return sheet_name

    @staticmethod
    def get_columns(name: str):
        return settings.EXCEL_PATTERN.get(name).get('columns')

    @staticmethod
    def get_valid_table(data_frame: DataFrame, column_name: Union[str, int] = 'REF PEÇA (A)'):
        logger.debug(f"Validating table according to column: {column_name}")
        if isinstance(column_name, int):
            column_name = data_frame.columns[column_name]
        try:
            assert column_name in data_frame.columns
        except Exception as error:
            logger.error("The table doesn't have the column specified!")
            logger.exception(error)

        new_data_frame: DataFrame = data_frame.dropna(axis=0, subset=[column_name])
        new_data_frame = new_data_frame.fillna('')
        return new_data_frame

    def get_data_frame(self, path, sheet_name: str) -> DataFrame:
        data_frame = read_excel(path, self.get_sheet(sheet_name), header=0, usecols=self.get_columns(sheet_name))
        return self.get_valid_table(data_frame=data_frame, column_name=0)

    def generate_payload(self, path: Union[str, Path], belongs_to: str, orderBy: str) -> None:
        logger.info("Extracting data from dataframes!")
        panels_df = self.get_data_frame(sheet_name="panels", path=path)
        part_panels_payload(data_frame=panels_df, belongs_to=belongs_to, orderBy=orderBy)
        compact_panels_df = self.get_data_frame(sheet_name="compact-panels", path=path)
        part_compact_panels_payload(data_frame=compact_panels_df, belongs_to=belongs_to, orderBy=orderBy)
        accessories_df = self.get_data_frame(sheet_name="accessories", path=path)
        consumable_accessories_payload(data_frame=accessories_df, belongs_to=belongs_to)

    def __call__(self, *args, **kwargs):
        belongs_to = kwargs.get("belongs_to", '')
        orderBy = kwargs.get("orderBy", '')
        path = kwargs.get("path", "")
        self.generate_payload(path=path, belongs_to=belongs_to, orderBy=orderBy)
