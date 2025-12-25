import d20
import discord
from discord import app_commands
from discord.ext import commands


class MorkBorg(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @app_commands.command(name="mb", description="Mörk Borg ability check.")
    @app_commands.describe(modifier="Your ability score modifier (e.g. +2, -1)")
    async def mb_check(self, interaction: discord.Interaction, modifier: int) -> None:
        # Construct the dice expression
        # d20 uses standard notation. We need to handle signs for the string representation nicely.
        mod_str = f"{modifier:+}" if modifier else ""  # e.g., "+2", "-1", or ""
        expression = f"1d20{mod_str}"

        result = d20.roll(expression)

        is_crit = result.crit == d20.CritType.CRIT
        is_fumble = result.crit == d20.CritType.FAIL

        outcome = None
        color = discord.Color.light_grey()

        if is_crit:
            outcome = "**CRITICAL SUCCESS!** (Natural 20)"
            color = discord.Color.gold()
        elif is_fumble:
            outcome = "**FUMBLE!** (Natural 1)"
            color = discord.Color.dark_red()

        embed = discord.Embed(title="Mörk Borg Check", color=color)
        embed.add_field(name="Roll", value=f"{result.result}", inline=True)
        embed.add_field(name="Total", value=f"**{result.total}**", inline=True)

        if outcome:
            embed.add_field(name="Result", value=outcome, inline=False)

        await interaction.response.send_message(embed=embed)


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(MorkBorg(bot))
