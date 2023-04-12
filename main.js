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
    receiveMessage(websocket);
});

function receiveMessage(websocket)
{
    websocket.addEventListener("message", function({data})
    {
        // receive and parse data
        let received = JSON.parse(data);

        for(let matchnum in received)
        {
            let div = document.createElement("div");
            div.className = "match";

            // create and populate table
            let table = document.createElement("tbody");

            // row 1: stage
            let tr = document.createElement("tr");
            let td = document.createElement("td");
            td.className = "tg-0lax"; // from https://www.tablesgenerator.com
            td.innerText = "Stage:"
            tr.append(td);
            // stage name
            td = document.createElement("td");
            td.className = "tg-0lax";
            td.colSpan = "4";
            td.innerText = STAGES[received[matchnum].stage];
            tr.append(td);
            table.append(tr);

            // row 2: mode
            tr = document.createElement("tr");
            td = document.createElement("td");
            td.className = "tg-0lax";
            td.innerText = "Mode:";
            tr.append(td);
            // mode name
            td = document.createElement("td");
            td.className = "tg-0lax";
            td.colSpan = "4";
            td.innerText = MODES[received[matchnum].mode];
            tr.append(td);
            table.append(tr);

            // row 3: alpha team
            tr = document.createElement("tr");
            td = document.createElement("td");
            td.className = "tg-0lax";
            td.innerText = "Alpha:";
            tr.append(td);
            // names of alpha team players
            for(let i = 0; i < received[matchnum].alpha.length; ++i)
            {
                td = document.createElement("td");
                td.className = "tg-0lax";
                td.innerText = received[matchnum].alpha[i];
                tr.append(td);
            }
            table.append(tr);

            // row 4: bravo team
            tr = document.createElement("tr");
            td = document.createElement("td");
            td.className = "tg-0lax";
            td.innerText = "Bravo:";
            tr.append(td);
            // names of bravo team players
            for(let i = 0; i < received[matchnum].bravo.length; ++i)
            {
                td = document.createElement("td");
                td.className = "tg-0lax";
                td.innerText = received[matchnum].bravo[i];
                tr.append(td);
            }
            table.append(tr);

            // row 5: random team
            tr = document.createElement("tr");
            td = document.createElement("td");
            td.className = "tg-0lax";
            td.innerText = "Random:";
            tr.append(td);
            // names of random team players
            for(let i = 0; i < received[matchnum].random.length; ++i)
            {
                td = document.createElement("td");
                td.className = "tg-0lax";
                td.innerText = received[matchnum].random[i];
                tr.append(td);
            }
            table.append(tr);

            // row 6: spectators
            tr = document.createElement("tr");
            td = document.createElement("td");
            td.className = "tg-0lax";
            td.innerText = "Spectators:";
            tr.append(td);
            // names of spectators
            for(let i = 0; i < received[matchnum].spec.length; ++i)
            {
                td = document.createElement("td");
                td.className = "tg-0lax";
                td.colSpan = "2";
                td.innerText = received[matchnum].spec[i];
                tr.append(td);
            }
            table.append(tr);

            div.append(table);
            document.body.append(div);
        }
    });
}

function showMessage(message)
{
    window.setTimeout(() => window.alert(message), 50);
}
