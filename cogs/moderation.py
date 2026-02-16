import discord
from discord import app_commands
from discord.ext import commands
from datetime import datetime, timezone, timedelta

from db import add_warning, get_warnings
from cogs.utility import log_action

class Moderation(commands.Cog):
  def __init__(self, bot: commands.Bot):
    self.bot = bot

  @app_commands.command(name="warn", description="Warn a user (stored in DB).")
  @app_commands.checks.has_permissions(moderate_members=True)
  async def warn(self, interaction: discord.Interaction, user: discord.Member, reason: str):
    created_at = datetime.now(timezone.utc).isoformat()
    wid = await add_warning(interaction.guild_id, user.id, interaction.user.id, reason, created_at)

    embed = discord.Embed(title="⚠️ Warning issued", description=f"{user.mention} wurde verwarnt.")
    embed.add_field(name="Reason", value=reason, inline=False)
    embed.set_footer(text=f"Warning ID: {wid}")

    await interaction.response.send_message(embed=embed, ephemeral=True)
    await log_action(interaction.guild, f"⚠️ Warn #{wid}: {user.mention} by {interaction.user.mention} — {reason}")

  @app_commands.command(name="warnings", description="Show warnings of a user.")
  @app_commands.checks.has_permissions(moderate_members=True)
  async def warnings(self, interaction: discord.Interaction, user: discord.Member):
    rows = await get_warnings(interaction.guild_id, user.id)
    if not rows:
      await interaction.response.send_message(f"✅ {user.mention} hat keine Warnings.", ephemeral=True)
      return

    embed = discord.Embed(title=f"⚠️ Warnings für {user}", description=f"Anzahl: {len(rows)}")
    for (wid, mod_id, reason, created_at) in rows[:8]:
      embed.add_field(
        name=f"#{wid} — {created_at.split('T')[0]}",
        value=f"Moderator: <@{mod_id}>\nGrund: {reason}",
        inline=False,
      )

    await interaction.response.send_message(embed=embed, ephemeral=True)

  @app_commands.command(name="mute", description="Timeout a user for x minutes.")
  @app_commands.checks.has_permissions(moderate_members=True)
  async def mute(
      self,
      interaction: discord.Interaction,
      user: discord.Member,
      minutes: app_commands.Range[int, 1, 10080],
      reason: str = "No reason"
  ):
    until = datetime.now(timezone.utc) + timedelta(minutes=minutes)
    await user.timeout(until, reason=reason)

    await interaction.response.send_message(
      f"🔇 {user.mention} gemutet für {minutes} Minuten. Grund: {reason}",
      ephemeral=True
    )
    await log_action(interaction.guild, f"🔇 Timeout: {user.mention} by {interaction.user.mention} — {minutes}min — {reason}")

  @app_commands.command(name="unmute", description="Remove timeout from a user.")
  @app_commands.checks.has_permissions(moderate_members=True)
  async def unmute(self, interaction: discord.Interaction, user: discord.Member):
    await user.timeout(None)
    await interaction.response.send_message(f"🔊 {user.mention} ist wieder unmuted.", ephemeral=True)
    await log_action(interaction.guild, f"🔊 Untimeout: {user.mention} by {interaction.user.mention}")

async def setup(bot: commands.Bot):
  await bot.add_cog(Moderation(bot))
