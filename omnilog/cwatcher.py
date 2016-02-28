import hashlib
import json
import threading
import time

from omnilog.config import Config


class ConfigWatcher(threading.Thread):
    runner = None

    def __init__(self, config_path, runner, vertical_queue):
        super().__init__()

        self.runner = runner
        self.vertical_queue = vertical_queue
        self.interval_secs = 1
        self.config_path = config_path
        self.last_config_checksum = None

    def set_config(self):

        config_file = open(self.config_path)
        Config.config_dict = json.load(config_file)

    def run(self):

        counter = 0
        print("Started config watcher ...")

        while self.runner.is_set():

            time.sleep(self.interval_secs)
            hash = hashlib.md5(open(self.config_path, 'rb').read()).hexdigest()
            if hash != self.last_config_checksum:
                self.set_config()
                self.last_config_checksum = hash
                if counter != 0:
                    self.vertical_queue.put("RESTART")
                    print("Config changes detected ... setting new config.")
            counter += 1