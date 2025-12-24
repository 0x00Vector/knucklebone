import os

import d20
import discord
from discord import app_commands

from bot.db import Database

TOKEN = os.getenv("DISCORD_TOKEN")
GUILD_ID = os.getenv("GUILD_ID")  # optional (recommended for dev)


class KnuckleboneBot(discord.Client):
    def __init__(self) -> None:
        super().__init__(intents=discord.Intents.default())
        self.tree = app_commands.CommandTree(self)
        self.db = Database()

    async def setup_hook(self) -> None:
        await self.db.connect()
        print(f"DB ready at {os.getenv('DB_PATH', '/app/data/bot.db')}")

        # Dev guild sync is fast; global sync can take a while to show up
        if GUILD_ID:
            guild = discord.Object(id=int(GUILD_ID))
            self.tree.copy_global_to(guild=guild)
            await self.tree.sync(guild=guild)
            print(f"Commands synced to guild {GUILD_ID}")
        else:
            await self.tree.sync()
            print("Commands synced globally")

    async def close(self) -> None:
        await self.db.close()
        await super().close()


bot = KnuckleboneBot()


@bot.tree.command(name="ping", description="Health check.")
async def ping(interaction: discord.Interaction) -> None:
    await interaction.response.send_message("pong 🦴")


@bot.tree.command(name="roll", description="Roll dice (e.g. 1d20+2, 4d6kh3).")
@app_commands.describe(expr="Dice expression")
async def roll(interaction: discord.Interaction, expr: str) -> None:
    try:
        result = d20.roll(expr)
    except Exception as e:
        return await interaction.response.send_message(
            f"Couldn’t parse that roll: `{expr}`\nError: `{e}`",
            ephemeral=True,
        )

    # result.result is a human-readable breakdown, result.total is the numeric total
    await interaction.response.send_message(
        f"🎲 `{expr}` → **{result.total}**\n{result.result}"
    )


@bot.event
async def on_ready() -> None:
    print(f"Logged in as {bot.user} (id={bot.user.id})")


if not TOKEN:
    raise RuntimeError("DISCORD_TOKEN is not set (check your .env)")

bot.run(TOKEN)
