from unittest import TestCase
from Helper import WikiHelper
from UserManager import UserManager

class Command_Line_Test_Case(TestCase):

    wikihelper = WikiHelper.WikiHelper
    user_manager = UserManager.UserManager('/Users/dustingulley/nku/CSC-540/RikiWiki/wiki_flask/user')

    def test_read_file(self):
        args = {
            'r': True
        }
        message = self.wikihelper.analyze_file(args, self.user_manager)
        assert 1 != 2

