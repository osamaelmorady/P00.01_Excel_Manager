import json
import os



def _get_config_path():
    # Windows safe writable location
    base = os.getenv("LOCALAPPDATA") or os.path.expanduser("~")
    folder = os.path.join(base, "ExcelManager")

    os.makedirs(folder, exist_ok=True)

    return os.path.join(folder, "app_state.json")


CONFIG_FILE = _get_config_path()


class AppState:

    @staticmethod
    def save_last_path(path: str):
        with open(CONFIG_FILE, "w") as f:
            json.dump({"last_path": path}, f)

    @staticmethod
    def load_last_path():
        if not os.path.exists(CONFIG_FILE):
            return None

        try:
            with open(CONFIG_FILE) as f:
                return json.load(f).get("last_path")
        except:
            return None



class AppState:

    @staticmethod
    def save_last_path(path: str):
        with open(CONFIG_FILE, "w") as f:
            json.dump({"last_path": path}, f)

    @staticmethod
    def load_last_path():
        if not os.path.exists(CONFIG_FILE):
            return None

        try:
            with open(CONFIG_FILE) as f:
                return json.load(f).get("last_path")
        except:
            return None
