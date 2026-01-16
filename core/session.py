import os, json, datetime

BASE_DIR = "workspaces"

class SessionManager:
    def __init__(self):
        os.makedirs(BASE_DIR, exist_ok=True)

    def create(self, name, target):
        ts = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        path = os.path.join(BASE_DIR, f"{name}_{ts}")

        os.makedirs(path + "/logs", exist_ok=True)
        os.makedirs(path + "/loot", exist_ok=True)

        meta = {
            "name": name,
            "target": target,
            "created": ts
        }

        with open(path + "/meta.json", "w") as f:
            json.dump(meta, f, indent=4)

        with open(path + "/notes.md", "w") as f:
            f.write(f"# Notes for {name}\n")

        return path, meta
