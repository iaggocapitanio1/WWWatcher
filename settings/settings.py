from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

CLIENT_ID = "b33ed854-1682-4d41-a035-4b7be543790b"

CLIENT_SECRET = "7e60884d-8cb9-4795-9584-8af8b807916c"

TOKEN_URL = "http://woodwork4.ddns.net:3005/oauth2/token"

PROJECTS_DIR = "/home/iaggo/Documents/ProjectsEins/WWWatcher/Projects"

ORION_HOST = "http://woodwork4.ddns.net:1027"

NGSI_LD_CONTEXT = "http://woodwork4.ddns.net:80/context/ww4zero.context-ngsi.jsonld"

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
        "handlers.core.excel.utilities": {
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
