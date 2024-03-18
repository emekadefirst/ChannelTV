import os
import asyncio
import sqlite3
import threading
from tool.business import bus
from tool.entertainment import ent
from tool.politics import pol
from tool.sport import spt
from tool.tech import tec
from tool.world import wrld



reply = str(input("Is this your first time\n1. Yes\n2. No\n>> ")).lower()
if reply == "1" or "yes":
    def create_db():
        db = sqlite3.connect('newsdata.db')
        cursor = db.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS articles (
                        id INTEGER PRIMARY KEY,
                        title TEXT,
                        content TEXT,
                        category TEXT,
                        image TEXT,
                        date_published DATE)''')
        db.commit()  
        return f"{db, cursor} Database has been created so as the table" 

    # Call create_db to establish connection and get cursor
    create_db()

else:
    print('continue')

async def run_tasks(tasks):
    await asyncio.gather(*tasks)

async def main():
    while True:
        print("What would you like to scrape from ChannelsTV\n1. Business news\n2. Entertainment news\n3. Politic news\n4. Sport news\n5. Tech news\n6. World news\n7. All\n8. Exit")
        responses = input("Enter your choices (comma-separated numbers): ").strip().split(',')
        tasks = []
        threads = []

        for response in responses:
            if response == "1":
                tasks.append(bus)
            elif response == "2":
                tasks.append(ent)
            elif response == "3":
                tasks.append(pol)
            elif response == "4":
                tasks.append(spt)
            elif response == "5":
                tasks.append(tec)
            elif response == "6":
                tasks.append(wrld)
            elif response == "7":
                for func in [bus, ent, pol, spt, tec, wrld]:
                    thread = threading.Thread(target=func)
                    threads.append(thread)
                    thread.start()
            elif response == "8":
                # Determine the command based on the operating system
                if os.name == 'nt':  # Windows
                    os.system('cls')
                else:  # Unix/Linux/MacOS
                    os.system('clear')
                return
            else:
                print("Invalid request:", response)
        
        if threads:
            for thread in threads:
                thread.join()
        elif tasks:
            await run_tasks([task() for task in tasks])

# Run the asyncio loop
asyncio.run(main())
