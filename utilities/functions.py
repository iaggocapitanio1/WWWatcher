import functools
import logging
import re
from pathlib import Path
from typing import Union, Optional, List
from utilities.http_request import make_request
from pandas import DataFrame, read_excel
from unidecode import unidecode

import settings
from payload import ConsumablePayload, PartPayload, ModulePayload

logger = logging.getLogger(__name__)


def get_furniture_ids(excel_file_name, folder_target: Path):
    """
    Get a list of furniture IDs related to the given Excel file name.

    Args:
        excel_file_name (str): The name of the Excel file to search for.
        folder_target (Path): The target folder where the mapping file is located.

    Returns:
        list: A list of furniture IDs related to the given Excel file name.
              Returns an empty list if the mapping file doesn't exist.
    """
    mapping_file = folder_target / settings.MAPPING_FILE
    furniture_ids = set()
    if not mapping_file.exists():
        logger.error("Mapping file does not exist.")
        return list(furniture_ids)

    df = read_excel(mapping_file)
    for column in df.columns:
        if (df[column].str.strip() == excel_file_name).any():
            ids = df.loc[df[column].str.strip() == excel_file_name, 'id\lists'].tolist()
            furniture_ids.update(ids)
    return list(furniture_ids)


def validate_path(path: Union[str, Path]) -> Path:
    if isinstance(path, str):
        path = Path(path)
    return path.resolve()


def clean_name(name: str) -> str:
    return re.sub(r'[^\w]', '_', name)


def get_furniture_name(file: str, budget_name: str) -> str:
    return file.replace(budget_name.upper().strip(), '').replace(' ', '').strip('_')


def verify(source_path: Path) -> bool:
    """
    Verifies if the given source path contains the specified reference as one of its parts and
    if it is not a directory.

    This function takes a path and a reference string as input. It first checks if the source_path
    is a directory, and if so, returns False. It then checks if the reference string is part of the path.
    If it is, the function traverses up the path to confirm if any part of the path matches the reference string.

    :param source_path: A Path object representing the source path to be verified.
    :return: True if the source path contains the reference and is not a directory, False otherwise.
    """
    if source_path.is_dir():
        return False
    if settings.CUT_LIST_DIR not in source_path.parts:
        return False
    current_path = Path(*source_path.parts[source_path.parts.index(settings.CUT_LIST_DIR):])
    while current_path != current_path.parent:  # Stop when reaching the root directory
        if current_path.name == settings.CUT_LIST_DIR:
            return True
        current_path = current_path.parent
    return False


def get_email(path: Union[str, Path]) -> str:
    path = validate_path(path)
    return path.parts[path.parts.index(settings.KEYWORD) + 1]


def get_budget_name(path: Union[str, Path]) -> str:
    path = validate_path(path)
    return path.parts[path.parts.index(settings.KEYWORD) + 2]


def get_customer_id(path: Union[str, Path]) -> str:
    email = get_email(path)
    response = make_request(method='POST', relative_url='accounts/get-customer/', data={'email': email})
    if response.status_code == 200:
        return response.json()['customer']
    return ''


def get_path_after_keyword(path: Union[str, Path]) -> Optional[Path]:
    try:
        logger.info(f"Trying to get reference path after keyword {settings.KEYWORD}: {path}")
        path = validate_path(path)
        path = Path(*path.parts[path.parts.index(settings.KEYWORD):])
        return path
    except Exception as error:
        logger.error(f"Error: Unable to retrieve the relative path. \n"
                     f"The event may have been triggered outside the reference path. {error}")


def generate_id(name: str, object_type: str = 'Part') -> str:
    name_ascii = unidecode(name)
    name_cleaned = re.sub(r'[^a-zA-Z0-9_-]', '', name_ascii)
    name_cleaned = clean_name(name_cleaned)
    return f'urn:ngsi-ld:{object_type}:{name_cleaned}'


def check(string: str) -> bool:
    return string in {"CNC", "X"}


def send_payload(payload):
    try:
        logger.info("Trying to post payload...")
        response = payload.post()
        logger.info(f"Response Status Code: {response.status_code}")
        if response.status_code == 409:
            logger.info("Trying to patch payload...")
            response = payload.delete()
            logger.info(f"Delete Status Code: {response.status_code}")
            response = payload.post()
            logger.info(f"Post Status Code: {response.status_code}")

        if response.status_code == 201 or response.status_code == 200:
            logger.info(response.status_code)
            logger.info(response.json())
        elif len(response.text) < 300:
            logger.info(response.status_code)
            logger.info(response.text)
        else:
            logger.info(response.status_code)
            logger.info("Response too long to display.")

    except Exception as error:
        logger.error(f"Error: Unable to send payload. {error}")


def batch_modules_payload(belongs_to_furniture: str, modules: list, prefix: str = '') -> None:
    if not modules:
        return
    if prefix and not prefix.endswith("_"):
        prefix = prefix + "_"
    for module in modules:
        identifier = generate_id(f"{prefix}{module}", object_type='Module')
        payload = ModulePayload(id=identifier, name=module, belongsToFurniture=belongs_to_furniture)
        send_payload(payload)


def get_correlated_module(part: str, modules: list) -> str:
    """
    Find the module that is correlated to the given part.

    Parameters:
    - part (str): The part name.
    - modules (list): The list of module names.

    Returns:
    - str: The correlated module name. Returns an empty string if no correlation is found.
    """
    longest_match = ""
    for module in modules:
        if module in part and len(module) > len(longest_match):
            longest_match = module
    return longest_match


def get_module(name: str, prefix: str, modules: list) -> str:
    module: str = get_correlated_module(name, modules=modules)
    return generate_id(f"{prefix}{module}", object_type='Module')


@functools.cache
def generate_dimensions(coordinates: List[List[int]] = None) -> dict:
    if coordinates is None:
        coordinates = [[0, 0], [0, 1], [1, 1], [1, 0], [0, 0]]
    return dict(type="Polygon", coordinates=[coordinates])


def process_row(name, payload_cls, belongs_to, **kwargs):
    object_type = kwargs.get("object_type", "Part")
    identifier = generate_id(name, object_type=object_type)
    if object_type == 'Consumable':
        prefix = kwargs.pop("prefix")
        kwargs.update(dict(name=name))
        identifier = generate_id(f"{prefix}{name}", object_type=object_type)
    payload = payload_cls(id=identifier, belongsTo=belongs_to, **kwargs)
    send_payload(payload)


def consumable_accessories_payload(data_frame: DataFrame, belongs_to: str, belongs_to_furniture: str, prefix: str,
                                   **kwargs):
    if data_frame is None:
        return
    try:
        for _, row in data_frame.iterrows():
            name, mat, quant, obs = row
            process_row(name, ConsumablePayload, belongs_to, amount=quant, belongsToFurniture=belongs_to_furniture,
                        status=0, object_type='Consumable', prefix=prefix)
    except ValueError as error:
        logger.error(f"Error: Unable to process consumable accessories payload. {error}")


def part_compact_panels_payload(data_frame: DataFrame, belongs_to: str, belongs_to_furniture: str, modules: list,
                                prefix: str, **kwargs):
    if data_frame is None:
        return
    for _, row in data_frame.iterrows():
        name, mat, quant, length, width, thickness, tag, nesting, cnc, f2, f3, f4, f5, obs = row
        process_row(name, PartPayload, belongs_to, partName=name, material=mat, amount=quant, length=length,
                    weight=width, dimensions=generate_dimensions(), thickness=thickness, tag=tag, cncFlag=check(cnc),
                    nestingFlag=check(nesting), f2=f2, f3=f3, f4=f4, f5=f5, observation=obs,
                    belongsToModule=get_module(name, prefix, modules=modules),
                    belongsToFurniture=belongs_to_furniture)


def part_panels_payload(data_frame: DataFrame, belongs_to: str, belongs_to_furniture: str, modules: list, prefix: str,
                        **kwargs):
    if data_frame is None:
        return
    for _, row in data_frame.iterrows():
        name, sort, mat, quant, length, width, thickness, tag, nesting, cnc, f2, f3, f4, f5, groove, o2, o3, o4, o5, \
            obs, weight, op_cnc = row
        process_row(name, PartPayload, belongs_to, partName=name, sort=sort, material=mat, amount=quant, length=length,
                    width=width, weight=weight, dimensions=generate_dimensions(), thickness=thickness, tag=tag,
                    nestingFlag=check(nesting), cncFlag=check(cnc), f2=f2, f3=f3, f4=f4, f5=f5, groove=groove,
                    belongsToFurniture=belongs_to_furniture, orla2=check(o2), orla3=check(o3), orla4=check(o4),
                    orla5=check(o5), observation=obs, belongsToModule=get_module(name, prefix ,modules),)
