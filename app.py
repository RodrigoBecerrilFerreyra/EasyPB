# Copyright 2023 Rodrigo Becerril Ferreyra

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

#     http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import asyncio
import websockets
import json
from aioconsole import ainput, aprint
from GamePB import Player, Game

async def handler(connection):

    # simple and crude command line interface

    commands = {
        "help": command_help,
        "license": command_license,
    }

    while True:
        command = await ainput("EZPB >> ")
        command = command.split()
        if len(command) < 1:
            continue

        if command[0] not in commands:
            await aprint(f"Command {command} not found.")
            continue

        if command[0] == "quit" or command[0] == "exit":
            break

        # this calls the function relating to the command
        await commands[command[0]](command[1:])

async def command_help(args):
    await aprint("Commands:")
    await aprint("help - prints this help message")
    await aprint("license - prints the licensing details")
    await aprint('"quit" or "exit" - end program')

async def command_license(args):
    await aprint("""Copyright 2023 Rodrigo Becerril Ferreyra

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.""")

async def main():
    async with websockets.serve(handler, "", 8001):
        await asyncio.Future()  # run forever

if __name__ == "__main__":
    asyncio.run(main())
