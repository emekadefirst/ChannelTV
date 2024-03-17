import asyncio
import threading
from tool.business import business
from tool.entertainment import entertainment
from tool.politics import politics
from tool.sport import sport
from tool.tech import tech
from tool.world import world

while True:
    print("What would you like to scrape from ChannelsTV\n1. Business news\n2. Entertainment news\n3. Politic news\n4. Sport news\n5. Tech news\n6. World news\n7. All")
    response = str(input(">> "))
    if response == "1":
        asyncio.run(business())
    elif response == "2":
        asyncio.run(entertainment())
    elif response == "3":
        asyncio.run(politics())
    elif response == "4":
        asyncio.run(sport())
    elif response == "5":
        asyncio.run(tech())
    elif response == "6":
        asyncio.run(world())
    elif response == "7":
        asyncio.run(world(), business(), business(), entertainment(), politics(), sport(), tech(), world())
    else:
        print("Invalid request")
    break