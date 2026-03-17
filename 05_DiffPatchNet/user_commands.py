from cowsay import cowsay, list_cows

HELPMSG = """Available commands:
    who                 list online users
    cows                list available cow names
    login COW_NAME      login with the specified cow name
    say COW_NAME MSG    send message to the specified user
    yield MSG           send message to all other users
    quit                disconnect"""
LOGINMSG = """You have to log in in order to use the chat."""
COWS = list_cows()


async def who(prompt: list[str], who, clients, cows):
    for cow in cows.values():
        await clients[who].put(cow)


async def cows(prompt: list[str], who, clients, cows):
    for cow in COWS:
        if cow not in cows.values():
            await clients[who].put(cow)


async def login(prompt: list[str], who, clients, cows):
    if len(prompt) < 2:
        await clients[who].put(HELPMSG)
        return
    cow = prompt[1]
    if cow in cows.values():
        await clients[who].put(f"Cow {cow} is already taken.")
        return
    cows[who] = cow
    await clients[who].put(f"Logged in as {cow}.")


async def say(prompt: list[str], who, clients, cows):
    if who not in cows.keys():
        await clients[who].put(LOGINMSG)
        return
    if len(prompt) < 3:
        await clients[who].put(HELPMSG)
        return
    to = prompt[1]
    msg = " ".join(prompt[2:])
    if to in cows.values():
        # get the stream key
        to = list(cows.keys())[list(cows.values()).index(to)]
        await clients[to].put(cowsay(msg, cow=cows[who]))
    else:
        await clients[who].put(f"User not found: {to}")


async def yield_(prompt: list[str], who, clients, cows):
    if who not in cows.keys():
        await clients[who].put(LOGINMSG)
        return
    if len(prompt) < 2:
        await clients[who].put(HELPMSG)
        return
    msg = " ".join(prompt[1:])
    for to in cows.keys():
        if to != who:
            await clients[to].put(cowsay(msg, cow=cows[who]))


async def quit(prompt: list[str], who, clients, cows):
    print(who, "DONE")
    if who not in cows.keys():
        await clients[who].put("You are not logged in.")
    else:
        del cows[who]
        await clients[who].put("Logged out.")


async def help(prompt: list[str], who, clients, cows):
    await clients[who].put(HELPMSG)
