from gallery.tools.db import DbConnection

def getUsers(db):
    res = db.execute('select * from users')
    for row in res:
        print(row)

def getUser(db, username):
    s = 'select * from users where username = \'{}\''.format(username)
    db.execute(s)
    

def main():
    db = DbConnection()
    db.connect()

    userInput = None
    menu = '\n'
    menu += '\n1) List users'
    menu +=	'\n2) Add user'
    menu +=	'\n3) Edit user'
    menu +=	'\n4) Delete user'
    menu +=	'\n5) Quit'

    while (userInput != '5'):
        print(menu)
        userInput = input("\nEnter command> ")
        
        if (userInput == '1'):
            s = db.get_users()
            print(s)
        elif (userInput == '2'):
            username = input('Username> ')
            password = input('Password> ')
            full_name = input('Full name> ')

            # check if username exists in the database
            if (not db.get_user(username)):
                # if not, add user
                db.add_user(username, password, full_name)
            # else, add the user to the database
            else:
                print('\nError: user with username ' + username + ' already exists')

        elif (userInput == '3'):
            username = input('Username to edit> ')
            user = db.get_user(username)

            if (not db.get_user(username)):
                print('\nNo such user.')
            else:
                user_array = user.split(',')

                password = input('New password (press enter to keep current)> ')
                if (not password):
                    password = user_array[1]

                full_name = input('New full name (press enter to keep current)> ')
                if (not full_name):
                    full_name = user_array[2]

                db.update_user(username, password, full_name)
        elif (userInput == '4'):
            username = input('Username to delete> ')

            if (not db.get_user(username)):
                print('\nNo such user.')
            else:
                response = input('Are you sure you want to delete ' + username + '? [Y / n] ')
                response = response.lower()
                if (response == 'y'):
                    db.delete_user(username)
        elif (userInput == '5'):
            print('You quit!')
        else:
            print('Please select a number between 1 and 5')



if __name__ == '__main__':
    main()
