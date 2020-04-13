import json
import os.path

template = {
    'id': 'auto',
    'operator': '',
    'value': '',
}
accounts = {}


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
        addAccount()
        return
    if (command == 'list'):
        if (not checkArgs(args, 0, -1)):
            print('[Error] Invalid arguments. Min: 0, Max: Unlimited.')
            return
        if (len(args) > 0):
            for x in args:
                printAccount(x)
        else:
            print(f'TOTAL ACCOUNTS: {len(accounts)}')
            for x in accounts:
                printAccount(x)
        return
    if (command == 'remove'):
        if (not checkArgs(args, 1, -1)):
            print('[Error] Invalid arguments. Min: 1, Max: Unlimited.')
            return
        for x in args:
            removeAccount(x)
        return
    if (command == 'operate'):
        if (not checkArgs(args, 2, 2)):
            print('[Error] Invalid arguments. Min: 2, Max: 2.')
            return
        operateAccount(args[0], args[1])
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
    if (command == '--help' or command == 'help'):
        if (not checkArgs(args, 0, 0)):
            print('[Error] Invalid arguments. This command doesn\'t take arguments.')
            return
        print('Available commands:')
        print('--help\t\t\t\tList all commands')
        print('list\t\t\t\tList all accounts')
        print('list (id) [id] [id]...\tList specific accounts')
        print('add\t\t\t\tAdd a new account')
        print('edit (id)\t\t\tEdit account')
        print('edit (id) (key)\t\t\tEdit account')
        print('edit (id) (key) (value)\t\tEdit account')
        print('remove (id) [id] [id]...\tRemove a account')
        print('operate (id) (delta)\tAdd or Remove money from account')
        print('load (filename)\t\t\tLoad accounts from file (json)')
        print(
            'save [filename]\t\t\tSave accounts to file (json). Default filename: accounts.json')
        print('search (query))\t\t\tLook up accounts')
        print('exit\t\t\t\tExit')
        return
    print('[Error] Command not found. Type --help to list all commands.')


def checkArgs(args, _min, _max):
    return len(args) >= _min and (_max < 0 or len(args) <= _max)


def addAccount():
    print('======== ADDING NEW ACCOUNT ========')
    global template
    global accounts
    my = {}
    myid = 0
    for x in accounts:
        if (int(x) >= myid):
            myid = x
    myid = int(myid) + 1
    for key in template:
        if (template[key] == 'auto'):
            value = myid
        else:
            value = input(f'Enter value for \'{key}\': ')
        my[key] = value
    for x in accounts:
        if (accounts[x]['operator'] == my['operator']):
            print(
                f'[Error] ACCOUNT WITH OPERATOR \'{my["operator"]}\' ALREADY EXISTS')
            return
    my['value'] = int(my['value'])
    accounts[myid] = my
    print(f'======== ACCOUNT #{myid} HAS BEED ADDED ========')


def removeAccount(uid):
    try:
        uid = int(uid)
    except:
        print(f'[Error] Invalid Account ID \'{uid}\'')
        return
    print(f'======== REMOVING ACCOUNT #{uid} ========')
    global accounts
    if (uid in accounts):
        del accounts[uid]
        print(f'======== ACCOUNT #{uid} HAS BEEN REMOVED ========')
    else:
        print(f'[Error] Account #{uid} not found')
        print(f'======== ERROR REMOVING ACCOUNT #{uid} ========')


def operateAccount(uid, delta):
    delta = int(delta)
    deltaStr = str(delta)
    if (delta > 0):
        deltaStr = '+' + deltaStr
    try:
        uid = int(uid)
    except:
        print(f'[Error] Invalid Account ID \'{uid}\'')
        return
    print(f'======== OPERATION ({deltaStr}) ON ACCOUNT #{uid} ========')
    global accounts
    if (uid in accounts):
        accounts[uid]['value'] += delta
        print(f'======== OPERATION ({deltaStr}) COMPLETE ========')
    else:
        print(f'[Error] Account #{uid} not found')
        print(f'======== OPERATION ({deltaStr}) ERROR ========')


def printAccount(uid):
    try:
        uid = int(uid)
    except:
        print(f'[Error] Invalid Account ID \'{uid}\'')
        return
    global accounts
    if (uid in accounts):
        print(f'==== ACCOUNT #{uid}: ====')
        for key in accounts[uid]:
            print(f'{key}: {accounts[uid][key]}')
        print('==================')
    else:
        print(f'[Error] Account #{uid} not found')


def saveToJSON(filename):
    if (filename == ''):
        filename = 'accounts'
    if (not filename.endswith(".json")):
        filename += '.json'
    global accounts
    print(f'======== SAVING TO FILE {filename} ========')
    with open(filename, 'w') as fp:
        json.dump(accounts, fp, sort_keys=True, indent=4)
    print(f'======== SAVED ========')


def loadFromJSON(filename):
    if (not filename.endswith(".json")):
        filename += '.json'
    if (not os.path.isfile(filename)):
        print('[Error] File \'{filename}\' does not exist')
    global accounts
    with open('data.txt') as fp:
        accounts = json.load(fp)


# MAIN
print('Welcome to \'INFECTIOUS BANK\'')
print('Type --help to list all commands.')
while (True):
    command = input()
    result = commandParser(command)
    if (result == 'exit'):
        break
print('Wash your hands! #STAYHOME')
