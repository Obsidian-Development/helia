import os

main = os.path.join("db/main.db")

def insert_table(table_name):
    insert = f"INSERT INTO {table_name}(guild_id, channel_id) VALUES(?,?)"
    return insert

def update_table(table_name, channel, guild):
    update = f"UPDATE {table_name} SET channel_id = {channel} WHERE guild_id = {guild}"
    return update

def select_table(table_name, guild):
    select = f"SELECT channel_id FROM {table_name} WHERE guild_id = {guild}"
    return select

def delete_table(table_name, guild):
    delete = f"DELETE FROM {table_name} WHERE guild_id = {guild}"
    return delete

