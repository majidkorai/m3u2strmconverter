from os import path, makedirs
from datetime import datetime
from enum import Enum

class LogLevel(Enum):
    OFF = 1
    MINIMUM = 2
    NORMAL = 3
    DEBUG = 4


class Logger(object):
    def __init__(self, full_name, log_level=LogLevel.DEBUG):
        module_name = path.splitext(path.basename(full_name))[0]
        self.log_name = module_name + ".log"
        logs_folder = "logs"
        if not path.exists(logs_folder):
            makedirs(logs_folder, exist_ok=True)

        self.log = path.join(logs_folder, self.log_name)
        self.create_log()

        self.logging_level = log_level

    def create_log(self):
        with open(self.log, mode="w", encoding="utf-8") as log_file:
            log_file.write(self.get_date_time() + "\t\t*** Starting Log ***\n")
        log_file.close()

    def get_date_time(self):
        return datetime.now().strftime("%m-%d-%Y %H:%M:%S")

    def set_logging_level(self, level):
        self.logging_level = level

    def write_to_log(self, msg="", log_level=LogLevel.DEBUG):
        if log_level.value > self.logging_level.value:
            return

        with open(self.log, mode="a", encoding="utf-8") as log_file:
            if msg.startswith("\n"):
                msg = msg[1:]
                log_file.write(self.get_date_time() + "\n")

            msg = f"{log_level.name}: {msg}"
            if msg.endswith("\n"):
                log_file.write(self.get_date_time() + "\t\t" + msg)
                log_file.write(self.get_date_time() + "\n")
            else:
                log_file.write(self.get_date_time() + "\t\t" + msg + "\n")
        log_file.close()
