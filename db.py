import aiosqlite

DB_PATH = "bot.db"

CREATE_TABLES_SQL = """
CREATE TABLE IF NOT EXISTS warnings (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  guild_id INTEGER NOT NULL,
  user_id INTEGER NOT NULL,
  moderator_id INTEGER NOT NULL,
  reason TEXT NOT NULL,
  created_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS xp (
  guild_id INTEGER NOT NULL,
  user_id INTEGER NOT NULL,
  xp INTEGER NOT NULL DEFAULT 0,
  level INTEGER NOT NULL DEFAULT 0,
  last_message_ts INTEGER NOT NULL DEFAULT 0,
  PRIMARY KEY (guild_id, user_id)
);
"""

async def init_db() -> None:
  async with aiosqlite.connect(DB_PATH) as db:
    await db.executescript(CREATE_TABLES_SQL)
    await db.commit()

async def add_warning(guild_id: int, user_id: int, moderator_id: int, reason: str, created_at: str) -> int:
  async with aiosqlite.connect(DB_PATH) as db:
    cur = await db.execute(
      "INSERT INTO warnings (guild_id, user_id, moderator_id, reason, created_at) VALUES (?, ?, ?, ?, ?)",
      (guild_id, user_id, moderator_id, reason, created_at),
    )
    await db.commit()
    return cur.lastrowid

async def get_warnings(guild_id: int, user_id: int):
  async with aiosqlite.connect(DB_PATH) as db:
    cur = await db.execute(
      "SELECT id, moderator_id, reason, created_at FROM warnings WHERE guild_id=? AND user_id=? ORDER BY id DESC",
      (guild_id, user_id),
    )
    return await cur.fetchall()

async def upsert_xp(guild_id: int, user_id: int, xp: int, level: int, last_message_ts: int) -> None:
  async with aiosqlite.connect(DB_PATH) as db:
    await db.execute(
      """
      INSERT INTO xp (guild_id, user_id, xp, level, last_message_ts)
      VALUES (?, ?, ?, ?, ?)
      ON CONFLICT(guild_id, user_id) DO UPDATE SET
        xp=excluded.xp, level=excluded.level, last_message_ts=excluded.last_message_ts
      """,
      (guild_id, user_id, xp, level, last_message_ts),
    )
    await db.commit()

async def get_xp(guild_id: int, user_id: int):
  async with aiosqlite.connect(DB_PATH) as db:
    cur = await db.execute(
      "SELECT xp, level, last_message_ts FROM xp WHERE guild_id=? AND user_id=?",
      (guild_id, user_id),
    )
    return await cur.fetchone()

async def get_top_xp(guild_id: int, limit: int = 10):
  async with aiosqlite.connect(DB_PATH) as db:
    cur = await db.execute(
      "SELECT user_id, xp, level FROM xp WHERE guild_id=? ORDER BY level DESC, xp DESC LIMIT ?",
      (guild_id, limit),
    )
    return await cur.fetchall()

