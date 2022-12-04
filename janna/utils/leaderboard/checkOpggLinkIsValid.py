import validators

def checkOpggLinkIsValid(message):
    if not validators.url(message.content.split()[0]):
        return False
    if message.content.startswith("https://euw.op.gg/summoners/euw/"):
        return True
    if message.content.startswith("https://euw.op.gg/summoner/userName="):
        message.content = message.content[len("https://euw.op.gg/summoner/userName="):]
        return True
    if message.content.startswith("https://www.leagueofgraphs.com/fr/summoner/euw/"):
        return True
    return False