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
import os
from aioconsole import ainput, aprint
from GamePB import Player, Game
from draw import create_image
from time import time


CLIENTS = set() # set of all websocket connections connected to the server
game = Game() # game needs to be global to be accessible to all games

async def handler(connection):

    # wait for "init" message from client and reply
    message = json.loads(await connection.recv())
    assert message["type"] == "init"

    # respond to initial request to give current info on first connect
    # go through game.stage_display and retrieve the image locations if present
    images = []
    for match in game.stage_display:
        filename = match["image"]
        if filename != "":
            images.append(filename)

    await connection.send(json.dumps({
        "type": "images",
        "images": images
    }))

    CLIENTS.add(connection)
    try:
        await connection.wait_closed()
    finally:
        CLIENTS.remove(connection)

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
            await aprint(f"[EZPB ] Player {player_name} successfully added on team {team_name}.")

        except RuntimeError as e:
            await aprint(f"[EZPB ] Could not add player {player_name} as game is already full.")

async def command_remove_players(args, game=None):
    for player in args:

        return_code = game.remove_player(player)
        if return_code:
            await aprint(f"[EZPB ] Player {player} successfully removed.")
        else:
            await aprint(f"[EZPB ] Failed to remove player {player}.")

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
    await aprint(f"[EZPB ] Player {player.name} successfully changed to team {player.team}.")

async def command_matchmake(args, game=None):
    game.matchmake()

async def command_next(args, game=None):
    # avoids IndexError
    game.current_match = min(game.current_match + 1, len(game.stage_display) - 1)

async def command_send_data(args, game=None):
    """Creates images based on the game.stage_display queue and
    sends them to the JavaScript.
    """

    images = [] # list of strings

    # go through the stage_display queue and create images for each match in queue
    # also set the "image" property in each element of the queue
    for match in game.stage_display:

        if match["image"] == "": # if there is no image for the match yet, create it
            filename = create_image(match, tmp=False, location=f"EZPB-{int(time() * 10000)}.png")
            match["image"] = filename
            game.list_of_images.append(filename)
            await aprint(f"[EZPB ] Image {filename} created.")

        else:
            filename = match["image"]
            # no need to append to list_of_images here because no new image was created

        images.append(filename)

    websockets.broadcast(CLIENTS, json.dumps({
        "type": "images",
        "images": images
    }))

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

        # simple and crude command line interface

        commands = {
            "help": command_help,
            "license": command_license,
            "add_players" : command_add_players,
            "remove_players": command_remove_players,
            "change_team": command_change_team,
            "matchmake": command_matchmake,
            "next": command_next,
            "send_data": command_send_data
        }


        while True:
            command = await ainput("EZPB >> ")
            command = command.split()
            if len(command) < 1:
                continue

            if command[0] == "quit" or command[0] == "exit":

                # clean up image files
                for filename in game.list_of_images:
                    os.remove(filename)
                    await aprint(f"[EZPB ] Image {filename} deleted.")

                break

            try:
                # this calls the function relating to the command
                await commands[command[0]](command[1:], game=game)
            except KeyError:
                await aprint(f"[EZPB ] Command {command[0]} not found.")

if __name__ == "__main__":
    asyncio.run(main())
