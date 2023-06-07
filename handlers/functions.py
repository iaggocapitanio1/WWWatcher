import datetime
import logging
from pathlib import Path
from typing import Union

from pandas import DataFrame

from payload import ConsumablePayload, PartPayload
from settings import settings

logger = logging.getLogger(__name__)

URL = settings.ORION_HOST + "/ngsi-ld/v1/entities/"


def get_file_name(path: Union[str, Path]) -> str:
    """
    This function takes the path of a file and extracts its name for any operational system
    that the lib os covers.
    :param path:  file path in string format.
    :return: file name in string format.
    """
    import os
    if isinstance(path, str):
        path = Path(path)
    path = path.resolve()
    name, ext = os.path.splitext(os.path.basename(path))
    name = name.strip().replace(' ', '_').upper()
    logger.info(f"Getting file name: {name}")
    return name


def get_file_dir(file_path: str) -> str:
    """
    This function return the directory that a file is located. For instance,
    an Excel file that has the path: C:\\User\\John\\Documents\\my_excel.xlsx.
    This function will return the directory path: C:\\User\\John\\Documents\\.

    :param file_path: file path in string format.
    :return: directory path in string format.
    """
    from pathlib import Path
    path = Path(file_path).resolve()
    logger.info(f"Getting Directory name: {path.parent.__str__()}")
    return path.parent.__str__()


def generate_id(name: str, object_type: str = 'Part') -> str:
    """
    This function generates an id that matches with the name, which must preserve the unique constraint.

    :param name: the file name in string format.
    :param object_type: the object type in string format as the NGSI-LD recommend.
    :return: the id in string format.
    """
    identifier = f'urn:ngsi-ld:{object_type}:' + name
    logger.info(msg=f"Generated id: {identifier} for name: {name}")
    return identifier.__str__()


def validate_project_name(project_name: str) -> str:
    if '.' in project_name:
        raise ValueError("The project name cannot have a dot in its name!")
    return project_name.lower()


def consumable_accessories_payload(data_frame: DataFrame, belongs_to: str, **kwargs):
    """
    This function aim to extract the panels of a predefined pandas DataFrame and
    send the payloads to context broker.
    :param data_frame:
    :param belongs_to:
    """
    observed_at = kwargs.get("observed_at", datetime.datetime.utcnow().isoformat())

    for index, row in tuple(data_frame.iterrows()):
        logger.info(f"Accessories Row: \n {row}")
        name, mat, quant, obs = row
        identifier: str = generate_id(name, object_type='Part')
        consumable = ConsumablePayload(id=identifier, name=name, amount=quant, status=0, belongsTo=belongs_to)
        logger.debug(msg=f"Extracting form excel the values:"
                         f" {identifier, name, mat, quant, obs, belongs_to, observed_at}")
        logger.debug(msg=f"Trying to post Accessories...")
        response = consumable.post()
        logger.debug(msg=f"Response Status Code: {response.status_code}")
        if response != 201:
            logger.debug(msg=f"Trying to patch Accessories...")
            response = consumable.patch()
            logger.debug(msg=f"Response Status Code: {response.status_code}")


def check(string: str) -> bool:
    return string == "CNC" or string == "X"


def part_compact_panels_payload(data_frame: DataFrame, belongs_to: str, orderBy: str, **kwargs):
    """
    This function aim to extract the panels of a predefined pandas DataFrame and
    send the payloads to context broker.
    :param orderBy:
    :param data_frame:
    :param belongs_to:
    """

    for index, row in tuple(data_frame.iterrows()):
        logger.info(f"Compact Panels Row: \n {row}")
        name, mat, quant, length, width, thickness, tag, nesting, cnc, f2, f3, f4, f5, obs = row

        identifier: str = generate_id(name, object_type='Part')
        panel = PartPayload(id=identifier,
                            partName=name,
                            material=mat,
                            amount=quant,
                            length=length,
                            weight=width,
                            dimensions=dict(
                                type="Polygon",
                                coordinates=[[[0, 0], [0, 1], [1, 1], [1, 0], [0, 0]]]
                            ),
                            thickness=thickness,
                            tag=tag,
                            nestingFlag=check(nesting),
                            cncFlag=check(cnc),
                            f2=f2,
                            f3=f3,
                            f4=f4,
                            f5=f5,
                            observation=obs,
                            belongsTo=belongs_to,
                            orderBy=orderBy)
        logger.debug(msg=f"Trying to post Compact Panel...")
        response = panel.post()
        logger.debug(msg=f"Response Status Code: {response.status_code}")
        if response != 201:
            logger.debug(msg=f"Trying to patch Compact Panel...")
            response = panel.patch()
            logger.debug(msg=f"Response Status Code: {response.status_code}")


def part_panels_payload(data_frame: DataFrame, belongs_to: str, orderBy: str, **kwargs):
    """
    This function aim to extract the panels of a predefined pandas DataFrame and
    send the payloads to context broker.
    :param orderBy:
    :param data_frame:
    :param belongs_to:
    """
    for index, row in tuple(data_frame.iterrows()):
        logger.info(f"Panels Row: \n {row}")
        name, sort, mat, quant, length, width, thickness, tag, nesting, cnc, f2, f3, f4, f5, groove, o2, o3, o4, o5, \
            obs, weight, op_cnc = row
        identifier: str = generate_id(name, object_type='Part')
        panel = PartPayload(id=identifier,
                            partName=name,
                            sort=sort,
                            material=mat,
                            amount=quant,
                            length=length,
                            width=width,
                            dimensions=dict(
                                type="Polygon",
                                coordinates=[[[0, 0], [0, 1], [1, 1], [1, 0], [0, 0]]]
                            ),
                            thickness=thickness,
                            tag=tag,
                            nestingFlag=check(nesting),
                            cncFlag=check(cnc),
                            f2=f2,
                            f3=f3,
                            f4=f4,
                            f5=f5,
                            groove=groove,
                            orla2=check(o2),
                            orla3=check(o3),
                            orla4=check(o4),
                            orla5=check(o5),
                            observation=obs,
                            weight=weight,
                            belongsTo=belongs_to,
                            orderBy=orderBy)
        response = panel.post()
        logger.debug(msg=f"Response Status Code: {response.status_code}")
        if response != 201:
            logger.debug(msg=f"Trying to patch Panels...")
            response = panel.patch()
            logger.debug(msg=f"Response Status Code: {response.status_code}")
            logger.info(msg=f"Response text : {response.text}")