import asyncio
import anthropic
from anthropic.lib.tools.mcp import async_mcp_tool
from mcp import ClientSession
from mcp.client.stdio import stdio_client, StdioServerParameters

from .config import BrainConfig
from .persona import SYSTEM_PROMPT


class WalleBrain:
    """Cerveau IA de WALL-E — Claude + outils MCP pour contrôler le hardware."""

    def __init__(self):
        self._client  = anthropic.AsyncAnthropic(api_key=BrainConfig.ANTHROPIC_API_KEY)
        self._history = []

    def think(self, user_input: str) -> str:
        """Sync wrapper pour Flask — exécute la boucle async."""
        return asyncio.run(self._think_async(user_input))

    async def _think_async(self, user_input: str) -> str:
        self._history.append({"role": "user", "content": user_input})
        self._trim_history()

        server_params = StdioServerParameters(
            command=BrainConfig.MCP_COMMAND,
            args=BrainConfig.MCP_ARGS,
        )

        async with stdio_client(server_params) as (read, write):
            async with ClientSession(read, write) as mcp_client:
                await mcp_client.initialize()

                tools_result = await mcp_client.list_tools()
                mcp_tools = [async_mcp_tool(t, mcp_client) for t in tools_result.tools]

                # Le tool runner gère la boucle outil → réponse automatiquement
                runner = self._client.beta.messages.tool_runner(
                    model=BrainConfig.MODEL,
                    max_tokens=BrainConfig.MAX_TOKENS,
                    system=SYSTEM_PROMPT,
                    tools=mcp_tools,
                    messages=self._history,
                )

                last_message = None
                async for message in runner:
                    last_message = message

        reply = next(
            (b.text for b in last_message.content if b.type == "text"), "…"
        )
        self._history.append({"role": "assistant", "content": reply})
        self._trim_history()
        return reply

    def reset(self):
        self._history.clear()

    def _trim_history(self):
        if len(self._history) > BrainConfig.MAX_HISTORY * 2:
            self._history = self._history[-(BrainConfig.MAX_HISTORY * 2):]
