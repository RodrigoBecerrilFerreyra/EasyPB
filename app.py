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
import secrets
from aioconsole import ainput, aprint
from GamePB import Player, Game
from draw import create_image
from time import time


CLIENTS = set() # set of all websocket connections connected to the server
game = None # game needs to be global to be accessible to all games

async def handler(connection):

    # wait for "init" message from client and reply
    message = json.loads(await connection.recv())
    assert message["type"] == "init"

    if "join" in event:
        await join(connection, event["join"])
    elif "start" in event:
        await start(connection)
    # else do nothing (shouldn't happen)

async def start(connection):
    """Start a new PB and create a room and control code."""

    # create the new game, generate a room key and control key, and send them
    # both to the client
    # TODO: remove games being global; only one game can run at a time this way

    global game
    game = Game()
    room_key = secrets.token_urlsafe()
    control_key = secrets.token_urlsafe()
    event = {
        "type": "keys",
        "room": room_key,
        "control": control_key
    }
    connection.send(json.dumps(event))

async def join(connection, join_key):
    """Adds the connection to the list if it is not a control client."""

    # TODO: remove games being global; only one game can run at a time this way
    global game
    if join_key == game.room_key:
        # add connection to list and do nothing until it disconnects
        CLIENTS.add(connection)
        try:
            await connection.wait_closed()
        finally:
            await CLIENTS.remove(connection)

    elif join_key == game.control_key:
        # This is where all the logic goes.
        pass

    else:
        event = {
            "type": "error",
            "message": "Join key in URL is neither a room key nor a control key."
        }
        connection.send(json.dumps(event))

async def send_data(args, game=None):
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

async def main():
    async with websockets.serve(handler, "", 8001):
        await asyncio.Future() # run forever

if __name__ == "__main__":
    asyncio.run(main())
