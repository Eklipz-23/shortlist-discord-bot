import os
import discord
from discord import app_commands
from discord.ext import commands

LOG_CHANNEL_ID = int(os.getenv("LOG_CHANNEL_ID", "0"))

async def log_action(guild: discord.Guild, text: str):
  if not LOG_CHANNEL_ID:
    return
  channel = guild.get_channel(LOG_CHANNEL_ID)
  if channel:
    await channel.send(text)

class Utility(commands.Cog):
  def __init__(self, bot: commands.Bot):
    self.bot = bot

  @app_commands.command(name="ping", description="Check if the bot is alive.")
  async def ping(self, interaction: discord.Interaction):
    await interaction.response.send_message(
      f"Pong! 🏓 Latency: {round(self.bot.latency * 1000)}ms",
      ephemeral=True
    )

  @app_commands.command(name="say", description="Admin announcement as the bot.")
  @app_commands.checks.has_permissions(administrator=True)
  async def say(self, interaction: discord.Interaction, message: str):
    await interaction.response.send_message("✅ Sent.", ephemeral=True)
    await interaction.channel.send(message)
    await log_action(interaction.guild, f"📢 Announcement by {interaction.user.mention}: {message}")

  @say.error
  async def say_error(self, interaction: discord.Interaction, error: app_commands.AppCommandError):
    if isinstance(error, app_commands.MissingPermissions):
      await interaction.response.send_message("❌ Du brauchst Admin-Rechte dafür.", ephemeral=True)
    else:
      await interaction.response.send_message("❌ Fehler.", ephemeral=True)

async def setup(bot: commands.Bot):
  await bot.add_cog(Utility(bot))
