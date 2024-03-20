import os
import asyncio
import aiosqlite
from tool.business import bus
from tool.entertainment import ent
from tool.politics import pol
from tool.sport import spt
from tool.tech import tec
from tool.world import wrld

async def create_db():
    db = await aiosqlite.connect('newsdata.db', isolation_level=None)
    cursor = await db.cursor()
    await cursor.execute('''CREATE TABLE IF NOT EXISTS articles (
                    id INTEGER PRIMARY KEY,
                    title TEXT,
                    content TEXT,
                    category TEXT,
                    image TEXT,
                    date_published DATE)''')
    await db.commit()  
    return db, cursor

async def run_tasks(tasks):
    await asyncio.gather(*tasks)

async def main():
    reply = input("Is this your first time?\n1. Yes\n2. No\n>> ").lower()
    if reply == "1" or reply == "yes":
        await create_db()
    else:
        print('Continue')

    while True:
        print("What would you like to scrape from ChannelsTV\n1. Business news\n2. Entertainment news\n3. Political news\n4. Sport news\n5. Tech news\n6. World news\n7. All\n8. Exit")
        responses = input("Enter your choices (comma-separated numbers): ").strip().split(',')
        tasks = []

        for response in responses:
            if response == "1":
                tasks.append(bus())
            elif response == "2":
                tasks.append(ent())
            elif response == "3":
                tasks.append(pol())
            elif response == "4":
                tasks.append(spt())
            elif response == "5":
                tasks.append(tec())
            elif response == "6":
                tasks.append(wrld())
            elif response == "7":
                tasks.extend([bus(), ent(), pol(), spt(), tec(), wrld()])
            elif response == "8":
                # Determine the command based on the operating system
                if os.name == 'nt':  # Windows
                    os.system('cls')
                else:  # Unix/Linux/MacOS
                    os.system('clear')
                return
            else:
                print("Invalid request:", response)
        
        if tasks:
            await run_tasks(tasks)

# Run the asyncio loop
asyncio.run(main())
