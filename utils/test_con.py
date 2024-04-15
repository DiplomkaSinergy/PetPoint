import asyncio
import aiomysql

async def test_connection():
    try:
        conn = await aiomysql.connect(host='127.0.0.1', port=3306, user='root', password='pass', db='db')
        print("Connected successfully!")
        await conn.close()
    except Exception as e:
        print("Failed to connect:", e)

asyncio.run(test_connection())
