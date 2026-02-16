import os
import discord
from discord.ext import commands
from dotenv import load_dotenv

from db import init_db

load_dotenv()

TOKEN = os.getenv("DISCORD_TOKEN")
GUILD_ID = int(os.getenv("GUILD_ID", "0"))
WELCOME_CHANNEL_ID = int(os.getenv("WELCOME_CHANNEL_ID", "0"))

INTENTS = discord.Intents.default()
INTENTS.message_content = True  # benötigt fürs XP-System
INTENTS.members = True          # benötigt fürs Welcome

class ShortlistBot(commands.Bot):
  def __init__(self):
    super().__init__(command_prefix="!", intents=INTENTS)

  async def setup_hook(self):
    await init_db()

    await self.load_extension("cogs.utility")
    await self.load_extension("cogs.moderation")
    await self.load_extension("cogs.leveling")

    # Slash Commands: schneller Sync auf deine Guild (Server)
    if GUILD_ID:
      guild = discord.Object(id=GUILD_ID)
      self.tree.copy_global_to(guild=guild)
      await self.tree.sync(guild=guild)
    else:
      await self.tree.sync()

bot = ShortlistBot()

@bot.event
async def on_ready():
  print(f"✅ Logged in as {bot.user} (id={bot.user.id})")
  await bot.change_presence(
    activity=discord.Activity(type=discord.ActivityType.watching, name="Moderation & Levels")
  )

@bot.event
async def on_member_join(member: discord.Member):
  if not WELCOME_CHANNEL_ID:
    return
  channel = member.guild.get_channel(WELCOME_CHANNEL_ID)
  if channel:
    embed = discord.Embed(
      title="Willkommen!",
      description=f"Hey {member.mention}, willkommen auf **{member.guild.name}** 👋",
    )
    await channel.send(embed=embed)

def main():
  if not TOKEN:
    raise RuntimeError("DISCORD_TOKEN fehlt. Trage ihn in .env ein.")
  bot.run(TOKEN)

if __name__ == "__main__":
  main()
