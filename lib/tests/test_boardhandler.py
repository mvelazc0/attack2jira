from unittest import main, TestCase
from lib.boardhandler import BoardHandler
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


class TestBoardHandler(TestCase):
    """ Testing the BoardHandler Class"""

    boardhandler = None

    def test_check_board(self):
        """Test if check_board works"""

        no_board_id = "00"
        # existing_board_id = ''

        # there shouldn't be a board with ID:
        self.assertEqual(boardhandler.check_board(no_board_id), False)

        # # there should be a board with ''
        # self.assertEqual(boardhandler.check_board(existing_board_id), True)

    def test_create_board(self):
        """ Test if it attempts to create a board"""

        board = "bees"
        filter_id = "dogs"
        project_key = "cats"

        self.assertEqual(boardhandler.create_board(board, filter_id, project_key), 400)


if __name__ == "__main__":

    url = ""
    username = ""
    password = ""

    boardhandler = BoardHandler(url, username, password)

    main()
