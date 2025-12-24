import d20
import discord
from discord import app_commands
from discord.ext import commands

class MorkBorg(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @app_commands.command(name="mb", description="Mörk Borg ability check (DR 12 by default).")
    @app_commands.describe(modifier="Your ability score modifier (e.g. +2, -1)", dr="Difficulty Rating (default 12)")
    async def mb_check(self, interaction: discord.Interaction, modifier: int, dr: int = 12) -> None:
        # Construct the dice expression
        # d20 uses standard notation. We need to handle signs for the string representation nicely.
        mod_str = f"{modifier:+}" if modifier else "" # e.g., "+2", "-1", or ""
        expression = f"1d20{mod_str}"

        result = d20.roll(expression)
        
        # d20 objects: result.total is the sum, result.crit/result.fumble verify nat 20/1
        # In d20 library, crit/fumble are determined by the dice config, default 20/1.
        # We can check the dice directly to be sure.
        die_val = result.dice[0].values[0] # Gets the value of the first die rolled

        outcome = ""
        color = discord.Color.light_grey()

        if die_val == 20:
            outcome = "**CRITICAL SUCCESS!** (Natural 20)"
            color = discord.Color.gold()
        elif die_val == 1:
            outcome = "**FUMBLE!** (Natural 1)"
            color = discord.Color.dark_red()
        elif result.total >= dr:
            outcome = "SUCCESS"
            color = discord.Color.green()
        else:
            outcome = "FAILURE"
            color = discord.Color.red()

        embed = discord.Embed(title="Mörk Borg Check", color=color)
        embed.add_field(name="Roll", value=f"{result.result}", inline=True)
        embed.add_field(name="DR", value=f"{dr}", inline=True)
        embed.add_field(name="Result", value=outcome, inline=False)

        await interaction.response.send_message(embed=embed)

async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(MorkBorg(bot))
