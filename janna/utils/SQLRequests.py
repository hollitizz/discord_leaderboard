from collections import Counter
from mysql.connector import MySQLConnection
from mysql.connector.connection import CursorBase
import os


class AlreadyExists(Exception):
    pass


class SQLRequests(MySQLConnection):
    def __init__(self):
        super().__init__(
            host=os.getenv('DB_HOST'),
            user=os.getenv('DB_USER'),
            password=os.getenv('DB_PASS'),
            database=os.getenv('DB_NAME')
        )
        self.__cursor: CursorBase = self.cursor()

    def __clearCache(self):
        self.connect()
        try:
            self.__cursor.fetchall()
        except:
            pass

    def getTables(self) -> 'list[str]':
        self.__clearCache()
        self.__cursor.execute("SHOW TABLES")
        return self.__cursor.fetchall()

    def getLeagueMainAccountNameFromUserId(self, user_id: int) -> str:
        request = f"""
            SELECT summoner_name FROM accounts
            WHERE user_id = "{user_id}"
            ORDER BY
                tier DESC,
                `rank` ASC,
                lp DESC
            LIMIT 1
        """
        self.__clearCache()
        self.__cursor.execute(request)
        return self.__cursor.fetchone()[0]


    def getUserMainAccountTier(self, user_id):
        request = f"""
            SELECT tier FROM accounts
            WHERE user_id = "{user_id}"
            ORDER BY
                tier DESC,
                `rank` ASC,
                lp DESC
            LIMIT 1
        """
        self.__clearCache()
        self.__cursor.execute(request)
        return self.__cursor.fetchone()[0]

    def getSortedUsers(self) -> 'list[tuple]':
        request = f"""
            SELECT user_id, summoner_name, tier, `rank`, lp FROM accounts
            ORDER BY
                tier DESC,
                `rank` ASC,
                lp DESC
        """
        self.__clearCache()
        self.__cursor.execute(request)
        result = self.__cursor.fetchall()
        users = [x for i, x in enumerate(result) if x[0] not in {y[0] for y in result[:i]}]
        return users

    def createUser(self, user_id: int):
        request = f"""
            INSERT INTO users (user_id)
            VALUES ("{user_id}")
        """
        self.__clearCache()
        self.__cursor.execute(request)
        self.commit()
        return 'ok'


    def checkUserExist(self, user_id: int):
        request = f"""
            SELECT count(*) FROM users
            WHERE user_id = "{user_id}"
        """
        self.__clearCache()
        self.__cursor.execute(request)
        return self.__cursor.fetchone()[0] != 0

    def addAccountToUser(self, user_id: int, summoner_name: str, tier: int, rank: int, lp: int, league_id: str):
        request = f"""
            INSERT INTO accounts (user_id, summoner_name, lp, tier, `rank`, league_id)
            VALUES ("{user_id}", "{summoner_name}", {lp}, {tier}, {rank}, "{league_id}")
        """
        self.__clearCache()
        try:
            self.__cursor.execute(request)
            self.commit()
        except:
            raise AlreadyExists(f"Le compte {summoner_name} est déjà lié à un utilisateur !")
        return 'ok'

    def setVisiblity(self, user_id, is_displayed: bool):
        request = f"""
            UPDATE accounts
            SET is_displayed = {str(is_displayed).upper()}
            WHERE user_id = "{user_id}"
        """
        self.__clearCache()
        self.__cursor.execute(request)
        self.commit()
        return 'ok'

    def getUsersId(self):
        request = f"""
            SELECT user_id FROM users
        """
        self.__clearCache()
        self.__cursor.execute(request)
        return [i[0] for i in self.__cursor.fetchall()]

    def deleteUser(self, user_id):
        request = f"""
            DELETE FROM users
            WHERE user_id = "{user_id}";
            DELETE FROM accounts
            WHERE user_id = "{user_id}";
        """
        self.__clearCache()
        self.__cursor.execute(request, multi=True)
        self.commit()
        return 'ok'

    def getUserAccountsLeagueId(self, user_id: int):
        request = f"""
            SELECT summoner_name, league_id FROM accounts
            WHERE user_id = "{user_id}"
        """
        self.__clearCache()
        self.__cursor.execute(request)
        return self.__cursor.fetchall()

    def updateUser(self, league_id: str, tier: int, rank: int, lp: int, summoner_name: str):
        request = f"""
            UPDATE accounts
            SET tier = {tier}, `rank` = {rank}, lp = {lp}, summoner_name = "{summoner_name}"
            WHERE league_id = "{league_id}"
        """
        self.__clearCache()
        self.__cursor.execute(request)
        self.commit()
        return 'ok'

    def getLeaderboardMsgs(self) -> 'list[int]':
        request = f"""
            SELECT msg_id FROM leaderboard_msgs
        """
        self.__clearCache()
        self.__cursor.execute(request)
        return [int(i[0]) for i in self.__cursor.fetchall()]

    def clearLeaderboardMsgs(self):
        request = f"""
            TRUNCATE leaderboard_msgs
        """
        self.__clearCache()
        self.__cursor.execute(request)
        self.commit()
        return 'ok'

    def addNewLeaderboardMsg(self, msg_id: int):
        request = f"""
            INSERT INTO leaderboard_msgs (msg_id)
            VALUES ("{msg_id}")
        """
        self.__clearCache()
        self.__cursor.execute(request)
        self.commit()
        return 'ok'

    def checkuserVisibility(self, user_id: int):
        request = f"""
            SELECT is_displayed FROM users
            WHERE user_id = "{user_id}"
        """
        self.__clearCache()
        self.__cursor.execute(request)
        return self.__cursor.fetchone()[0] == 1