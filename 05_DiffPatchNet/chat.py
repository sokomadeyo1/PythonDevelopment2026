#!/usr/bin/env python3
import asyncio
from shlex import split

import user_commands

clients = {}
cows = {}
cmds = {
    "who": user_commands.who,
    "cows": user_commands.cows,
    "login": user_commands.login,
    "say": user_commands.say,
    "yield": user_commands.yield_,
    "quit": user_commands.quit,
    "help": user_commands.help
}


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
                await exec_cmd(prompt, me, clients, cows)
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


async def exec_cmd(prompt: list[str], who, clients, cows):
    """Run the parsed command."""
    if len(prompt) == 0:
        return
    cmd = prompt[0]
    if cmd not in cmds.keys():
        await cmds["help"](prompt, who, clients, cows)
        return
    await cmds[cmd](prompt, who, clients, cows)


async def main():
    server = await asyncio.start_server(chat, "0.0.0.0", 1337)
    async with server:
        await server.serve_forever()


asyncio.run(main())
