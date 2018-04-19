import argparse
import re
from UserManager import UserManager
import datetime

def users_to_string(users):
    """Converts the user dictionary to a string"""

    message = ""

    for key, value in users.iteritems():
        sValue = str(value)
        sValue = sValue[1:(len(sValue) - 1)]
        message += str(key) + ": " + sValue + "\n"

    return message

def analyze_file(args, user_manager):
    """A file is present analyze it"""

    message = ""
    users = None
    role_s = ""
    time = ""
    roles = []
    auth = None
    added = False
    user = None
    sData = ""
    deleted = False

    if args.r:
        users = user_manager.read()
        message += users_to_string(users)
    if args.p and (args.n is not None) and (args.pa is not None):
        if args.ro is not None:
            role_s = args.ro
            roles = role_s.split(",")
        if args.am is not None:
            auth = args.am
        time = str(datetime.datetime.now())
        added = user_manager.add_user(args.n, args.pa, time, True, roles, auth)
        if added is False or added is None:
            message += args.n + " failed!"
        else:
            message += args.n + " added!"
    if args.g and args.n is not None:
        user = user_manager.get_user(args.n)
        sData = str(user.data)
        sData = sData[1:(len(sData) - 1)]
        message += user.name + ": " + sData + "\n"
    if args.d and args.n is not None:
        deleted = user_manager.delete_user(args.n)
        if deleted is True:
            message += args.n + " deleted!"
        else: message += args.n + " failed!"
    if args.u and args.n is not None:
        user = user_manager.get_user(args.n)
        if args.pa is not None:
            user.data['password'] = args.pa
        if args.ro is not None:
            role_s = args.ro
            roles = role_s.split(",")
            user.data['roles'] = roles
        if args.am is not None:
            user.data['authentication_method'] = args.am
        time = str(datetime.datetime.now())
        user.data['time'] = time
        user_manager.update(user.name, user.data)
        message += args.n + " updated!"

    return message


if __name__ == '__main__':

    message = None  # The message to print to the user
    parser = None   # The argparse instance
    user_manager = None

    parser = argparse.ArgumentParser()  # Create the parser

    """Add the parser arguments"""
    parser.add_argument('-p', help='Path to the user file.')
    parser.add_argument('-r', help='Read the contents of the user file and print to the console', action="store_true")
    parser.add_argument('-a', help="Add a new user.  You must also use the name (-n) and password (-pass) at minumun.", action="store_true")
    parser.add_argument('-n', help="Username")
    parser.add_argument('-pa', help="Password")
    parser.add_argument('-ro',  help="Roles.  Ex. administer,user,power_user")
    parser.add_argument('-am', help="Auth method.")
    parser.add_argument('-g', help="Gets a single user.  You must also use the name (-n) option.", action="store_true")
    parser.add_argument('-d', help="Delete User.  You must also use the name (-n option),", action="store_true")
    parser.add_argument('-u', help="Update User. You must also use the -n option at minimum.", action="store_true")
    args = parser.parse_args()

    if args.p is not None:
        user_manager = UserManager.UserManager(args.p)
        message = analyze_file(args, user_manager)
    else:
        message = "Please provide a file to analyze"

    print message

