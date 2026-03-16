import os
import sys

class BrainConfig:
    ANTHROPIC_API_KEY = os.environ.get("ANTHROPIC_API_KEY", "")
    MODEL             = os.environ.get("WALLE_MODEL", "claude-opus-4-6")
    MAX_TOKENS        = int(os.environ.get("WALLE_MAX_TOKENS", 512))
    MAX_HISTORY       = int(os.environ.get("WALLE_MAX_HISTORY", 20))

    # Commande pour démarrer le serveur MCP walle-mcp
    MCP_COMMAND = os.environ.get("WALLE_MCP_COMMAND", "walle-mcp")
    MCP_ARGS    = []
