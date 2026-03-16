#!/usr/bin/env python3
import asyncio
from shlex import split

from cowsay import cowsay, list_cows

COWS = list_cows()
HELPMSG = """Available commands:
    who                 list online users
    cows                list available cow names
    login COW_NAME      login with the specified cow name
    say COW_NAME MSG    send message to the specified user
    yield MSG           send message to all other users
    quit                disconnect"""
LOGINMSG = """You have to log in in order to use the chat."""

clients = {}
cows = {}


async def chat(reader, writer):
    me = "{}:{}".format(*writer.get_extra_info("peername"))
    print(me)
    clients[me] = asyncio.Queue()
    send = asyncio.create_task(reader.readline())
    receive = asyncio.create_task(clients[me].get())
    while not reader.at_eof():
        done, pending = await asyncio.wait(
            [send, receive], return_when=asyncio.FIRST_COMPLETED
        )
        for q in done:
            if q is send:
                send = asyncio.create_task(reader.readline())
                # parse command
                prompt = split(q.result().decode())
                await exec_cmd(prompt, me, clients)
            elif q is receive:
                receive = asyncio.create_task(clients[me].get())
                writer.write(f"{q.result()}\n".encode())
                await writer.drain()
    send.cancel()
    receive.cancel()
    print(me, "DONE")
    del clients[me]
    if me in cows.keys():
        del cows[me]
    writer.close()
    await writer.wait_closed()


async def exec_cmd(prompt: list[str], who, clients):
    """Run the parsed command."""
    if len(prompt) == 0:
        return
    match prompt[0]:
        case "who":
            for cow in cows.values():
                await clients[who].put(cow)

        case "cows":
            for cow in COWS:
                if cow not in cows.values():
                    await clients[who].put(cow)

        case "login":
            if len(prompt) < 2:
                await clients[who].put(HELPMSG)
                return
            cow = prompt[1]
            if cow in cows.values():
                await clients[who].put(f"Cow {cow} is already taken.")
                return
            cows[who] = cow
            await clients[who].put(f"Logged in as {cow}.")

        case "say":
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

        case "yield":
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

        case "quit":
            print(who, "DONE")
            if who not in cows.keys():
                await clients[who].put("You are not logged in.")
            else:
                del cows[who]
                await clients[who].put("Logged out.")

        case _:
            await clients[who].put(HELPMSG)


async def main():
    server = await asyncio.start_server(chat, "0.0.0.0", 1337)
    async with server:
        await server.serve_forever()


asyncio.run(main())
