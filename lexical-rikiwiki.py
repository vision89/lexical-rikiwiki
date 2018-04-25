import argparse
from UserManager import UserManager
from Helper import WikiHelper


if __name__ == '__main__':
    wikihelper = WikiHelper.WikiHelper;
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
        message = wikihelper.analyze_file(args, user_manager)
    else:
        message = "Please provide a file to analyze"

    print message

