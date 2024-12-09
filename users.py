# users.py

import os
import json

db_folder = os.path.abspath('database')


def get_users():
    userList_json = os.path.join(db_folder, 'userList.json')
    with open(userList_json) as fp:
        users = json.load(fp)
        return users

def get_user(username):
    users = get_users()
    for user in users:
        if user['username'] == username:
            return user