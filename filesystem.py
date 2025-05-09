import os
import json
from datetime import datetime, date

_default_config_directory = os.getcwd() + "\\config.json"
_default_history_directory = os.getcwd() + "\\history"
_default_log_directory = os.getcwd() + "\\logs"

class DateTimeEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, date):
            return obj.isoformat()  # Convert date to a string in ISO 8601 format
        return super().default(obj)


def load_config(path=_default_config_directory):
    with open(path, "r") as config_json:
        return json.load(config_json)

def log_ChatSession(ChatSession, id, path=_default_history_directory):
    data = repr(ChatSession.history)
    log_file_name = f"session_{id}.txt"
    with open(path + "\\" + log_file_name, "w") as log_file:
        log_file.write(data)

def log_app(message, severity="info", path=_default_log_directory):  # takes in discord class Message
    severity = severity.lower()
    valid_severities = ["info", "warning", "error"]
    if severity not in valid_severities:
        severity = "info"
    current_datetime = datetime.now()
    timestamp = "[{}]".format(current_datetime.strftime("%Y-%m-%d %H:%M:%S"))

    if severity == "info":
        data = f"{timestamp} [INFO] {message}"
    elif severity == "warning":
        data = f"{timestamp} [WARNING] {message}"
    elif severity == "error":
        data = f"{timestamp} [ERROR] {message}"
    
    log_file_name = f"log_{current_datetime.date()}.txt"

    with open(_default_log_directory + "\\" + log_file_name, "a") as log_file:
        log_file.write(data)

#UNUSED----------------------------------------------------------------
def log_discord_message(message, path=_default_history_directory):  # takes in discord class Message
    current_datetime = datetime.now()
    log_file_name = f"discord_{message.channel.id}.txt"
    xml_data = repr(message)
    data = {
    "time": current_datetime,
    "xml": xml_data,
    "msg": message.content
    }
    with open(path + "\\" + log_file_name, "a") as log_file:
        log_file.write(json.dumps(data, cls=DateTimeEncoder, indent=2))
#UNUSED----------------------------------------------------------------

config = load_config()
