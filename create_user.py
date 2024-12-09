import os
import json
from main import User

database = os.path.abspath('database')

users = []

def create_user_command(username, password, role):
    while True:
        try:
            if username and password and role:
    
                userList = os.path.join(database, 'userList.json')
                with open(userList) as file:
                    users = json.load(file)
                    print('Users: ',users)
                
                users.append({
                    'username': username,
                    'password': password,
                    'role': role
                })

                with open(userList, 'w') as file:
                    json.dump(users, file, indent=4,  
                                    separators=(',',': '))
                print(f"User created successfully: username({username}), role({role})")
                break
            else:
                print('User data is missing.')
                break
        except:
            print("An error occurred.")
            break



    

if __name__ == "__main__":
    while True:
        try:
            username = input('Please enter username: ')
            password = input("Please enter password: ")
            role = input("Please enter role: ")

            if not username:
                username = input('Please enter username: ')

            elif not password:
                password = input("Please enter password: ") 
            
            elif not role:
                role = input("Please enter role: ")

            else:
               create_user_command(username, password, role)


        except:
            print("An error occurred. Try again later.")
            break
        
