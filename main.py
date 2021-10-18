from core.gui import Window
import logging.config
from log_code.log_config import config


info_logger = logging.getLogger('info_log')
logging.config.dictConfig(config)


def main_start():
    info_logger.info("Start")
    window = Window()
    window.mainloop()
    info_logger.info("End")


if __name__ == "__main__":
    main_start()
