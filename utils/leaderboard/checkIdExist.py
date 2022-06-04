from myTypes import userList

async def checkIdExist(users: userList, tag: str):
    for i, user in enumerate(users):
        if (user.tag.replace('!', '') == tag):
            return i
    return -1