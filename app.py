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
        "add_players" : command_add_players,
        "remove_players": command_remove_players,
        "change_team": command_change_team
    }

    game = Game([])

    while True:
        command = await ainput("EZPB >> ")
        command = command.split()
        if len(command) < 1:
            continue

        if command[0] == "quit" or command[0] == "exit":
            break

        if command[0] not in commands:
            await aprint(f"Command {command} not found.")
            continue

        # this calls the function relating to the command
        await commands[command[0]](command[1:], game=game)

async def command_add_players(args, game=None):
    for player in args:

        try: # this try block tries to find the team name
            equals_sign = player.index("=")
            team = player[equals_sign+1:].upper()
            player_name = player[:equals_sign]
        except ValueError:
            team = "R"
            player_name = player

        if team == "Y":
            team_name = Player.TEAM_YELL
        elif team == "B":
            team_name = Player.TEAM_BLUE
        else:
            team_name = Player.TEAM_RAND

        try: # this try block catches RuntimeError when more than 10 players join
            game.add_player(player_name=player_name, player_team=team_name)
            await aprint(f"Player {player_name} successfully added on team {team_name}.")

        except RuntimeError as e:
            await aprint(f"Could not add player {player_name} as game is already full.")

async def command_remove_players(args, game=None):
    for player in args:

        return_code = game.remove_player(player)
        if return_code:
            await aprint(f"Player {player} successfully removed.")
        else:
            await aprint(f"Failed to remove player {player}.")

async def command_change_team(args, game=None):

    if len(args) != 2:
        return # incorrect syntax

    try:
        player = game.find_player(args[0])
    except LookupError as e:
        await aprint(e)
        return

    team = args[1][0].upper() # the first character in the second argument
    if team == "Y":
        team_name = Player.TEAM_YELL
    elif team == "B":
        team_name = Player.TEAM_BLUE
    else:
        team_name = Player.TEAM_RAND

    player.team = team_name
    await aprint(f"Player {player.name} successfully changed to team {player.team}.")

async def command_help(args, game=None):
    await aprint("Commands:")
    await aprint("help - prints this help message")
    await aprint("license - prints the licensing details")
    await aprint('"quit" or "exit" - end program')

async def command_license(args, game=None):
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
