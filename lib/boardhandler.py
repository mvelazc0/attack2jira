import sys
import traceback
import requests
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
from typing import NamedTuple
from yarl import URL

class BoardHandler(NamedTuple):
    """ Kanban Board Class for Attack2Jira"""

    url:  URL
    username: str
    apitoken: str

    def check_board(self, board_id):
        # TODO: pass the id created from create_board() if there isnt a board created for future checks
        """Checks if Kanban Board Exists"""

        print("[*] Checking if there is an Att&ck board... ")

        headers = {"Content-Type": "application/json"}

        r = requests.get(
            f"{self.url}/rest/agile/1.0/board/{board_id}",
            headers=headers,
            auth=(self.username, self.apitoken),
            verify=False,
        )

        if r.status_code == 200:
            print("[!] Success! Looks like there is an existing kanban board")
            return True

        else:
            print("[!] No board detected ")
            traceback.print_exc(file=sys.stderr)
            return False

    def create_board(self, board, filter_id, project_key):
        """Creates Kanban Board under Project: Security"""

        print("[*] Creating the Att&ck board...")
        headers = {"Content-Type": "application/json"}

        project_dict = {
            "name": board,
            "type": "kanban",
            "filterId": filter_id,
            "location": {"type": "project", "projectKeyOrId": project_key},
        }

        r = requests.post(
            self.url / "/rest/agile/1.0/board",
            json=project_dict,
            headers=headers,
            auth=(self.username, self.apitoken),
            verify=False,
        )
        if r.status_code == 201:
            print("[!] Success!")

        elif r.status_code == 401:
            print("[!] Unauthorized. Probably not enough permissions :(")
            sys.exit(1)

        else:
            print("[!] Error creating Jira board: ")
            return r.status_code
            traceback.print_exc(file=sys.stderr)
            sys.exit(1)