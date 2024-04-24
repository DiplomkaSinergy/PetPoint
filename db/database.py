# database.py
import aiomysql
from config import MYSQL_USER, MYSQL_PASSWORD, MYSQL_DB, MYSQL_HOST

async def get_connection():
    return await aiomysql.connect(host=MYSQL_HOST, user=MYSQL_USER,
                                  password=MYSQL_PASSWORD, db=MYSQL_DB,
                                  autocommit=True)

async def fetch(query, args=None):
    conn = await get_connection()
    async with conn.cursor(aiomysql.DictCursor) as cur:
        await cur.execute(query, args)
        result = await cur.fetchall()
    conn.close()
    return result

async def execute(query, args=None):
    conn = await get_connection()
    async with conn.cursor() as cur:
        await cur.execute(query, args)
        affected_rows = cur.rowcount
    conn.close()
    return affected_rows


async def create_tables():
    conn = await get_connection()
    try:
        async with conn.cursor() as cursor:
            await cursor.execute("""
                CREATE TABLE IF NOT EXISTS shops (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    name VARCHAR(255),
                    address TEXT
                );
                CREATE TABLE IF NOT EXISTS categories (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    name VARCHAR(255)
                );
                CREATE TABLE IF NOT EXISTS products (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    name VARCHAR(255),
                    description TEXT,
                    category_id INT,
                    price DECIMAL(10, 2),
                    stock INT,
                    FOREIGN KEY (category_id) REFERENCES categories(id)
                );
                CREATE TABLE IF NOT EXISTS orders (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    user_id INT,
                    status VARCHAR(50),
                    total_price DECIMAL(10, 2),
                    pickup_address TEXT
                );
            """)
        await conn.commit()
    finally:
        conn.close()
