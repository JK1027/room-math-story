# --- Global Configuration Settings ---
from scripts.config import paths
from scripts.config import constants

class Settings:
    def __init__(self):
        self.paths = paths
        self.constants = constants

settings = Settings()
