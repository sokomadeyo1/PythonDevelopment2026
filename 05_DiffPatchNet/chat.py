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
clients = {}


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
    writer.close()
    await writer.wait_closed()


async def exec_cmd(prompt: list[str], who, clients):
    """Run the parsed command."""
    if len(prompt) == 0:
        return
    match prompt[0]:
        case "who":
            await clients[who].put(clients.keys())

        case "cows":
            for cow in COWS:
                if cow not in clients.keys():
                    await clients[who].put(cow)

        case "login":
            pass

        case "say":
            if len(prompt) < 3:
                await clients[who].put(HELPMSG)
                return
            to = prompt[1]
            msg = " ".join(prompt[2:])
            if to in clients.keys():
                await clients[to].put(f"{who} {msg}")
            else:
                await clients[who].put(f"User not found: {to}")

        case "yield":
            if len(prompt) < 2:
                await clients[who].put(HELPMSG)
                return
            msg = " ".join(prompt[1:])
            for to in clients.values():
                if to is not clients[who]:
                    await to.put(f"{who} {msg}")

        case "quit":
            print(who, "DONE")
            del clients[who]

        case _:
            await clients[who].put(HELPMSG)


async def main():
    server = await asyncio.start_server(chat, "0.0.0.0", 1337)
    async with server:
        await server.serve_forever()


asyncio.run(main())
