import logging

logger = logging.getLogger(__name__)


def get_file_name(path: str) -> str:
    """
    This function takes the path of a file and extracts its name for any operational system
    that the lib os covers.
    :param path:  file path in string format.
    :return: file name in string format.
    """
    import os
    file_name = os.path.basename(path)
    logger.info(f"Getting file name: {file_name}")
    file_name = file_name.replace(' ', '_')
    name, ext = os.path.splitext(file_name)
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


def generate_id(file_name: str, object_type: str = 'Part') -> str:
    """
    This function generates an id that matches with the file_name, which must preserve the unique constraint.

    :param file_name: the file name in string format.
    :param object_type: the object type in string format as the NGSI-LD recommend.
    :return: the id in string format.
    """
    identifier = f'urn:ngsi-ld:{object_type}:' + file_name
    logger.info(msg=f"Generated id: {identifier} for name: {file_name}")
    return identifier.__str__()
