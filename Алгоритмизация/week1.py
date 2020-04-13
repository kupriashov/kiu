import json
import os.path

template = {
    'id': 'auto',
    'first_name': '',
    'last_name': '',
    'group': '',
    'bday': '',
    'height': '',
    'weight': '',
}
users = {}


def commandParser(txt):
    _ = txt.split()
    command = _[0]
    if (len(_) > 1):
        del _[0]
        args = _
    else:
        args = []
    if (command == 'exit'):
        print('Exiting...')
        return 'exit'
    if (command == 'add'):
        if (not checkArgs(args, 0, 0)):
            print('[Error] Invalid arguments. This command doesn\'t take arguments.')
            return
        addUser()
        return
    if (command == 'list'):
        if (not checkArgs(args, 0, -1)):
            print('[Error] Invalid arguments. Min: 0, Max: Unlimited.')
            return
        if (len(args) > 0):
            for x in args:
                printUser(x)
        else:
            print(f'TOTAL USERS: {len(users)}')
            for x in users:
                printUser(x)
        return
    if (command == 'edit'):
        if (not checkArgs(args, 1, 3)):
            print('[Error] Invalid arguments. Min: 1, Max: 3.')
            return
        if (len(args) == 1):
            editUser(args[0])
        if (len(args) == 2):
            editUser2(args[0], args[1])
        if (len(args) == 3):
            editUser3(args[0], args[1], args[2])
        return
    if (command == 'remove'):
        if (not checkArgs(args, 1, -1)):
            print('[Error] Invalid arguments. Min: 1, Max: Unlimited.')
            return
        for x in args:
            removeUser(x)
        return
    if (command == 'load'):
        if (not checkArgs(args, 1, 1)):
            print('[Error] Invalid arguments. Min: 1, Max: 1.')
            return
        loadFromJSON(args[0])
        return
    if (command == 'save'):
        if (not checkArgs(args, 1, 1)):
            print('[Error] Invalid arguments. Min: 1, Max: 1.')
            return
        saveToJSON(args[0])
        return
    if (command == 'save'):
        if (not checkArgs(args, 1, -1)):
            print('[Error] Invalid query')
            return
        query = args
        if (len(args) > 1):
            query = ' '.join(args)
        lookupUser(query)
        return
    if (command == '--help' or command == 'help'):
        if (not checkArgs(args, 0, 0)):
            print('[Error] Invalid arguments. This command doesn\'t take arguments.')
            return
        print('Available commands:')
        print('--help\t\t\t\tList all commands')
        print('list\t\t\t\tList all users')
        print('list (id) [id] [id]...\tList specific users')
        print('add\t\t\t\tAdd a new user')
        print('edit (id)\t\t\tEdit user')
        print('edit (id) (key)\t\t\tEdit user')
        print('edit (id) (key) (value)\t\tEdit user')
        print('remove (id) [id] [id]...\tRemove a user')
        print('load (filename)\t\t\tLoad users from file (json)')
        print(
            'save [filename]\t\t\tSave users to file (json). Default filename: users.json')
        print('search (query))\t\t\tLook up users')
        print('exit\t\t\t\tExit')
        return
    print('[Error] Command not found. Type --help to list all commands.')


def checkArgs(args, _min, _max):
    return len(args) >= _min and (_max < 0 or len(args) <= _max)


def addUser():
    print('======== ADDING NEW USER ========')
    global template
    global users
    my = {}
    myid = 0
    for x in users:
        if (int(x) >= myid):
            myid = x
    myid = int(myid) + 1
    for key in template:
        if (template[key] == 'auto'):
            value = myid
        else:
            value = input(f'Enter value for \'{key}\': ')
        my[key] = value
    users[myid] = my
    print(f'======== USER #{myid} HAS BEED ADDED ========')


def removeUser(uid):
    try:
        uid = int(uid)
    except:
        print(f'[Error] Invalid User ID \'{uid}\'')
        return
    print(f'======== REMOVING USER #{uid} ========')
    global users
    if (uid in users):
        del users[uid]
        print(f'======== USER #{uid} HAS BEEN REMOVED ========')
    else:
        print(f'[Error] User #{uid} not found')
        print(f'======== ERROR REMOVING USER #{uid} ========')


def editUser3(uid, key, value):
    try:
        uid = int(uid)
    except:
        print(f'[Error] Invalid User ID \'{uid}\'')
        return
    if (key == 'id'):
        print(f'[Error] Can\'t edit User\'s ID')
        return
    print(f'======== EDITITNG USER #{uid} ========')
    global users
    if (uid in users):
        if (key in users[uid]):
            users[uid][key] = value
            print(f'======== USER #{uid} HAS BEEN EDITED ========')
        else:
            print(f'[Error] Invalid key \'{key}\'')
            print(f'======== ERROR EDITITNG USER #{uid} ========')
    else:
        print(f'[Error] User #{uid} not found')
        print(f'======== ERROR EDITITNG USER #{uid} ========')


def editUser2(uid, key):
    try:
        uid = int(uid)
    except:
        print(f'[Error] Invalid User ID \'{uid}\'')
        return
    if (key == 'id'):
        print(f'[Error] Can\'t edit User\'s ID')
        return
    print(f'======== EDITITNG USER #{uid} ========')
    global users
    if (uid in users):
        if (key in users[uid]):
            print(f'Key: {key}')
            print(f'Current value: {users[uid][key]}')
            value = input('New value (leave blank to keep old value): ')
            if (len(value) > 0):
                users[uid][key] = value
                print(f'======== USER #{uid} HAS BEEN EDITED ========')
        else:
            print(f'[Error] Invalid key \'{key}\'')
            print(f'======== ERROR EDITITNG USER #{uid} ========')
    else:
        print(f'[Error] User #{uid} not found')
        print(f'======== ERROR EDITITNG USER #{uid} ========')


def editUser(uid):
    try:
        uid = int(uid)
    except:
        print(f'[Error] Invalid User ID \'{uid}\'')
        return
    print(f'======== EDITITNG USER #{uid} ========')
    global users
    if (uid in users):
        for key in users[uid]:
            print(f'Key: {key}')
            print(f'Current value: {users[uid][key]}')
            value = input('New value (leave blank to keep old value): ')
            if (len(value) > 0):
                users[uid][key] = value
        print(f'======== USER #{uid} HAS BEEN EDITED ========')
    else:
        print(f'[Error] User #{uid} not found')
        print(f'======== ERROR EDITITNG USER #{uid} ========')


def lookupUser(query):
    result = []
    global users
    for uid in users:
        for key in users[uid]:
            if (query in users[uid][key] and not (uid in result)):
                result.append(uid)
    if (len(result) < 1):
        print('No users matched your query')
        return
    print(f'Found {len(result)} users:')
    for uid in result:
        printUser(uid)


def printUser(uid):
    try:
        uid = int(uid)
    except:
        print(f'[Error] Invalid User ID \'{uid}\'')
        return
    global users
    if (uid in users):
        print(f'==== USER #{uid}: ====')
        for key in users[uid]:
            print(f'{key}: {users[uid][key]}')
        print('==================')
    else:
        print(f'[Error] User #{uid} not found')


def saveToJSON(filename):
    if (filename == ''):
        filename = 'users'
    if (not filename.endswith(".json")):
        filename += '.json'
    global users
    print(f'======== SAVING TO FILE {filename} ========')
    with open(filename, 'w') as fp:
        json.dump(users, fp, sort_keys=True, indent=4)
    print(f'======== SAVED ========')


def loadFromJSON(filename):
    if (not filename.endswith(".json")):
        filename += '.json'
    if (not os.path.isfile(filename)):
        print('[Error] File \'{filename}\' does not exist')
    global users
    with open('data.txt') as fp:
        users = json.load(fp)


# MAIN
print('Welcome to \'INFECTIOUS USER EDITOR version UID-19\'')
print('Type --help to list all commands.')
while (True):
    command = input()
    result = commandParser(command)
    if (result == 'exit'):
        break
print('Wash your hands! #STAYHOME')
