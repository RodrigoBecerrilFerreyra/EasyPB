#!/bin/env python3

from PIL import Image, ImageDraw, ImageFont
from time import time

STAGES = (
    "800px-S3_Stage_Scorch_Gorge.png",
    "800px-S3_Stage_Eeltail_Alley.png",
    "800px-S3_Stage_Hagglefish_Market.png",
    "800px-S3_Stage_Undertow_Spillway.png",
    "800px-S3_Stage_Mincemeat_Metalworks.png",
    "800px-S3_Stage_Hammerhead_Bridge.png",
    "800px-S3_Stage_Museum_d'Alfonsino.png",
    "S3_Stage_Mahi-Mahi_Resort.png",
    "800px-S3_Stage_Inkblot_Art_Academy.png",
    "800px-S3_Stage_Sturgeon_Shipyard.png",
    "800px-S3_Stage_MakoMart.png",
    "800px-S3_Stage_Wahoo_World.png",
    "S3_Stage_Brinewater_Springs.png",
    "S3_Stage_Flounder_Heights.png",
    "S3_Stage_Um'ami_Ruins.png",
    "S3_Stage_Manta_Maria.png",
    "S3_Stage_Not_Found.png"
)

# starts at 2 because 0 is spectator and 1 is recon mode
MODES = {
    2: "S3_Badge_Turf_War_50.png",
    3: "S3_icon_Splat_Zones.png",
    4: "S3_icon_Tower_Control.png",
    5: "S3_icon_Rainmaker.png",
    6: "S3_icon_Clam_Blitz.png"
}


def create_image(match, whole_image=False, tmp=True, location=""):
    """Creates an image describing the match and returns a string containing the
    location of the image on storage.

    @param match The match to be described.
    @param whole_image Return the Image object itself instead of saving the image
    into storage.
    @param tmp If whole_image is False, save the image into the OS's temporary
    directory.
    @location if tmp is False, save the image here instead of the temp directory.
    """

    # open all necessary objects
    stage = Image.open(f"./assets/Stages/{STAGES[match['stage']]}")
    mode = Image.open(f"./assets/Icons/Modes/{MODES[match['mode']]}")
    background = Image.open("./assets/Background.png")
    grey = Image.open("./assets/Playercards/inkswirl_grey.png")
    blue = Image.open("./assets/Playercards/inkswirl_blue.png")
    yell = Image.open("./assets/Playercards/inkswirl_yellow.png")
    purp = Image.open("./assets/Playercards/inkswirl_purple.png")
    font = ImageFont.truetype("./assets/Splatfont2.ttf", size=50)
    draw = ImageDraw.Draw(background)

    # add the stage and the mode
    background.paste(stage, (50, 50))
    background.paste(mode, (50, 50), mask=mode)

    # make the nameplates and write the names in
    # Explanation of numbers:
    #   h = 503 is the amount of vertical space taken by the stage + mode + 3px
    #   75 is 150/2 -> 150 is 900-750 -> 900 is the width of the background and
    #     750 is the width of the playercard. In short, 75 keeps the playercard centered.
    #   105 = 75+30 -> 30 is the radius of the rounded corners of each playercard.
    #   (h+h+100)//2 is the center of the playercard. The card in question starts at
    #     h, and the next playercard starts at h + 100
    #   h += 100 -> each playercard has a separation of 100

    h = 503
    for player in match["alpha"]:

        # this checks to see if player is a string. If it is, use it as is.
        # If not (if it's a Player object), use player.name instead.
        player_name = player.name if not isinstance(player, str) else player
        background.paste(yell, (75, h))
        draw.text((105, (h + h + 100)//2), player_name, anchor="lm", font=font)
        h += 100

    for player in match["bravo"]:

        player_name = player.name if not isinstance(player, str) else player
        background.paste(blue, (75, h))
        draw.text((105, (h + h + 100)//2), player_name, anchor="lm", font=font)
        h += 100

    for player in match["random"]:

        player_name = player.name if not isinstance(player, str) else player
        background.paste(purp, (75, h))
        draw.text((105, (h + h + 100)//2), player_name, anchor="lm", font=font)
        h += 100

    for player in match["spec"]:

        player_name = player.name if not isinstance(player, str) else player
        background.paste(grey, (75, h))
        draw.text((105, (h + h + 100)//2), player_name, anchor="lm", font=font)
        h += 100

    if whole_image:
        return background

    if tmp:
        filename = f"/tmp/EZPB-{int(time()*1000)}.png"
        background.save(filename)
        return filename
    else:
        background.save(location)
        return location

if __name__ == "__main__":

    pass
