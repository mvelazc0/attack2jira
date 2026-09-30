from attackcti import attack_client
import json, sys, argparse, traceback
from getpass import getpass
from lib.jirahandler import JiraHandler
from lib.boardhandler import BoardHandler
from http import HTTPStatus
from argparse import RawTextHelpFormatter


class Attack2Jira:
    def __init__(self, url, username, password):

        self.jirahandler = JiraHandler(url, username, password)
        self.boardhandler = BoardHandler(url, username, password)

    def get_attack_techniques(self):

        try:
            print("[*] Obtaining ATT&CK's techniques...")
            client = attack_client()
            all_enterprise = client.get_enterprise()
            techniques = []
            for technique in all_enterprise["techniques"]:
                tech = json.loads(technique.serialize())
                # avoid bringing in the revoked techniques
                if not "revoked" in tech.keys():
                    techniques.append(tech)
            print("[!] Done!")
            return techniques

        except:
            traceback.print_exc(file=sys.stderr)
            print("[!] Error connecting to Att&ck's API !")
            return

    def create_attack_techniques_and_subtechniques(self, key):
        """this creates each sub-technique as a SubTask. No issue links are created"""

        jiraclient = self.jirahandler
        techniques = self.get_attack_techniques()
        sorted_techniques = sorted(
            techniques, key=lambda k: k["external_references"][0]["external_id"]
        )

        print("[*] Creating Jira issues for ATT&CK's techniques...")

        for technique in sorted_techniques:
            try:
                custom_fields = self.jirahandler.get_custom_fields()

                name = technique["name"]
                id = technique["external_references"][0]["external_id"]
                url = technique["external_references"][0]["url"]
                tactic = technique["kill_chain_phases"][0]["phase_name"]
                description = technique["description"]

                # some techniques dont have the field populated
                datasources = (
                    technique["x_mitre_data_sources"]
                    if "x_mitre_data_sources" in technique.keys()
                    else []
                )

                ds_payload = []

                for ds in datasources:
                    ds_payload.append({"value": ds.title()})

                if not technique["x_mitre_is_subtechnique"]:
                    # Not a sub-technique
                    issue_dict = {
                        "fields": {
                            "project": {"key": key},
                            "summary": name,
                            "description": description,
                            "issuetype": {"name": "Task"},
                            custom_fields["Id"]: id,
                            custom_fields["Tactic"]: {"value": tactic},
                            custom_fields["Maturity"]: {"value": "Not Tracked"},
                            custom_fields["Url"]: url,
                            custom_fields["Datasources"]: ds_payload,
                            # "customfield_11050": "Value that we're putting into a Free Text Field."
                        }
                    }
                    if self.jirahandler.check_issues_exist(issue_dict):
                        parent_dict = jiraclient.create_issue(issue_dict, id)
                        sub_technique_creation = True
                    else:
                        print(f"[x] Looks like there is a ticket already for: {name}")
                        parent_dict = ()
                        sub_technique_creation = False

                elif sub_technique_creation:
                    # Sub-technique
                    issue_dict = {
                        "fields": {
                            "parent": {"id": parent_dict["id"]},
                            "project": {"key": key},
                            "summary": name,
                            "description": description,
                            "issuetype": {"name": "Sub-task"},
                            custom_fields["Id"]: id,
                            custom_fields["Tactic"]: {"value": tactic},
                            custom_fields["Maturity"]: {"value": "Not Tracked"},
                            custom_fields["Url"]: url,
                            custom_fields["Datasources"]: ds_payload,
                            custom_fields[
                                "Sub-Technique of"
                            ]: f"{jiraclient.url}/browse/{parent_dict['key']}",
                        }
                    }
                    ret_id = jiraclient.create_issue(issue_dict, id)
                    print(f"\t + Created sub Technique with id : {str(ret_id)}")

            except Exception as ex:
                print(f"\t[*] Could not create ticket for {id}")
                print(ex)
                traceback.print_exc(file=sys.stderr)

        print("[*] Done!")

    def generate_json_layer(self, hideDisabled):
        VERSION = "2.2"
        NAME = "Attack2Jira"
        DESCRIPTION = "Attack2Jira"
        DOMAIN = "mitre-enterprise"
        GRADIENT = {
            "colors": ["#DCDCDC", "#03ad03"],
        }

        layer_json = {
            "domain": DOMAIN,
            "name": NAME,
            "description": DESCRIPTION,
            "gradient": GRADIENT,
            "version": VERSION,
            "hideDisabled": hideDisabled,
            "techniques": [],
        }

        # Define your colors here
        not_tracked_color = "#DCDCDC"
        shade_0_color = "#e1fce1"  # lightest green
        shade_1_color = "#81fc81"  # lighter green
        shade_2_color = "#49fc49"  # green
        shade_3_color = "#03ad03"  # darker green

        res_dict = self.jirahandler.get_technique_maturity()
        for key in res_dict.keys():
            enabled = True

            if res_dict[key]["value"] == "Not Tracked":
                enabled = False
                color = not_tracked_color
            elif res_dict[key]["value"] == "Initial":
                color = shade_0_color
            elif res_dict[key]["value"] == "Defined":
                color = shade_1_color
            elif res_dict[key]["value"] == "Resilient":
                color = shade_2_color
            elif res_dict[key]["value"] == "Optimized":
                color = shade_3_color

            technique = {"techniqueID": key, "enabled": enabled, "color": color}
            layer_json["techniques"].append(technique)

        print("[*] Outputting JSON layer attack2jira.json")
        with open("attack2jira.json", "w", encoding="utf-8") as f:
            json.dump(layer_json, f, ensure_ascii=False, indent=4)

    def set_up_jira_project_automated(self, project, key):
        """ Set up Jira Project"""
        self.jirahandler.create_project(project, key)

    def set_up_jira_board_automated(self, key):
        """ Set up Jira Kanban Board"""
        try:
            filter_id = input("Filter_ID for board: ")
            key = input(f"Enter project KEY or leave blank (default is {key}): ") or key
            board_id = str(input("Enter board ID (press E if board not created): ") or None)
        except Exception as ex:
            traceback.print_exc(file=sys.stderr)
            print(ex)

        if not self.boardhandler.check_board(board_id):
            board_name = input(
                "Please enter the name of the board you wish to create: "
            )
            self.boardhandler.create_board(board_name, filter_id, key)

    def set_up_jira_automated(self, key):
        """ Set up Attack2Mitre """

        self.jirahandler.create_custom_fields()
        self.jirahandler.add_custom_field_options()
        self.jirahandler.add_custom_fields_to_screen(key)
        self.jirahandler.hide_unwanted_fields(key)
        self.create_attack_techniques_and_subtechniques(key)


def main():

    parser = argparse.ArgumentParser(formatter_class=RawTextHelpFormatter)
    parser.add_argument(
        "-url", dest="url", type=str, help="Url of Jira instance", default=""
    )
    parser.add_argument("-u", dest="user", type=str, help="Username", default="")
    parser.add_argument(
        "-a",
        dest="action",
        type=str,
        default="",
        help="action to execute\nTwo supported:\n'initialize' will create the JIRA entities. \n'export' will export the JSON layer.",
    )
    parser.add_argument(
        "-p",
        dest="project",
        type=str,
        help="Name of the Jira project to create.",
        default="Mitre Attack Framework",
    )
    parser.add_argument(
        "-k",
        dest="key",
        type=str,
        help="Project Key.(default='ATT')",
        default="ATT",
    )
    parser.add_argument(
        "-hide",
        help="If set, 'Not Tracked' techniques will be hidden",
        action="store_true",
    )
    results = parser.parse_args()

    # arguments
    url = results.url
    user = results.user
    action = results.action
    hideDisabled = results.hide
    project = results.project
    key = results.key

    if url and user and action:
        pswd = getpass(f"Jira API Token for {user}:")
        attack2jira = Attack2Jira(url, user, pswd)

        if action == "project":
            """ Initialise Attack2Mitre with project"""
            attack2jira.set_up_jira_project_automated(project, key)

        elif action == "board":
            """ Initialise Attack2Mitre with kanban board"""
            attack2jira.set_up_jira_board_automated(key)

        elif action == "export":
            """ Export Json Layer for ATT&ACK Navigator"""
            attack2jira.generate_json_layer(hideDisabled)

        # finish set up
        attack2jira.set_up_jira_automated(key)

    else:
        parser.print_help()


if __name__ == "__main__":

    try:
        main()

    except KeyboardInterrupt:
        print("\n")
        print("[!] Exiting attack2jira")
        sys.exit()