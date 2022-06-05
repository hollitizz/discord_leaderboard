from discord import Interaction, app_commands
from utils.myTypes import Setup


def checkPerms(self: Setup, ctx: Interaction):
    if ctx.user.id not in self.db.bot_admins:
        raise app_commands.MissingPermissions("Vous n'avez pas les permissions nécessaires pour effectuer cette action !")