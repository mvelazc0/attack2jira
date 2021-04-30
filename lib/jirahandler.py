from attackcti import attack_client
import requests
import sys, traceback, json
import urllib3
from http import HTTPStatus
from yarl import URL

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


class JiraHandler:

    url = URL
    username = str
    apitoken = str

    def __init__(self, url, username, password):

        self.login(url, username, password)

    def login(self, url, username, apitoken):

        headers = {"Content-Type": "application/json"}

        try:
            print(f"[*] Authenticating to {url} ...")
            r = requests.get(
                f"{url}/rest/api/2/issue/createmeta",
                headers=headers,
                auth=(username, apitoken),
                verify=False,
            )

            if r.status_code == HTTPStatus.OK:
                self.username = username
                self.apitoken = apitoken
                self.url = url
                print("[!] Success!")

            elif r.status_code == HTTPStatus.UNAUTHORIZED:
                print("[!] Wrong username or password :( .")
                sys.exit()

        except Exception as ex:
            print("[!] Error when trying to authenticate.")
            traceback.print_exc(file=sys.stderr)

    def create_project(self, project, key):

        print("[*] Creating the Att&ck project...")
        headers = {"Content-Type": "application/json"}
        project_dict = {
            "key": key,
            "name": project,
            "templateKey": "com.pyxis.greenhopper.jira:gh-simplified-basic",
        }
        try:
            r = requests.post(
                f"{self.url}/rest/simplified/latest/project",
                json=project_dict,
                headers=headers,
                auth=(self.username, self.apitoken),
                verify=False,
            )
            if r.status_code == HTTPStatus.CREATED:
                print("[!] Success!")

            elif r.status_code == HTTPStatus.UNAUTHORIZED:
                print("[!] Unauthorized. Probably not enough permissions :(")

            else:
                print("[!] Error creating Jira project. Does it already exist ?")

        except Exception as ex:
            print("[!] Error creating Jira project")
            traceback.print_exc(file=sys.stderr)

    def create_custom_fields(self):

        # avoid creating the custom fields more than once
        if not self.do_custom_fields_exist():
            print("[*] Creating custom fields ...")
            headers = {"Content-Type": "application/json"}
            try:

                custom_fields = []
                custom_field1_dict = {
                    "searcherKey": "com.atlassian.jira.plugin.system.customfieldtypes:multiselectsearcher",
                    "name": "Tactic",
                    "description": "Attack Tactic",
                    "type": "com.atlassian.jira.plugin.system.customfieldtypes:select",
                }
                custom_fields.append(custom_field1_dict)

                custom_field2_dict = {
                    "searcherKey": "com.atlassian.jira.plugin.system.customfieldtypes:multiselectsearcher",
                    "name": "Maturity",
                    "description": "Detection Maturity",
                    "type": "com.atlassian.jira.plugin.system.customfieldtypes:select",
                }
                custom_fields.append(custom_field2_dict)

                custom_field3_dict = {
                    "searcherKey": "com.atlassian.jira.plugin.system.customfieldtypes:exacttextsearcher",
                    "name": "Url",
                    "description": "Attack Technique Url",
                    "type": "com.atlassian.jira.plugin.system.customfieldtypes:url",
                }
                custom_fields.append(custom_field3_dict)

                custom_field4_dict = {
                    "searcherKey": "com.atlassian.jira.plugin.system.customfieldtypes:multiselectsearcher",
                    "name": "Datasources",
                    "description": "Data Sources",
                    "type": "com.atlassian.jira.plugin.system.customfieldtypes:multiselect",
                }
                custom_fields.append(custom_field4_dict)

                custom_field5_dict = {
                    "searcherKey": "com.atlassian.jira.plugin.system.customfieldtypes:textsearcher",
                    "name": "Id",
                    "description": "Technique Id",
                    "type": "com.atlassian.jira.plugin.system.customfieldtypes:textfield",
                }
                custom_fields.append(custom_field5_dict)

                custom_field6_dict = {
                    "searcherKey": "com.atlassian.jira.plugin.system.customfieldtypes:textsearcher",
                    "name": "Sub-Technique of",
                    "description": "Parent Technique Id",
                    "type": "com.atlassian.jira.plugin.system.customfieldtypes:textfield",
                }
                custom_fields.append(custom_field6_dict)

                for custom_field in custom_fields:
                    r = requests.post(
                        f"{self.url}/rest/api/3/field",
                        json=custom_field,
                        headers=headers,
                        auth=(self.username, self.apitoken),
                        verify=False,
                    )

                    if r.status_code == HTTPStatus.CREATED:
                        print(
                            f"[!] Successfully created /{custom_field['name']}/ custom field."
                        )

                    elif r.status_code == HTTPStatus.UNAUTHORIZED:
                        print("[!] Unauthorized. Probably not enough permissions :(")

                    else:
                        print("[!] Error creating custom fields")
                        sys.exit()

            except Exception as ex:
                traceback.print_exc(file=sys.stderr)

        else:
            print("[!] Found custom fields")

    def add_custom_field_options(self):

        custom_fields = self.get_custom_fields()
        headers = {"Content-Type": "application/json"}
        try:

            # maturity field options
            payload = [
                {"name": "Not Tracked"},
                {"name": "Initial"},
                {"name": "Defined"},
                {"name": "Resilient"},
                {"name": "Optimized"},
            ]
            r = requests.post(
                f"{self.url}/rest/globalconfig/1/customfieldoptions/{custom_fields['Maturity']}",
                headers=headers,
                json=payload,
                auth=(self.username, self.apitoken),
                verify=False,
            )
            if r.status_code != HTTPStatus.NO_CONTENT:
                print("[!] Error creating options for the maturity custom field.")
                sys.exit()

            # tactic field options
            payload = self.get_attack_tactics()
            r = requests.post(
                f"{self.url}/rest/globalconfig/1/customfieldoptions/{custom_fields['Tactic']}",
                headers=headers,
                json=payload,
                auth=(self.username, self.apitoken),
                verify=False,
            )
            if r.status_code != HTTPStatus.NO_CONTENT:
                print("[!] Error creating options for the tactic custom field.")
                sys.exit()

            # data source field options
            payload = self.get_attack_datasources()
            r = requests.post(
                f"{self.url}/rest/globalconfig/1/customfieldoptions/{custom_fields['Datasources']}",
                headers=headers,
                json=payload,
                auth=(self.username, self.apitoken),
                verify=False,
            )
            if r.status_code != HTTPStatus.NO_CONTENT:
                print("[!] Error creating options for the datasources custom field.")
                sys.exit()

        except Exception as ex:
            traceback.print_exc(file=sys.stderr)
            sys.exit()

    def get_custom_fields(self):

        custom_fields = [
            "Tactic",
            "Maturity",
            "Url",
            "Datasources",
            "Id",
            "Sub-Technique of",
        ]
        headers = {"Content-Type": "application/json"}
        resp = dict()

        try:
            r = requests.get(
                f"{self.url}/rest/api/3/field",
                headers=headers,
                auth=(self.username, self.apitoken),
                verify=False,
            )
            if r.status_code == HTTPStatus.OK:
                results = r.json()
                for r in results:
                    if r["name"] in custom_fields:
                        resp.update({r["name"]: r["id"]})

            else:
                print("[!] Error getting custom fields")

            return resp

        except Exception as ex:
            traceback.print_exc(file=sys.stderr)

    def hide_unwanted_fields(self, key):

        print("[*] Hiding unnecessary fields from ATTACK's issue layout...")
        project_id = self.get_project_id(key)
        screen_tab_ids = self.get_project_screen_tab_ids(project_id)
        custom_Fields = self.get_custom_fields()

        headers = {"Content-Type": "application/json"}

        json_string = '{"context":{"primary":[{"id":"assignee","type":"FIELD"},{"id":"reporter","type":"FIELD"},{"id":"labels","type":"FIELD"},{"id":"MATURITY_CUSTOMFIELD","type":"FIELD"},{"id":"DATASOURCE_CUSTOMFIELD","type":"FIELD"}],"secondary":[{"id":"priority","type":"FIELD"}],"alwaysHidden":[{"id":"timeoriginalestimate","type":"FIELD"},{"id":"timetracking","type":"FIELD"},{"id":"components","type":"FIELD"},{"id":"fixVersions","type":"FIELD"},{"id":"customfield_10014","type":"FIELD"},{"id":"duedate","type":"FIELD"},{"id":"customfield_10011","type":"FIELD"},{"id":"customfield_10026","type":"FIELD"},{"id":"devSummary","type":"DEV_SUMMARY"}]},"content":{"visible":[{"id":"TACTIC_CUSTOMFIELD","type":"FIELD"},{"id":"ID_CUSTOMFIELD","type":"FIELD"},{"id":"URL_CUSTOMFIELD","type":"FIELD"},{"id":"SUBTECHNIQUE_CUSTOMFIELD","type":"FIELD"},{"id":"description","type":"FIELD"}],"alwaysHidden":[]}}'

        json_string = json_string.replace(
            "DATASOURCE_CUSTOMFIELD", custom_Fields["Datasources"]
        )
        json_string = json_string.replace("ID_CUSTOMFIELD", custom_Fields["Id"])
        json_string = json_string.replace("TACTIC_CUSTOMFIELD", custom_Fields["Tactic"])
        json_string = json_string.replace(
            "MATURITY_CUSTOMFIELD", custom_Fields["Maturity"]
        )
        json_string = json_string.replace("URL_CUSTOMFIELD", custom_Fields["Url"])
        json_string = json_string.replace(
            "SUBTECHNIQUE_CUSTOMFIELD", custom_Fields["Sub-Technique of"]
        )

        try:
            for screen_tab_id in screen_tab_ids:
                r = requests.put(
                    f"{self.url}/rest/issuedetailslayout/config/classic/screen?projectIdOrKey={key}&screenId={str(screen_tab_id[0])}",
                    data=json_string,
                    headers=headers,
                    auth=(self.username, self.apitoken),
                    verify=False,
                )
            print("[!] Done.")

        except Exception as ex:
            print(ex)
            traceback.print_exc(file=sys.stderr)

    def do_custom_fields_exist(self):

        custom_fields = self.get_custom_fields()

        ## TODO: Need to perform better checks but this works for now.
        if len(custom_fields.keys()) == 6:
            return True
        else:
            return False

    def create_issue(self, issue_dict, id):

        headers = {"Content-Type": "application/json"}
        try:
            r = requests.post(
                f"{self.url}/rest/api/2/issue",
                json=issue_dict,
                headers=headers,
                auth=(self.username, self.apitoken),
                verify=False,
            )

            if r.status_code == HTTPStatus.CREATED:
                print(f"\t[!] Successfully created Jira issue for {id}")
                return json.loads(r.text)
            else:
                print(f"\t[!] Error creating Jira issue for {id}")
                print(r.text)
                sys.exit()

        except Exception as ex:
            print(ex)
            traceback.print_exc(file=sys.stderr)
            sys.exit()

    def get_attack_screens(self, key):

        headers = {"Content-Type": "application/json"}
        screen_ids = []
        try:
            r = requests.get(
                f"{self.url}/rest/api/3/screens",
                headers=headers,
                auth=(self.username, self.apitoken),
                verify=False,
            )

            if r.status_code == HTTPStatus.OK:
                results = r.json()["values"]
                for r in results:
                    if key in r["name"] and "Default Issue Screen" in r["name"]:
                        screen_ids.append(r["id"])
            else:
                print("[!] Error obtaining screens")

            return screen_ids

        except Exception as ex:
            traceback.print_exc(file=sys.stderr)
            sys.exit()


    def check_issues_exist(self, issue_dict):
        """Get issues from project"""

        headers = {"Content-Type": "application/json"}
        read_issues = 0
        startAt = 0
        res_dict = dict()

        try:

            while True:

                r = requests.get(
                    f"{self.url}/rest/api/3/search?jql=project%20%3D%20ATTACK&startAt={str(startAt)}",
                    headers=headers,
                    auth=(self.username, self.apitoken),
                    verify=False,
                )
                resp_dict = r.json()
                for issue in resp_dict["issues"]:
                    if issue in issue_dict.values():
                        print(f"{issue} already exists ... ")
                        return True
                    else:
                        return False

                read_issues += 50
                startAt += 50
                if read_issues >= r.json()["total"]:
                    break

            return res_dict

        except Exception as ex:
            traceback.print_exc(file=sys.stderr)
            sys.exit()

    def get_technique_maturity(self):

        print("[*] Getting issues from the ATTACK project...")
        custom_fields = self.get_custom_fields()
        headers = {"Content-Type": "application/json"}
        read_issues = 0
        startAt = 0
        res_dict = dict()

        try:

            while True:

                r = requests.get(
                    f"{self.url}/rest/api/3/search?jql=project%20%3D%20ATTACK&startAt={str(startAt)}",
                    headers=headers,
                    auth=(self.username, self.apitoken),
                    verify=False,
                )
                resp_dict = r.json()
                for issue in resp_dict["issues"]:
                    technique_id = issue["fields"][custom_fields["id"]]
                    res_dict.update(
                        {technique_id: issue["fields"][custom_fields["Maturity"]]}
                    )
                read_issues += 50
                startAt += 50
                if read_issues >= r.json()["total"]:
                    break

            return res_dict

        except Exception as ex:
            traceback.print_exc(file=sys.stderr)
            sys.exit()

    def get_attack_datasources(self):

        try:
            datasource_payload = []
            client = attack_client()
            datasources = list(set(ds.lower() for ds in client.get_data_sources()))
            for datasource in datasources:
                dict = {"name": datasource.title()}
                datasource_payload.append(dict)
            return datasource_payload

        except:
            traceback.print_exc(file=sys.stderr)
            print("[!] Error connecting obtaining datasources from Att&ck's API !")
            sys.exit()

    def get_attack_tactics(self):

        try:
            tactics_payload = []
            client = attack_client()
            enterprise_tactics = client.get_enterprise()
            tactics = [
                tactic["name"].lower().replace(" ", "-")
                for tactic in enterprise_tactics["tactics"]
            ]
            for tactic in tactics:
                tactics_payload.append({"name": tactic})
            return tactics_payload

        except:
            traceback.print_exc(file=sys.stderr)
            print("[!] Error connecting obtaining tactics from Att&ck's API !")
            sys.exit()

    def add_custom_fields_to_screen(self, key):

        print("[*] Adding custom fields to ATTACK's default screen tab ...")
        headers = {"Content-Type": "application/json"}
        project_id = self.get_project_id(key)
        screen_tab_ids = self.get_project_screen_tab_ids(project_id)
        custom_fields = self.get_custom_fields()

        try:
            for key in custom_fields.keys():
                for screen_tab_id in screen_tab_ids:
                    custom_field_dict = {"fieldId": custom_fields[key]}

                    r = requests.post(
                        f"{self.url}/rest/api/3/screens/{str(screen_tab_id[0])}/tabs/{str(screen_tab_id[1])}/fields",
                        json=custom_field_dict,
                        headers=headers,
                        auth=(self.username, self.apitoken),
                        verify=False,
                    )

            print("[!] Done!.")

        except Exception as ex:
            traceback.print_exc(file=sys.stderr)
            sys.exit()

    def get_project_id(self, key):
        headers = {"Content-Type": "application/json"}
        try:
            r = requests.get(
                f"{self.url}/rest/api/3/project/search",
                headers=headers,
                auth=(self.username, self.apitoken),
                verify=False,
            )
            resp_dict = r.json()
            for project in resp_dict["values"]:
                if project["key"] == key:
                    return project["id"]
            return 0

        except:
            traceback.print_exc(file=sys.stderr)
            print("[!] Error obtaining project id!")
            sys.exit()

    def get_project_screen_tab_ids(self, project_id):
        headers = {"Content-Type": "application/json"}
        screen_tab_ids = []
        try:
            r = requests.get(
                f"{self.url}/rest/api/3/issuetypescreenscheme/mapping?issueTypeScreenSchemeId={project_id}",
                headers=headers,
                auth=(self.username, self.apitoken),
                verify=False,
            )
            resp_dict = r.json()
            for screen in resp_dict["values"]:
                screen_tab_ids.append(
                    [
                        screen["screenSchemeId"],
                        self.get_screen_tab_id(screen["screenSchemeId"]),
                    ]
                )

            return screen_tab_ids

        except:
            traceback.print_exc(file=sys.stderr)
            print("[!] Error obtaining screen/tab ids!")
            sys.exit()

    def get_screen_tab_id(self, screen_id):
        headers = {"Content-Type": "application/json"}
        try:
            r = requests.get(
                f"{self.url}/rest/api/3/screens/{screen_id}/tabs",
                headers=headers,
                auth=(self.username, self.apitoken),
                verify=False,
            )
            resp_dict = r.json()
            return resp_dict[0]["id"]

        except:
            traceback.print_exc(file=sys.stderr)
            print("[!] Error obtaining screen/tab ids!")
            sys.exit()