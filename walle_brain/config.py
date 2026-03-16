import os
import sys

def _mcp_command_default() -> str:
    # Cherche walle-mcp dans le même bin que l'interpréteur Python courant
    # (fonctione dans un venv même sans le PATH étendu)
    bin_dir = os.path.dirname(sys.executable)
    candidate = os.path.join(bin_dir, "walle-mcp")
    return candidate if os.path.isfile(candidate) else "walle-mcp"

class BrainConfig:
    ANTHROPIC_API_KEY = os.environ.get("ANTHROPIC_API_KEY", "")
    MODEL             = os.environ.get("WALLE_MODEL", "claude-opus-4-6")
    MAX_TOKENS        = int(os.environ.get("WALLE_MAX_TOKENS", 512))
    MAX_HISTORY       = int(os.environ.get("WALLE_MAX_HISTORY", 20))

    MCP_COMMAND = os.environ.get("WALLE_MCP_COMMAND", _mcp_command_default())
    MCP_ARGS    = []
