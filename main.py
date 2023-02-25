import logging.config
import os
import time
import watchdog.observers

from handlers.hadlers import ExcelEventHandler
from settings import settings

if __name__ == "__main__":
    logging.config.dictConfig(settings.LOGGER)
    logger = logging.getLogger(__name__)
    path = os.path.join(settings.PROJECTS_DIR)
    observer = watchdog.observers.Observer()
    excel_event_handler = ExcelEventHandler()
    observer.schedule(excel_event_handler, path=path, recursive=True)
    observer.start()
    try:
        while True:
            # It's not recommended setting a low time interval, as this can consume more processing power on your pc.
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
