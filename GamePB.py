"""Contains the logic for keeping track of matches and creating new ones automatically."""
# GamePB.py

"""
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
"""

import random
from collections import deque

MODES = {
    "SP": 0, # spectator
    "RC": 1,
    "TW": 2,
    "SZ": 3,
    "TC": 4,
    "RM": 5,
    "CB": 6
}

STAGES = (
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
)

class Player:
    """Describes a player and the team he or she is on."""

    TEAM_RAND = 0
    TEAM_YELL = 1
    TEAM_BLUE = 2

    def __init__(self, name, team=TEAM_RAND, times_spectated=0):
        """Creates a new player.
        
        @param name The player's username.
        @param team The player's preferred team (either TEAM_YELL or TEAM_BLUE) (default: TEAM_RAND).
        @param times_spectated Used in order to add a player in the middle of a PB session.
        """

        self.name = name
        if team not in [TEAM_RAND, TEAM_YELL, TEAM_BLUE]:
            raise ValueError(f"Invalid team {team}, expected TEAM_RAND, TEAM_YELL, or TEAM_BLUE.")
        self.team = team
        self.times_spectated = times_spectated

    def __str__(self):
        return self.name

class Game:
    """Describes the game session, and past and future matches."""

    def __init__(self, players):
        """Creates a new game session.
        
        @param players A list of players that are in the game session.
        """
        self.players = players
        self.history = []
        self.stage_display = deque(maxlen=5)

    def __str__(self):
        """Returns a crude table-like representation of the entire history of the game."""

        retstr = ""

        for game in self.history:
            #players = game["alpha"] + game["bravo"] + game["spec"]
            retstr += f"{STAGES[game['stage']]}\t{game['mode']}\t"
            retstr += f"{' '.join([player.name for player in game['alpha']])}\t"
            retstr += f" | {' '.join([player.name for player in game['bravo']])}\t"
            retstr += f" | {' '.join([player.name for player in game['random']])}\t"
            retstr += f" | {' '.join([player.name for player in game['spec']])}\n"

        return retstr

    def add_match(self, match):
        """Add a match to the history."""
        self.history.append(match)
        self.stage_display.append(match)

    def matchmake(self, force_stage=None, force_mode=None, include_turf=False):
        """Creates a new match according to a set of rules and returns it.

        @param force_stage Supply a stage instead of choosing a random one.
        @param force_mode Supply a mode instead of choosing a random one.
        @param include_turf A boolean to add Turf War to the mode rotation.
        @returns A dictionary with match info.
        """

        last_game = history[-1]

        # choose a stage
        if force_stage is not None:
            if force_stage not in range(len(STAGES)):
                raise ValueError(f"Invalid stage {force_stage} given.")
            stage = force_stage
        else:
            while True:
                stage = random.choice(range(len(STAGES)))
                if stage != last_game["stage"]:
                    break

        # choose a mode
        if force_mode is not None:
            if force_mode not in MODES:
                raise ValueError(f"Invalid mode {force_mode} given.")
            mode = force_mode
        else:
            while True:
                modes = [MODES["SZ"], MODES["TC"], MODES["RM"], MODES["CB"]]
                if include_turf:
                    modes.append(MODES["TW"])
                mode = random.choice(modes)
                if mode != last_game["mode"]:
                    break

        # select players
        # Algorithm:
        # All players in spec last game must go into either alpha or bravo this game
        # (players cannot spectate twice in a row).
        # Of the eight players that are left to spectate, select the two with the
        # lowest amount of games spectated. In in case of a tie, select the two
        # with the highest amount of games played in the mode that was selected above.
        # In case of a tie, choose between them randomly.
        # After choosing the spectators, assign players to preferred teams (player.team).
        # If player does not have a preferred team (Player.TEAM_RAND) then assign randomly.
        alpha_team = []
        bravo_team = []
        random_team = []
        spectators = []

        # choose spectators

        if len(self.players) == 10:
            num_spectators = 2
        else:
            num_spectators = len(self.players) % 2

        # remove players that have spectated last game
        possible_spectators = self.players.copy()
        last_game_spectators = []
        for spectator in last_game["spec"]:
            possible_spectators.remove(spectator)
            last_game_spectators.append(spectator)

        # sort by times spectated
        possible_spectators.sort(key=lambda player: player.times_spectated, reverse=True)

        # add the amount of spectators needed
        for _ in range(num_spectators):
            spectators.append(possible_spectators.pop())
    
        # assign teams
        for player in possible_spectators + last_game_spectators:
            if player.team == Player.TEAM_RAND:
                random_team.append(player)
            elif player.team == Player.TEAM_YELL:
                alpha_team.append(player)
            elif player.TEAM_BLUE:
                bravo_team.append(player)

        return {
            "stage": stage,
            "mode": mode,
            "alpha": alpha_team,
            "bravo": bravo_team,
            "random": random_team,
            "spec": spectators
        }

if __name__ == "__main__":

    pass
