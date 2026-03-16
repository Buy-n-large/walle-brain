import re
import anthropic
from .config import BrainConfig
from .persona import SYSTEM_PROMPT


class WalleBrain:
    """Cerveau IA de WALL-E — conversation via Claude API avec mémoire de session."""

    def __init__(self):
        self._client  = anthropic.Anthropic(api_key=BrainConfig.ANTHROPIC_API_KEY)
        self._history = []  # [{"role": "user"|"assistant", "content": str}]

    def think(self, user_input: str) -> tuple[str, list[dict]]:
        """
        Envoie un message à WALL-E et retourne (réponse_texte, commandes).

        commandes : liste de dicts {"type": "LED"|"SERVO"|"STEPPER", "args": [...]}
        """
        self._history.append({"role": "user", "content": user_input})
        self._trim_history()

        response = self._client.messages.create(
            model=BrainConfig.MODEL,
            max_tokens=BrainConfig.MAX_TOKENS,
            system=SYSTEM_PROMPT,
            messages=self._history,
        )

        reply = response.content[0].text
        self._history.append({"role": "assistant", "content": reply})

        commands = self._parse_commands(reply)
        clean    = self._strip_commands(reply)

        return clean, commands

    def reset(self):
        self._history.clear()

    # ------------------------------------------------------------------ #

    def _trim_history(self):
        max_pairs = BrainConfig.MAX_HISTORY
        if len(self._history) > max_pairs * 2:
            self._history = self._history[-(max_pairs * 2):]

    _CMD_RE = re.compile(
        r'\[(LED\s+\d+\s+\d+\s+\d+|SERVO\s+\d+|STEPPER\s+-?\d+)\]'
    )

    def _parse_commands(self, text: str) -> list[dict]:
        commands = []
        for match in self._CMD_RE.finditer(text):
            parts = match.group(1).split()
            cmd_type = parts[0]
            args = [int(x) for x in parts[1:]]
            commands.append({"type": cmd_type, "args": args})
        return commands

    def _strip_commands(self, text: str) -> str:
        return self._CMD_RE.sub("", text).strip()
