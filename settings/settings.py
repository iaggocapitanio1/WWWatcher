from pathlib import Path
from dotenv import load_dotenv
import os

DEV = False

if DEV:
    load_dotenv()

BASE_DIR = Path(__file__).resolve().parent

CLIENT_ID = os.environ.get("CLIENT_ID", "")

CLIENT_SECRET = os.environ.get("CLIENT_SECRET", "")

TOKEN_URL = os.environ.get("TOKEN_URL", "http://woodwork4.ddns.net:3005/oauth2/token")

WW4_GET_CUSTOMER_URL = os.environ.get("WW4_GET_CUSTOMER_URL", "")

PROJECTS_DIR = os.environ.get("PROJECTS_DIR", "")

ORION_HOST = os.environ.get("ORION_HOST", "")

NGSI_LD_CONTEXT = os.environ.get("NGSI_LD_CONTEXT", False)

ORION_HEADERS = {
    'Content-Type': 'application/json',
    'Fiware-Service': 'woodwork40',
    'Link': f'<{NGSI_LD_CONTEXT}>; rel="http://www.w3.org/ns/json-ld#context;type="application/ld+json"'

}

EXCEL_PATTERN = {
    "panels": {
        "columns": [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21],
        "sheet_name": [6]
    },
    "compact-panels": {
        "columns": [0, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14],

        "sheet_name": [9]
    },
    "accessories": {
        "columns": [0, 2, 3, 4],
        "sheet_name": [7]
    }
}
LOGGER = {
    "version": 1,
    "formatters": {
        "simple": {
            "format": "%(asctime)s - level: %(levelname)s - loc: %(name)s - func: %(funcName)s - msg: %(message)s"
        }
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "level": "INFO",
            "formatter": "simple",
            "stream": "ext://sys.stdout"
        },
        "file": {
            "class": "logging.handlers.RotatingFileHandler",
            "filename": "logs/watchdog.log",
            "level": "DEBUG",
            "maxBytes": 1048574,
            "backupCount": 3,
            "formatter": "simple"
        }
    },
    "loggers": {
        "handlers.core.payload": {
            "level": "DEBUG",
            "handlers": [
                "console",
                "file"
            ],
            "propagate": True
        },
        "handlers.core.excel": {
            "level": "DEBUG",
            "handlers": [
                "console",
                "file"
            ],
            "propagate": True
        },
        "handlers.core.utilities": {
            "level": "DEBUG",
            "handlers": [
                "console",
                "file"
            ],
            "propagate": True
        },
        "handlers.functions": {
            "level": "DEBUG",
            "handlers": [
                "console",
                "file"
            ],
            "propagate": True
        },
        "handlers.handlers": {
            "level": "DEBUG",
            "handlers": [
                "console",
                "file"
            ],
            "propagate": True
        },
        "__main__": {
            "level": "DEBUG",
            "handlers": [
                "console",
                "file"
            ],
            "propagate": True
        }
    },
    "root": {
        "level": "DEBUG",
        "handlers": [
            "console", "file"
        ],
    }
}
