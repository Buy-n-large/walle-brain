import os

class BrainConfig:
    ANTHROPIC_API_KEY = os.environ.get("ANTHROPIC_API_KEY", "")
    MODEL             = os.environ.get("WALLE_MODEL", "claude-opus-4-6")
    MAX_TOKENS        = int(os.environ.get("WALLE_MAX_TOKENS", 256))
    # Nombre max de tours de conversation conservés en mémoire
    MAX_HISTORY       = int(os.environ.get("WALLE_MAX_HISTORY", 20))
