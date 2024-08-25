from flask import Flask
from robot_modes import RobotModes

app = Flask(__name__)
mode_manager = RobotModes()

@app.route("/run/<mode_name>", methods=['POST'])
def run(mode_name):
    mode_manager.run(mode_name)
    return "%s running"

@app.route("/stop", methods=['POST'])
def stop():
    mode_manager.stop()
    return "Stopped"

app.run(host="0.0.0.0", debug=True)