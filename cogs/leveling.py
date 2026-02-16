import time
import discord
from discord import app_commands
from discord.ext import commands

from db import get_xp, upsert_xp, get_top_xp

def xp_for_next_level(level: int) -> int:
  return 50 + level * 25

class Leveling(commands.Cog):
  def __init__(self, bot: commands.Bot):
    self.bot = bot

  @commands.Cog.listener()
  async def on_message(self, message: discord.Message):
    if message.author.bot or not message.guild:
      return

    now = int(time.time())
    row = await get_xp(message.guild.id, message.author.id)
    if row:
      xp, level, last_ts = row
    else:
      xp, level, last_ts = 0, 0, 0

    # Anti-spam cooldown (30s)
    if now - last_ts < 30:
      return

    xp += 10
    last_ts = now

    leveled_up = False
    while xp >= xp_for_next_level(level):
      xp -= xp_for_next_level(level)
      level += 1
      leveled_up = True

    await upsert_xp(message.guild.id, message.author.id, xp, level, last_ts)

    if leveled_up:
      try:
        await message.channel.send(f"🎉 {message.author.mention} ist jetzt **Level {level}**!")
      except discord.Forbidden:
        pass

  @app_commands.command(name="rank", description="Show your rank.")
  async def rank(self, interaction: discord.Interaction, user: discord.Member | None = None):
    user = user or interaction.user
    row = await get_xp(interaction.guild_id, user.id)
    if not row:
      await interaction.response.send_message(f"{user.mention} hat noch keine XP.", ephemeral=True)
      return
    xp, level, _ = row
    need = xp_for_next_level(level)
    await interaction.response.send_message(f"🏅 {user.mention}: Level **{level}** — XP **{xp}/{need}**", ephemeral=True)

  @app_commands.command(name="leaderboard", description="Top users by level.")
  async def leaderboard(self, interaction: discord.Interaction):
    top = await get_top_xp(interaction.guild_id, limit=10)
    if not top:
      await interaction.response.send_message("Noch keine Daten.", ephemeral=True)
      return

    lines = []
    for i, (user_id, xp, level) in enumerate(top, start=1):
      lines.append(f"**{i}.** <@{user_id}> — Level **{level}** (XP {xp})")

    embed = discord.Embed(title="🏆 Leaderboard", description="\n".join(lines))
    await interaction.response.send_message(embed=embed, ephemeral=True)

async def setup(bot: commands.Bot):
  await bot.add_cog(Leveling(bot))
