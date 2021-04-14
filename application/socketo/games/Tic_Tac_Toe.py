import random

Board = {
    "TopL": " ",
    "TopM": " ",
    "TopR": " ",
    "MidL": " ",
    "MidM": " ",
    "MidR": " ",
    "LowL": " ",
    "LowM": " ",
    "LowR": " "
}

def check(x, Board):
#Top Horizontal
    if Board["TopL"] == x and Board["TopM"] == x and Board["TopR"] == x:
        return 1
#Mid Horizontal
    elif Board["MidL"] == x and Board["MidM"] == x and Board["MidR"] == x:
        return 1
#Low Horizontal
    elif Board["LowL"] == x and Board["LowM"] == x and Board["LowR"] == x:
        return 1
    #Left Vertical
    elif Board["TopL"] == x and Board["MidL"] == x and Board["LowL"] == x:
        return 1
    #Middle Vertical
    elif Board["TopM"] == x and Board["MidM"] == x and Board["LowM"] == x:
        return 1
    #Right Vertical
    elif Board["TopR"] == x and Board["MidR"] == x and Board["LowR"] == x:
        return 1
    #Diagonal leftL-rightT
    elif Board["LowL"] == x and Board["MidM"] == x and Board["TopR"] == x:
        return 1
    elif Board["TopL"] == x and Board["MidM"] == x and Board["LowR"] == x:
        return 1
    return 0

def pickX(users):
    return random.choice(users)
