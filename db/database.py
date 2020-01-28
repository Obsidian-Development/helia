import sqlite3


class Database:
    def __init__(self, bot=None):
        self.bot = bot
        self.conn = None
        self.DB_NAME = "database.db"
        print("Opened database successfully")

    def flag_gaming_channel(self, channel_id, game_title, allowed):
        self.conn = sqlite3.connect(self.DB_NAME)
        sql = 'insert into game_restriction (channel_ID, title, allowed) ' \
              'VALUES ("{}","{}",{})'.format(channel_id, game_title, allowed)

        self.conn.execute(sql)
        self.conn.commit()
        self.conn.close()

    def get_flagged_games(self, channel_id):
        flagged_games = []
        self.conn = sqlite3.connect(self.DB_NAME)
        games = self.conn.execute("select title from game_restriction where channel_ID = '{}' and allowed = 1"
                                  .format(channel_id))

        for game in games:
            flagged_games.append(game[0])

        self.conn.commit()
        self.conn.close()
        return flagged_games

    def remove_flagged_games(self, channel_id):
        self.conn = sqlite3.connect(self.DB_NAME)
        self.conn.execute("delete from game_restriction WHERE channel_id = '{}';".format(channel_id))
        self.conn.close()

    def get_game_channel(self, title):
        channels = []
        self.conn = sqlite3.connect(self.DB_NAME)
        games = self.conn.execute("select channel_ID from game_restriction where title = '{}' and allowed = 1"
                                  .format(title))

        for game in games:
            channels.append(game[0])

        self.conn.commit()
        self.conn.close()
        return channels


    def insert_coins(self, userid, coins, mention=None):
        self.conn = sqlite3.connect(self.DB_NAME)

        if mention == None and self.bot != None: mention = self.bot.Client.get_user_info(userid)

        if mention != None:
            sql = "INSERT OR IGNORE INTO members (userid, coins, user_mention) VALUES(?,0,?);"
            self.conn.execute(sql, (userid, mention,))
            params = (coins, mention, userid,)
            sql = "UPDATE members SET coins = coins + ?, user_mention = ? WHERE userid = ?;"

        elif mention == None:
            sql = "INSERT OR IGNORE INTO members (userid, coins) VALUES(?,0,?);"
            self.conn.execute(sql, (userid,))
            params = (coins, userid,)
            sql = "UPDATE members SET coins = coins + ? WHERE userid = ?;"

        self.conn.execute(sql, params)
        self.conn.commit()
        self.conn.close()

    def remove_coins(self, userid, coins, mention=None):
        self.conn = sqlite3.connect(self.DB_NAME)

        if mention == None and self.bot != None: mention = self.bot.Client.get_user_info(userid)

        if mention != None :
            sql = "INSERT OR IGNORE INTO members (userid, coins, user_mention) VALUES(?,0,?);"
            self.conn.execute(sql, (userid,mention,))
            params = (coins, mention, userid,)
            sql = "UPDATE members SET coins = coins - ?, user_mention = ? WHERE userid = ?;"

        elif mention == None :
            sql = "INSERT OR IGNORE INTO members (userid, coins) VALUES(?,0,?);"
            self.conn.execute(sql, (userid,))
            params = (coins, userid,)
            sql = "UPDATE members SET coins = coins - ? WHERE userid = ?;"


        self.conn.execute(sql, params)
        self.conn.commit()
        self.conn.close()

    def get_coins(self, userid):
        self.conn = sqlite3.connect(self.DB_NAME)
        sql = "INSERT OR IGNORE INTO members (userid, coins) VALUES(?,0);"
        self.conn.execute(sql, (userid,))
        sql = "SELECT coins, userid FROM members WHERE userid = ?"
        params = (userid,)
        result = self.conn.execute(sql, params)
        output = 0
        for i in result :
            output = output + i[0]

        self.conn.close()

        return output

    def get_top_coin_holders(self):
        toplist = []
        self.conn = sqlite3.connect(self.DB_NAME)
        sql = "SELECT userid, coins, user_mention FROM members ORDER BY coins DESC LIMIT 5;"
        result = self.conn.execute(sql)
        for user in result:
            toplist.append({"userid": user[0], "coins": user[1], "mention": user[2]})
        self.conn.close()
        return toplist

    def get_rich_users(self, botid, wealthy_amount):
        users = []
        self.conn = sqlite3.connect(self.DB_NAME)
        sql = "SELECT userid, coins, user_mention FROM members WHERE MEMBERS.userid != ? AND MEMBERS.coins >= ?;"
        params = (botid, wealthy_amount,)
        result = self.conn.execute(sql, params)
        for user in result:
            users.append({"userid": user[0], "coins": user[1], "mention": user[2]})
        return users


    def add_music_to_db(self, link):
        self.conn = sqlite3.connect(self.DB_NAME)
        sql = "insert or ignore into music (link, countRequested) VALUES (?, ?)"
        params = (link, 0)
        self.conn.execute(sql, params)

        sql = "UPDATE music SET countRequested = countRequested + 1 WHERE link = ?"
        params = (link,)
        self.conn.execute(sql, params)

        self.conn.commit()
        self.conn.close()

    def get_random_music(self):
        self.conn = sqlite3.connect(self.DB_NAME)
        sql = "SELECT * FROM music ORDER BY RANDOM() LIMIT 1;"
        result = self.conn.execute(sql)
        self.conn.commit()
        output = None
        for x in result: output = x[0]
        self.conn.close()
        return output

if __name__ == '__main__':
    db = Database()




