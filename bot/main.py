import os
import discord
from discord.ext import commands

from bot.db import Database

TOKEN = os.getenv("DISCORD_TOKEN")
GUILD_ID = os.getenv("GUILD_ID")

class KnuckleboneBot(commands.Bot):
    def __init__(self) -> None:
        # commands.Bot is a subclass of discord.Client that supports Cogs
        super().__init__(
            command_prefix="!", # Prefix is required but we primarily use slash commands
            intents=discord.Intents.default(),
            help_command=None
        )
        self.db = Database()

    async def setup_hook(self) -> None:
        await self.db.connect()
        print(f"DB ready at {os.getenv('DB_PATH', '/app/data/bot.db')}")

        # Load Extensions (Cogs)
        # We manually list them here, or could iterate the directory
        initial_extensions = [
            "bot.cogs.general",
            "bot.cogs.morkborg",
        ]

        for ext in initial_extensions:
            try:
                await self.load_extension(ext)
                print(f"Loaded extension: {ext}")
            except Exception as e:
                print(f"Failed to load extension {ext}: {e}")

        # Sync commands
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

@bot.event
async def on_ready() -> None:
    print(f"Logged in as {bot.user} (id={bot.user.id})")

if __name__ == "__main__":
    if not TOKEN:
        raise RuntimeError("DISCORD_TOKEN is not set (check your .env)")
    bot.run(TOKEN)