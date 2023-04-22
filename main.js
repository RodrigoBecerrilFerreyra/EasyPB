/*
Copyright 2023 Rodrigo Becerril Ferreyra

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
*/

const STAGES = [
    "Scorch Gorge",
    "Eeltail Alley",
    "Hagglefish Market",
    "Undertow Spillway",
    "Mincemeat Metalworks",
    "Hammerhead Bridge",
    "Museum d'Alfonsino",
    "Mahi-Mahi Resort",
    "Inkblot Art Academy",
    "Sturgeon Shipyard",
    "MakoMart",
    "Wahoo World",
    "Brinewater Springs",
    "Flounder Heights",
    "Um'ami Ruins",
    "Manta Maria",
]

const MODES = [
    "Spectator",
    "Recon",
    "Turf War",
    "Splat Zones",
    "Tower Control",
    "Rainmaker",
    "Clam Blitz"
]

window.addEventListener("DOMContentLoaded", function()
{
    // Open the WebSocket connection and register event handlers.
    const websocket = new WebSocket("ws://localhost:8001/");
    websocket.addEventListener("error", function()
    {
        showMessage("It looks like there isn't a PB up right now. Please try again later.")
    });
    receiveMessage(websocket);

    // send message to server to send updated stage data
    // "please send me the latest data" (the data is handled by receiveMessage)
    websocket.addEventListener("open", function()
    {
        websocket.send(JSON.stringify({type: "init"}))
    });
});

function receiveMessage(websocket)
{
    websocket.addEventListener("message", function({data})
    {
        // receive and parse data
        let received = JSON.parse(data);

        if(received.type === "images")
        {

            for(let location of received.images)
            {
                // create the div and image and append it to body
                let div = document.createElement("div");
                div.className = "match-div";
                let image = document.createElement("img")
                image.className = "match-image";
                image.src = location;
                div.append(image);
                document.body.append(div);

                // check if there are more than three divs with class match-div;
                // if so, delete the first one
                let div_matchdiv = document.body.querySelectorAll("div.match-div");
                if(div_matchdiv.length > 3)
                {
                    div_matchdiv[0].remove()
                }
            }
        }
        else if(received.type === "exit")
        {
            showMessage("The PB has ended. Thank you for joining!")
        }
    });
}

function showMessage(message)
{
    window.setTimeout(() => window.alert(message), 50);
}
