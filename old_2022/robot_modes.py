import subprocess

class RobotModes():
    mode_config = {
        "test_rainbow": "test_rainbow.py"
    }

    def __init__(self):
        self.current_process = None

    def is_running(self):
        return self.current_process and self.current_process.returncode is None

    def run(self, mode_name):
        if not self.is_running():
            script = self.mode_config[mode_name]
            self.current_process = subprocess.Popen(["python3", script])
            return True
        return False

    def stop(self):
        if self.is_running():
            self.current_process.send_signal(subprocess.signal.SIGINT)
            self.current_process = None

