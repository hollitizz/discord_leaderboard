async def checkPlayerExist(users, tag):
    i = 0

    for i in range(len(users)):
        if (users[i][0].replace('!', '') == tag):
            return i
    return -1