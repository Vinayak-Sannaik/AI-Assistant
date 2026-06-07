import json
from pathlib import Path


class PersistentMemory:

    def __init__(
        self,
        memory_file="memory.json"
    ):
        self.memory_file = Path(memory_file)

        if not self.memory_file.exists():
            self.memory_file.write_text("{}")

    def load(self):
        with open(self.memory_file, "r") as f:
            return json.load(f)

    def save(self, data):
        with open(self.memory_file, "w") as f:
            json.dump(
                data,
                f,
                indent=2
            )

    def set(self, key, value):
        data = self.load()

        data[key] = value

        self.save(data)

    def get(self, key):
        data = self.load()

        return data.get(key)