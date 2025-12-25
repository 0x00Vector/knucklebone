import d20
import discord
from discord import app_commands
from discord.ext import commands

class General(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @app_commands.command(name="ping", description="Health check.")
    async def ping(self, interaction: discord.Interaction) -> None:
        await interaction.response.send_message("pong 🦴")

    @app_commands.command(name="roll", description="Roll dice (e.g. 1d20+2, 4d6kh3).")
    @app_commands.describe(expr="Dice expression")
    async def roll(self, interaction: discord.Interaction, expr: str) -> None:
        try:
            result = d20.roll(expr)
        except Exception as e:
            return await interaction.response.send_message(
                f"Couldn’t parse that roll: `{expr}`\nError: `{e}`",
                ephemeral=True,
            )

        await interaction.response.send_message(
            f"🎲 `{expr}` → **{result.total}**\n{result.result}"
        )

async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(General(bot))