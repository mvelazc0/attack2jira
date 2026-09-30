from unittest import main, TestCase
from lib.boardhandler import BoardHandler
import urllib3
import os
from http import HTTPStatus

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


class TestBoardHandler(TestCase):
    """ Testing the BoardHandler Class"""

    BoardHandler = None

    def test_check_board(self):
        """Test if check_board works"""

        no_board_id = 0
        # existing_board_id = ''

        # there shouldn't be a board with ID:
        self.assertEqual(boardhandler.check_board(no_board_id), False)

        # there should be a board with ''
        # self.assertEqual(boardhandler.check_board(existing_board_id), HTTPStatus.OK)

    def test_create_board(self):
        """ Test if it attempts to create a board"""

        board = "bees"
        filter_id = "dogs"
        project_key = "cats"

        self.assertEqual(
            boardhandler.create_board(board, filter_id, project_key),
            HTTPStatus.BAD_REQUEST,
        )


if __name__ == "__main__":

    url = os.environ["DOMAIN"]
    username = os.environ["USER"]
    password = os.environ["API_TOKEN"]

    boardhandler = BoardHandler(url, username, password)

    main()
