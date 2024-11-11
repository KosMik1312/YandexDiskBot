import aiosqlite


async def create_database():
    conn = await aiosqlite.connect('db/telegram_commands.db')
    # Create the table here, if it doesn't exist
    await conn.execute('''\
        CREATE TABLE IF NOT EXISTS telegram_commands (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            command TEXT NOT NULL,
            timestamp TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    await conn.commit()
    return conn
