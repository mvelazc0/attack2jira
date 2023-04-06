from attackcti import attack_client
import requests
import sys, traceback, json, re
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class JiraHandler:

    username=""
    apitoken=""
    url=""

    def __init__(self, url, username, password):

        self.login(url, username, password)

    def login(self, url, username, apitoken):

        headers = {'Content-Type': 'application/json'}

        try:
            print("[*] Authenticating to " + url + "...")
            r = requests.get(url + '/rest/api/2/issue/createmeta', headers=headers,auth=(username,apitoken), verify=False)

            if r.status_code == 200:
                self.username=username
                self.apitoken=apitoken
                self.url=url
                print("[!] Success!")

            elif r.status_code == 401:
                print('[!] Wrong username or password :( .')
                sys.exit(1)

        except Exception as ex:
            print('[!] Error when trying to authenticate.')
            traceback.print_exc(file=sys.stdout)
            sys.exit(1)

    def create_project(self, project, key):

        #https://developer.atlassian.com/cloud/jira/platform/rest/v3/#api-rest-api-3-project-post -> this did not work for me.
        #found this endpoint using chrome dev tools.
        print("[*] Creating the Att&ck project...")
        headers = {'Content-Type': 'application/json'}

        project_dict = {
            'key': key,
            'name': project,
            'templateKey': "com.pyxis.greenhopper.jira:gh-simplified-basic",
        }
        try:
            r = requests.post(self.url + '/rest/simplified/latest/project', json=project_dict, headers=headers, auth=(self.username, self.apitoken), verify=False)
            if r.status_code == 200:
                print("[!] Success!")

            elif r.status_code == 401:
                print('[!] Unauthorized. Probably not enough permissions :(')
                sys.exit(1)

            else:
                print('[!] Error creating Jira project. Does it already exist ?')
                sys.exit(1)

        except Exception as ex:
            print ("[!] Error creating Jira project")
            traceback.print_exc(file=sys.stdout)
            sys.exit(1)

    def create_custom_fields(self):

        # avoid creating the custom fields more than once
        if not self.do_custom_fields_exist():
            print("[*] Creating custom fields ...")
            headers = {'Content-Type': 'application/json'}
            try:

                custom_fields=[]
                custom_field1_dict = {
                    "searcherKey": "com.atlassian.jira.plugin.system.customfieldtypes:multiselectsearcher",
                    "name": "Tactic",
                    "description": "Attack Tactic",
                    "type": "com.atlassian.jira.plugin.system.customfieldtypes:select"
                }
                custom_fields.append(custom_field1_dict)

                custom_field2_dict = {
                    "searcherKey": "com.atlassian.jira.plugin.system.customfieldtypes:multiselectsearcher",
                    "name": "CTI",
                    "description": "CTI ATT&CK Map",
                    "type": "com.atlassian.jira.plugin.system.customfieldtypes:select"
                }
                custom_fields.append(custom_field2_dict)
                
                custom_field3_dict = {
                    "searcherKey": "com.atlassian.jira.plugin.system.customfieldtypes:multiselectsearcher",
                    "name": "Detection",
                    "description": "Detection ATT&CK Map",
                    "type": "com.atlassian.jira.plugin.system.customfieldtypes:select"
                }
                custom_fields.append(custom_field3_dict)
                
                custom_field4_dict = {
                    "searcherKey": "com.atlassian.jira.plugin.system.customfieldtypes:multiselectsearcher",
                    "name": "Hunt",
                    "description": "Hunt ATT&CK Map",
                    "type": "com.atlassian.jira.plugin.system.customfieldtypes:select"
                }
                custom_fields.append(custom_field4_dict)
                
                custom_field5_dict = {
                    "searcherKey": "com.atlassian.jira.plugin.system.customfieldtypes:multiselectsearcher",
                    "name": "Maturity",
                    "description": "Maturity ATT&CK Map",
                    "type": "com.atlassian.jira.plugin.system.customfieldtypes:select"
                }
                custom_fields.append(custom_field5_dict)
                
                custom_field6_dict = {
                    "searcherKey": "com.atlassian.jira.plugin.system.customfieldtypes:multiselectsearcher",
                    "name": "NIST",
                    "description": "NIST ATT&CK Map",
                    "type": "com.atlassian.jira.plugin.system.customfieldtypes:select"
                }
                custom_fields.append(custom_field6_dict)
                
                custom_field7_dict = {
                    "searcherKey": "com.atlassian.jira.plugin.system.customfieldtypes:multiselectsearcher",
                    "name": "Purple",
                    "description": "Purple ATT&CK Map",
                    "type": "com.atlassian.jira.plugin.system.customfieldtypes:select"
                }
                custom_fields.append(custom_field7_dict)
                
                custom_field8_dict = {
                    "searcherKey": "com.atlassian.jira.plugin.system.customfieldtypes:multiselectsearcher",
                    "name": "Red",
                    "description": "Red ATT&CK Map",
                    "type": "com.atlassian.jira.plugin.system.customfieldtypes:select"
                }
                custom_fields.append(custom_field8_dict)

                custom_field9_dict = {
                    "searcherKey": "com.atlassian.jira.plugin.system.customfieldtypes:exacttextsearcher",
                    "name": "Url",
                    "description": "Attack Technique Url",
                    "type": "com.atlassian.jira.plugin.system.customfieldtypes:url"
                }
                custom_fields.append(custom_field9_dict)

                custom_field10_dict = {
                    "searcherKey": "com.atlassian.jira.plugin.system.customfieldtypes:multiselectsearcher",
                    "name": "Datasources",
                    "description": "Data Sources",
                    "type": "com.atlassian.jira.plugin.system.customfieldtypes:multiselect"
                }
                custom_fields.append(custom_field10_dict)

                custom_field11_dict = {
                    "searcherKey": "com.atlassian.jira.plugin.system.customfieldtypes:textsearcher",
                    "name": "Id",
                    "description": "Technique Id",
                    "type": "com.atlassian.jira.plugin.system.customfieldtypes:textfield"
                }
                custom_fields.append(custom_field11_dict)

                custom_field12_dict = {
                    "searcherKey": "com.atlassian.jira.plugin.system.customfieldtypes:textsearcher",
                    "name": "Sub-Technique of",
                    "description": "Parent Technique Id",
                    "type": "com.atlassian.jira.plugin.system.customfieldtypes:textfield"
                }
                custom_fields.append(custom_field12_dict)

                for custom_field in custom_fields:
                    r = requests.post(self.url + '/rest/api/3/field', json=custom_field, headers=headers, auth=(self.username, self.apitoken), verify=False)

                    if r.status_code == 201:
                        print("\t [!] Successfully created \'"+custom_field['name']+"\' custom field.")

                    elif r.status_code == 401:
                        print('[!] Unauthorized. Probably not enough permissions :(')
                        sys.exit(1)

                    else:
                        print ("[!] Error creating custom fields")
                        sys.exit(1)


            except Exception as ex:
                traceback.print_exc(file=sys.stdout)
                sys.exit(1)

        else:
            print('[!] Found custom fields')

    def add_custom_field_options(self):

        custom_fields = self.get_custom_fields()
        headers = {'Content-Type': 'application/json'}
        try:

            # cti field options
            payload=[{"name":"Not Tracked"},{"name":"Initial"},{"name":"Defined"},{"name":"Resilient"},{"name":"Optimized"}]
            r=requests.post(self.url + '/rest/globalconfig/1/customfieldoptions/'+custom_fields['CTI'], headers=headers, json= payload, auth=(self.username, self.apitoken),verify=False)
            if r.status_code != 204:
                print("[!] Error creating options for the CTI custom field.")
                sys.exit()
    
            # detection field options
            payload=[{"name":"Not Tracked"},{"name":"Initial"},{"name":"Defined"},{"name":"Resilient"},{"name":"Optimized"}]
            r=requests.post(self.url + '/rest/globalconfig/1/customfieldoptions/'+custom_fields['Detection'], headers=headers, json= payload, auth=(self.username, self.apitoken),verify=False)
            if r.status_code != 204:
                print("[!] Error creating options for the Detection custom field.")
                sys.exit()

           # hunt field options
            payload=[{"name":"Not Tracked"},{"name":"Initial"},{"name":"Defined"},{"name":"Resilient"},{"name":"Optimized"}]
            r=requests.post(self.url + '/rest/globalconfig/1/customfieldoptions/'+custom_fields['Hunt'], headers=headers, json= payload, auth=(self.username, self.apitoken),verify=False)
            if r.status_code != 204:
                print("[!] Error creating options for the Hunt custom field.")
                sys.exit()

            # maturity field options
            payload=[{"name":"Not Tracked"},{"name":"Initial"},{"name":"Defined"},{"name":"Resilient"},{"name":"Optimized"}]
            r=requests.post(self.url + '/rest/globalconfig/1/customfieldoptions/'+custom_fields['Maturity'], headers=headers, json= payload, auth=(self.username, self.apitoken),verify=False)
            if r.status_code != 204:
                print("[!] Error creating options for the Maturity custom field.")
                sys.exit()

            # nist field options
            payload=[{"name":"Not Tracked"},{"name":"Initial"},{"name":"Defined"},{"name":"Resilient"},{"name":"Optimized"}]
            r=requests.post(self.url + '/rest/globalconfig/1/customfieldoptions/'+custom_fields['NIST'], headers=headers, json= payload, auth=(self.username, self.apitoken),verify=False)
            if r.status_code != 204:
                print("[!] Error creating options for the NIST custom field.")
                sys.exit()

            # purple field options
            payload=[{"name":"Not Tracked"},{"name":"Initial"},{"name":"Defined"},{"name":"Resilient"},{"name":"Optimized"}]
            r=requests.post(self.url + '/rest/globalconfig/1/customfieldoptions/'+custom_fields['Purple'], headers=headers, json= payload, auth=(self.username, self.apitoken),verify=False)
            if r.status_code != 204:
                print("[!] Error creating options for the Purple custom field.")
                sys.exit()
  
            # red field options
            payload=[{"name":"Not Tracked"},{"name":"Initial"},{"name":"Defined"},{"name":"Resilient"},{"name":"Optimized"}]
            r=requests.post(self.url + '/rest/globalconfig/1/customfieldoptions/'+custom_fields['Red'], headers=headers, json= payload, auth=(self.username, self.apitoken),verify=False)
            if r.status_code != 204:
                print("[!] Error creating options for the Red custom field.")
                sys.exit()

            # tactic field options
            payload = self.get_attack_tactics()
            r = requests.post(self.url + '/rest/globalconfig/1/customfieldoptions/' + custom_fields['Tactic'], headers=headers, json=payload, auth=(self.username, self.apitoken), verify=False)
            if r.status_code != 204:
                print("[!] Error creating options for the tactic custom field.")
                sys.exit()

            # data source field options
            payload = self.get_attack_datasources()
            r = requests.post(self.url + '/rest/globalconfig/1/customfieldoptions/' + custom_fields['Datasources'], headers=headers, json=payload, auth=(self.username, self.apitoken), verify=False)
            if r.status_code != 204:
                print("[!] Error creating options for the datasources custom field.")
                sys.exit()


        except Exception as ex:
            traceback.print_exc(file=sys.stdout)
            sys.exit()

    def get_custom_fields(self):

        #print("[*] Getting custom field ids ...")
        custom_fields=['Tactic','CTI','Detection','Hunt','Maturity','NIST','Purple','Red','Url','Datasources','Id','Sub-Technique of']
        headers = {'Content-Type': 'application/json'}
        resp = {}

        try:
            r = requests.get(self.url + '/rest/api/3/field', headers=headers, auth=(self.username, self.apitoken), verify=False)
            if r.status_code == 200:
                results = r.json()
                for r in results:
                    if r['name'] in custom_fields:
                        resp.update({r['name']:r['id']})

            else:
                print("[!] Error getting custom fields")
                sys.exit(1)

            return resp


        except Exception as ex:
            traceback.print_exc(file=sys.stdout)
            sys.exit(1)

    def hide_unwanted_fields_old(self,key):
    # Deprecated, keeping in just in case.
        print("[*] Hiding unnecessary fields from ATTACK's issue layout...")
        screen_tab_ids = self.get_screen_tabs(key)
        headers = {'Content-Type': 'application/json'}

        #json_string = u'{"contextItemsCategories":{"primary":[{"id":"assignee","type":"FIELD"},{"id":"labels","type":"FIELD"}],"secondary":[{"id":"priority","type":"FIELD"}],"alwaysHidden":[{"id":"reporter","type":"FIELD"},{"id":"devSummary","type":"DEV_SUMMARY"},{"id":"releases","type":"RELEASES_PANEL"},{"id":"customfield_10041","type":"FIELD"},{"id":"timeoriginalestimate","type":"FIELD"},{"id":"customfield_10014","type":"FIELD"},{"id":"components","type":"FIELD"},{"id":"fixVersions","type":"FIELD"},{"id":"duedate","type":"FIELD"},{"id":"customfield_10011","type":"FIELD"},{"id":"timetracking","type":"FIELD"}]},"contentItemsCategories":{"visible":[{"id":"description","type":"FIELD"}],"alwaysHidden":[]}}'
        #json_string = u'{"contextItemsCategories":{"primary":[{"id":"assignee","type":"FIELD"}],"secondary":[{"id":"priority","type":"FIELD"},{"id":"labels","type":"FIELD"}],"alwaysHidden":[{"id":"reporter","type":"FIELD"},{"id":"devSummary","type":"DEV_SUMMARY"},{"id":"releases","type":"RELEASES_PANEL"},{"id":"customfield_10041","type":"FIELD"},{"id":"timeoriginalestimate","type":"FIELD"},{"id":"customfield_10014","type":"FIELD"},{"id":"components","type":"FIELD"},{"id":"fixVersions","type":"FIELD"},{"id":"duedate","type":"FIELD"},{"id":"customfield_10011","type":"FIELD"},{"id":"timetracking","type":"FIELD"}]},"contentItemsCategories":{"visible":[{"id":"description","type":"FIELD"}],"alwaysHidden":[]}}'
        json_string = u'{"contextItemsCategories":{"primary":[{"id":"assignee","type":"FIELD"}],"secondary":[{"id":"labels","type":"FIELD"}],"alwaysHidden":[{"id":"priority","type":"FIELD"},{"id":"reporter","type":"FIELD"},{"id":"devSummary","type":"DEV_SUMMARY"},{"id":"releases","type":"RELEASES_PANEL"},{"id":"customfield_10041","type":"FIELD"},{"id":"timeoriginalestimate","type":"FIELD"},{"id":"customfield_10014","type":"FIELD"},{"id":"components","type":"FIELD"},{"id":"fixVersions","type":"FIELD"},{"id":"duedate","type":"FIELD"},{"id":"customfield_10011","type":"FIELD"},{"id":"timetracking","type":"FIELD"}]},"contentItemsCategories":{"visible":[{"id":"description","type":"FIELD"}],"alwaysHidden":[]}}'

        try:
            for screen_tab_id in screen_tab_ids:
                r = requests.put(self.url + '/rest/api/2/project/'+key+'/properties/viewScreenId-'+str(screen_tab_id[0]), data=json_string, headers=headers, auth=(self.username, self.apitoken), verify=False)
            print("[!] Done.")

        except Exception as ex:
            print (ex)
            traceback.print_exc(file=sys.stdout)
            sys.exit(1)
    
    def hide_unwanted_fields(self,key):

        #https://support.atlassian.com/jira-core-cloud/docs/configure-field-layout-in-the-issue-view/
        #https://jira.atlassian.com/browse/JRACLOUD-74697?error=login_required&error_description=Login+required&state=0c1a9f1d-8614-4158-b02e-f06e8706f5d4


        print("[*] Hiding unnecessary fields from ATTACK's issue layout...")
        #screen_tab_ids = self.get_screen_tabs(key)
        project_id=self.get_project_id(key)
        screen_ids = self.get_screen_ids(project_id)
        custom_Fields = self.get_custom_fields()

        headers = {'Content-Type': 'application/json'}

        #json_string = u'{"context":{"primary":[{"id":"assignee","type":"FIELD"},{"id":"reporter","type":"FIELD"},{"id":"devSummary","type":"DEV_SUMMARY"},{"id":"customfield_10094","type":"FIELD"},{"id":"customfield_10092","type":"FIELD"},{"id":"customfield_10090","type":"FIELD"},{"id":"customfield_10093","type":"FIELD"},{"id":"customfield_10091","type":"FIELD"},{"id":"labels","type":"FIELD"}],"secondary":[{"id":"priority","type":"FIELD"}],"alwaysHidden":[{"id":"timeoriginalestimate","type":"FIELD"},{"id":"timetracking","type":"FIELD"},{"id":"components","type":"FIELD"},{"id":"fixVersions","type":"FIELD"},{"id":"customfield_10014","type":"FIELD"},{"id":"duedate","type":"FIELD"},{"id":"customfield_10011","type":"FIELD"},{"id":"customfield_10026","type":"FIELD"}]},"content":{"visible":[{"id":"description","type":"FIELD"}],"alwaysHidden":[]}}'
        json_string = u'{"context":{"primary":[{"id":"assignee","type":"FIELD"},{"id":"reporter","type":"FIELD"},{"id":"labels","type":"FIELD"},{"id":"CTI_CUSTOMFIELD","type":"FIELD"},{"id":"DETECTION_CUSTOMFIELD","type":"FIELD"},{"id":"HUNT_CUSTOMFIELD","type":"FIELD"},{"id":"MATURITY_CUSTOMFIELD","type":"FIELD"},{"id":"NIST_CUSTOMFIELD","type":"FIELD"},{"id":"PURPLE_CUSTOMFIELD","type":"FIELD"},{"id":"RED_CUSTOMFIELD","type":"FIELD"},{"id":"DATASOURCE_CUSTOMFIELD","type":"FIELD"}],"secondary":[{"id":"priority","type":"FIELD"}],"alwaysHidden":[{"id":"timeoriginalestimate","type":"FIELD"},{"id":"timetracking","type":"FIELD"},{"id":"components","type":"FIELD"},{"id":"fixVersions","type":"FIELD"},{"id":"customfield_10014","type":"FIELD"},{"id":"duedate","type":"FIELD"},{"id":"customfield_10011","type":"FIELD"},{"id":"customfield_10026","type":"FIELD"},{"id":"devSummary","type":"DEV_SUMMARY"}]},"content":{"visible":[{"id":"TACTIC_CUSTOMFIELD","type":"FIELD"},{"id":"ID_CUSTOMFIELD","type":"FIELD"},{"id":"URL_CUSTOMFIELD","type":"FIELD"},{"id":"SUBTECHNIQUE_CUSTOMFIELD","type":"FIELD"},{"id":"description","type":"FIELD"}],"alwaysHidden":[]}}'        
        
        json_string = json_string.replace("DATASOURCE_CUSTOMFIELD", custom_Fields['Datasources'])
        json_string = json_string.replace("ID_CUSTOMFIELD", custom_Fields['Id'])
        json_string = json_string.replace("TACTIC_CUSTOMFIELD", custom_Fields['Tactic'])
        json_string = json_string.replace("CTI_CUSTOMFIELD", custom_Fields['CTI'])
        json_string = json_string.replace("DETECTION_CUSTOMFIELD", custom_Fields['Detection'])
        json_string = json_string.replace("HUNT_CUSTOMFIELD", custom_Fields['Hunt'])
        json_string = json_string.replace("MATURITY_CUSTOMFIELD", custom_Fields['Maturity'])
        json_string = json_string.replace("NIST_CUSTOMFIELD", custom_Fields['NIST'])
        json_string = json_string.replace("PURPLE_CUSTOMFIELD", custom_Fields['Purple'])
        json_string = json_string.replace("RED_CUSTOMFIELD", custom_Fields['Red'])
        json_string = json_string.replace("URL_CUSTOMFIELD", custom_Fields['Url'])
        json_string = json_string.replace("SUBTECHNIQUE_CUSTOMFIELD", custom_Fields['Sub-Technique of'])

        try:
            for screen_id in screen_ids:
                r = requests.put(self.url + '/rest/issuedetailslayout/config/classic/screen?projectIdOrKey='+key+'&screenId='+str(screen_id), data=json_string, headers=headers, auth=(self.username, self.apitoken), verify=False)
            print("[!] Done.")

        except Exception as ex:
            print (ex)
            traceback.print_exc(file=sys.stdout)
            sys.exit(1)


    def do_custom_fields_exist(self):

        custom_fields = self.get_custom_fields()

        ## TODO: Need to perform better checks but this works for now.
        if len(custom_fields.keys()) == 12:
            return True
        else:
            return False


    def create_issue(self, issue_dict, id):

        # good examples https://developer.atlassian.com/server/jira/platform/jira-rest-api-examples/#creating-an-issue-examples
        headers = {'Content-Type': 'application/json'}
        try:
            r = requests.post(self.url + '/rest/api/2/issue', json=issue_dict, headers=headers, auth=(self.username, self.apitoken), verify=False)

            if r.status_code == 201:
                print ("\t[!] Successfully created Jira issue for "+id)
                return json.loads(r.text)
            else:
                print ("\t[!] Error creating Jira issue for "+id)
                print (r.text)
                sys.exit()

        except Exception as ex:

            print(ex)
            traceback.print_exc(file=sys.stdout)
            sys.exit()


    def get_attack_screens(self, key):

        headers = {'Content-Type': 'application/json'}
        screen_ids=[]
        try:
            r = requests.get(self.url + '/rest/api/3/screens', headers=headers, auth=(self.username, self.apitoken), verify=False)

            if r.status_code == 200:
                results = r.json()['values']
                for r in results:
                    if key in r['name'] and "Default Issue Screen" in r['name']:
                        screen_ids.append(r['id'])
            else:
                print("[!] Error obtaining screens")
                sys.exit(1)

            return screen_ids

        except Exception as ex:
            traceback.print_exc(file=sys.stdout)
            sys.exit()

    def get_screen_tabs(self, key):

        # deprecated, keeping it in codebase just in case.
        headers = {'Content-Type': 'application/json'}
        screen_ids = self.get_attack_screens(key)
        screen_tab_ids=[]
        try:
            for screen_id in screen_ids:

                r = requests.get(self.url + '/rest/api/3/screens/'+str(screen_id)+'/tabs', headers=headers, auth=(self.username, self.apitoken), verify=False)
                if r.status_code == 200:
                    for result in r.json():
                        screen_tab_ids.append([screen_id, result['id']])
                else:
                    print("[!] Error obtaining screen tabs")
                    sys.exit(1)

            return screen_tab_ids

        except Exception as ex:
            traceback.print_exc(file=sys.stdout)
            sys.exit()


    def add_custom_field_to_screen_tab_old(self, key):
        # deprecated. keeping it in codebase just in case

        print("[*] Adding custom fields to ATTACK's default screen tab ...")
        headers = {'Content-Type': 'application/json'}
        screen_tab_ids = self.get_screen_tabs(key)
        custom_fields = self.get_custom_fields()

        try:
            for key in custom_fields.keys():
                for screen_tab_id in screen_tab_ids:
                    custom_field_dict = {'fieldId': custom_fields[key]}
                    #print (self.url + '/rest/api/2/screens/'+str(screen_tab_id[0])+'/tabs/'+str(screen_tab_id[1])+'/fields')
                    r = requests.post(self.url + '/rest/api/3/screens/'+str(screen_tab_id[0])+'/tabs/'+str(screen_tab_id[1])+'/fields', json = custom_field_dict, headers=headers, auth=(self.username, self.apitoken), verify=False)

            print("[!] Done!.")

        except Exception as ex:
            traceback.print_exc(file=sys.stdout)
            sys.exit()

    def get_technique_cti(self):

        print("[*] Getting issues from the ATTACK project...")
        custom_fields = self.get_custom_fields()
        headers = {'Content-Type': 'application/json'}
        read_issues=0
        startAt=0
        res_dict=dict()

        try:

            while(True):
                #print("Entering while loop. startAt is "+str(startAt))
                r = requests.get(self.url + '/rest/api/3/search?jql=project%20%3D%20ATTACK&startAt='+str(startAt), headers=headers, auth=(self.username, self.apitoken), verify=False)
                resp_dict = r.json()
                for issue in resp_dict['issues']:
                    technique_id = issue['fields'][custom_fields['Id']]
                    #print (issue['fields']['summary']," ",issue['fields'][custom_fields['CTI']] )
                    #print(technique_id, " ", issue['fields'][custom_fields['CTI']])
                    res_dict.update({technique_id:issue['fields'][custom_fields['CTI']]})                   
                read_issues+=50
                startAt+=50
                if (read_issues>=r.json()['total']):
                    break

            return res_dict

        except Exception as ex:
            traceback.print_exc(file=sys.stdout)
            sys.exit()

            
    def get_technique_detection(self):

        print("[*] Getting issues from the ATTACK project...")
        custom_fields = self.get_custom_fields()
        headers = {'Content-Type': 'application/json'}
        read_issues=0
        startAt=0
        res_dict=dict()

        try:

            while(True):
                #print("Entering while loop. startAt is "+str(startAt))
                r = requests.get(self.url + '/rest/api/3/search?jql=project%20%3D%20ATTACK&startAt='+str(startAt), headers=headers, auth=(self.username, self.apitoken), verify=False)
                resp_dict = r.json()
                for issue in resp_dict['issues']:
                    technique_id = issue['fields'][custom_fields['Id']]
                    #print (issue['fields']['summary']," ",issue['fields'][custom_fields['Detection']] )
                    #print(technique_id, " ", issue['fields'][custom_fields['Detection']])
                    res_dict.update({technique_id:issue['fields'][custom_fields['Detection']]})
                read_issues+=50
                startAt+=50
                if (read_issues>=r.json()['total']):
                    break

            return res_dict

        except Exception as ex:
            traceback.print_exc(file=sys.stdout)
            sys.exit()

            
    def get_technique_hunt(self):

        print("[*] Getting issues from the ATTACK project...")
        custom_fields = self.get_custom_fields()
        headers = {'Content-Type': 'application/json'}
        read_issues=0
        startAt=0
        res_dict=dict()

        try:

            while(True):
                #print("Entering while loop. startAt is "+str(startAt))
                r = requests.get(self.url + '/rest/api/3/search?jql=project%20%3D%20ATTACK&startAt='+str(startAt), headers=headers, auth=(self.username, self.apitoken), verify=False)
                resp_dict = r.json()
                for issue in resp_dict['issues']:
                    technique_id = issue['fields'][custom_fields['Id']]
                    #print (issue['fields']['summary']," ",issue['fields'][custom_fields['Hunt']] )
                    #print(technique_id, " ", issue['fields'][custom_fields['Hunt']])
                    res_dict.update({technique_id:issue['fields'][custom_fields['Hunt']]})
                read_issues+=50
                startAt+=50
                if (read_issues>=r.json()['total']):
                    break

            return res_dict

        except Exception as ex:
            traceback.print_exc(file=sys.stdout)
            sys.exit()
            
            
    def get_technique_maturity(self):

        print("[*] Getting issues from the ATTACK project...")
        custom_fields = self.get_custom_fields()
        headers = {'Content-Type': 'application/json'}
        read_issues=0
        startAt=0
        res_dict=dict()

        try:

            while(True):
                #print("Entering while loop. startAt is "+str(startAt))
                r = requests.get(self.url + '/rest/api/3/search?jql=project%20%3D%20ATTACK&startAt='+str(startAt), headers=headers, auth=(self.username, self.apitoken), verify=False)
                resp_dict = r.json()
                for issue in resp_dict['issues']:
                    technique_id = issue['fields'][custom_fields['Id']]
                    #print (issue['fields']['summary']," ",issue['fields'][custom_fields['Maturity']] )
                    #print(technique_id, " ", issue['fields'][custom_fields['Maturity']])
                    res_dict.update({technique_id:issue['fields'][custom_fields['Maturity']]})
                read_issues+=50
                startAt+=50
                if (read_issues>=r.json()['total']):
                    break

            return res_dict

        except Exception as ex:
            traceback.print_exc(file=sys.stdout)
            sys.exit()

    def get_technique_nist(self):

        print("[*] Getting issues from the ATTACK project...")
        custom_fields = self.get_custom_fields()
        headers = {'Content-Type': 'application/json'}
        read_issues=0
        startAt=0
        res_dict=dict()

        try:

            while(True):
                #print("Entering while loop. startAt is "+str(startAt))
                r = requests.get(self.url + '/rest/api/3/search?jql=project%20%3D%20ATTACK&startAt='+str(startAt), headers=headers, auth=(self.username, self.apitoken), verify=False)
                resp_dict = r.json()
                for issue in resp_dict['issues']:
                    technique_id = issue['fields'][custom_fields['Id']]
                    #print (issue['fields']['summary']," ",issue['fields'][custom_fields['NIST']] )
                    #print(technique_id, " ", issue['fields'][custom_fields['NIST']])
                    res_dict.update({technique_id:issue['fields'][custom_fields['NIST']]})
                read_issues+=50
                startAt+=50
                if (read_issues>=r.json()['total']):
                    break

            return res_dict

        except Exception as ex:
            traceback.print_exc(file=sys.stdout)
            sys.exit()
            
            
    def get_technique_purple(self):

        print("[*] Getting issues from the ATTACK project...")
        custom_fields = self.get_custom_fields()
        headers = {'Content-Type': 'application/json'}
        read_issues=0
        startAt=0
        res_dict=dict()

        try:

            while(True):
                #print("Entering while loop. startAt is "+str(startAt))
                r = requests.get(self.url + '/rest/api/3/search?jql=project%20%3D%20ATTACK&startAt='+str(startAt), headers=headers, auth=(self.username, self.apitoken), verify=False)
                resp_dict = r.json()
                for issue in resp_dict['issues']:
                    technique_id = issue['fields'][custom_fields['Id']]
                    #print (issue['fields']['summary']," ",issue['fields'][custom_fields['Purple']] )
                    #print(technique_id, " ", issue['fields'][custom_fields['Purple']])
                    res_dict.update({technique_id:issue['fields'][custom_fields['Purple']]})
                read_issues+=50
                startAt+=50
                if (read_issues>=r.json()['total']):
                    break

            return res_dict

        except Exception as ex:
            traceback.print_exc(file=sys.stdout)
            sys.exit()
            
            
    def get_technique_red(self):

        print("[*] Getting issues from the ATTACK project...")
        custom_fields = self.get_custom_fields()
        headers = {'Content-Type': 'application/json'}
        read_issues=0
        startAt=0
        res_dict=dict()

        try:

            while(True):
                #print("Entering while loop. startAt is "+str(startAt))
                r = requests.get(self.url + '/rest/api/3/search?jql=project%20%3D%20ATTACK&startAt='+str(startAt), headers=headers, auth=(self.username, self.apitoken), verify=False)
                resp_dict = r.json()
                for issue in resp_dict['issues']:
                    technique_id = issue['fields'][custom_fields['Id']]
                    #print (issue['fields']['summary']," ",issue['fields'][custom_fields['Red']] )
                    #print(technique_id, " ", issue['fields'][custom_fields['Red']])
                    res_dict.update({technique_id:issue['fields'][custom_fields['Red']]})
                read_issues+=50
                startAt+=50
                if (read_issues>=r.json()['total']):
                    break

            return res_dict

        except Exception as ex:
            traceback.print_exc(file=sys.stdout)
            sys.exit()
            
            
            
    def get_attack_datasources(self):
    
        try:
            datasource_payload=[]
            client = attack_client()

            #the datasources obtained via the line below do not correspond with the data sources being present in get_attack_techniques()
            #datasources = client.get_data_sources()

            #this is likely a temporary workaround
            data_sources_legacy = []
            techniques = client.get_techniques()
            for technique in techniques:
                try:
                    data_sources_field = technique['x_mitre_data_sources']
                except:
                    pass
                for ds in data_sources_field:
                    data_sources_legacy.append(str(ds).title())
            #making data_sources_legacy records unique
            data_sources_legacy = list(set(data_sources_legacy))
            # end of the workaround
            for datasource in data_sources_legacy:
                d = {'name': datasource}
                datasource_payload.append(d)
            return datasource_payload

        except:
            traceback.print_exc(file=sys.stdout)
            print ("[!] Error connecting obtaining datasources from Att&ck's API !")
            sys.exit()

    def get_attack_tactics(self):

        try:
            tactics_payload=[]
            client = attack_client()
            enterprise_tactics = client.get_enterprise()
            tactics = [tactic['name'].lower().replace(" ", "-") for tactic in enterprise_tactics['tactics']]
            for tactic in tactics:
                tactics_payload.append({"name": tactic})
            return tactics_payload

        except:
            traceback.print_exc(file=sys.stdout)
            print ("[!] Error connecting obtaining tactics from Att&ck's API !")
            sys.exit()

    def add_custom_fields_to_screen(self, key):

        print("[*] Adding custom fields to ATTACK's default screen tab ...")
        headers = {'Content-Type': 'application/json'}
        project_id=self.get_project_id(key)
        screen_tab_ids = self.get_screen_tab_ids(project_id)
        screen_ids = self.get_screen_ids(project_id)
        custom_fields = self.get_custom_fields()

        try:
            for key in custom_fields.keys():
                for i in range(1):
                    custom_field_dict = {'fieldId': custom_fields[key]}
                    #print (self.url + '/rest/api/2/screens/'+str(screen_tab_id[0])+'/tabs/'+str(screen_tab_id[1])+'/fields')
                    r = requests.post(self.url + '/rest/api/3/screens/'+str(screen_ids[i])+'/tabs/'+str(screen_tab_ids[i])+'/fields', json = custom_field_dict, headers=headers, auth=(self.username, self.apitoken), verify=False)

            print("[!] Done!.")

        except Exception as ex:
            traceback.print_exc(file=sys.stdout)
            sys.exit()

    def get_project_id(self,key):
        headers = {'Content-Type': 'application/json'}
        try:
            r = requests.get(self.url + '/rest/api/3/project/search', headers=headers, auth=(self.username, self.apitoken), verify=False)
            resp_dict = r.json()
            for project in resp_dict['values']:
                if project['key'] == key:
                    return project['id']
            return 0
                
        except:
            traceback.print_exc(file=sys.stdout)
            print ("[!] Error obtaining project id!")
            sys.exit()

    def get_screen_ids(self, project_id):
        headers = {'Content-Type': 'application/json'}
        screen_scheme_ids = self.get_screen_scheme_ids(project_id)
        screen_ids = []
        try:
            for item in screen_scheme_ids:
                r = requests.get(self.url +'/rest/api/2/screenscheme?id='+item, headers=headers, auth=(self.username, self.apitoken),verify=False)
                r_dict = r.json()
                screen_ids.append(list(r_dict['values'][0]['screens'].values())[0])
            return screen_ids

        except:
            traceback.print_exc(file=sys.stdout)
            print ("[!] Error obtaining screen ids!")
            sys.exit()


    def get_screen_scheme_ids(self, project_id):
        headers = {'Content-Type': 'application/json'}
        issue_type_screen_scheme_ids = self.get_project_issue_type_screen_scheme_ids(project_id)
        request_items=[]
        screen_scheme_ids=[]
        try:
            for item in issue_type_screen_scheme_ids:
                r = requests.get(self.url +'/rest/api/2/issuetypescreenscheme/mapping?issueTypeScreenSchemeId=' + item, headers=headers, auth=(self.username, self.apitoken), verify=False)
                r_dict=r.json()
                request_items.append(r_dict)
            for item in request_items:
                for subitem in item['values']:
                    screen_scheme_ids.append(subitem['screenSchemeId'])
            return  screen_scheme_ids
        
        except:
            traceback.print_exc(file=sys.stdout)
            print ("[!] Error obtaining screen scheme ids!")
            sys.exit()

    
    def get_project_issue_type_screen_scheme_ids(self, project_id):
        headers = {'Content-Type': 'application/json'}
        query={'projectId': project_id}
        issue_type_screen_scheme_ids=[]
        try:
            r = requests.get(self.url +'/rest/api/3/issuetypescreenscheme/project/', headers=headers, params=query, auth=(self.username, self.apitoken), verify=False) 
            resp_dict = r.json()
            for item in resp_dict['values']:
                issue_type_screen_scheme_ids.append(item['issueTypeScreenScheme']['id'])

            return issue_type_screen_scheme_ids

        except:
            traceback.print_exc(file=sys.stdout)
            print ("[!] Error obtaining issue type screen scheme ids!")
            sys.exit()
    
    
    def get_screen_tab_ids(self, project_id):
        screen_ids = self.get_screen_ids(project_id)
        screen_tab_ids = []
        try:
            for item in screen_ids:
                screen_tab_id = self.get_screen_tab_id(item)
                screen_tab_ids.append(screen_tab_id)
            return screen_tab_ids

        except:
            traceback.print_exc(file=sys.stdout)
            print ("[!] Error obtaining screen tab ids!")
            sys.exit()


    def get_screen_tab_id(self, screen_id):
        headers = {'Content-Type': 'application/json'}
        try:
            r = requests.get(self.url +'/rest/api/3/screens/'+str(screen_id)+'/tabs', headers=headers, auth=(self.username, self.apitoken), verify=False) 
            resp_dict = r.json()
            return resp_dict[0]['id']

        except:
            traceback.print_exc(file=sys.stdout)
            print ("[!] Error obtaining screen/tab ids!")
            sys.exit()
            
            
    def get_project_screen_tab_ids(self, project_id):
    #legacy - not used in the current version
        headers = {'Content-Type': 'application/json'}
        screen_tab_ids=[]
        try:
            r = requests.get(self.url +'/rest/api/3/issuetypescreenscheme/mapping?issueTypeScreenSchemeId='+project_id,headers=headers, auth=(self.username, self.apitoken), verify=False) 
            resp_dict = r.json()
            for screen in resp_dict['values']:
                screen_tab_ids.append([screen['screenSchemeId'], self.get_screen_tab_id(screen['screenSchemeId'])])

            return screen_tab_ids

        except:
            traceback.print_exc(file=sys.stdout)
            print ("[!] Error obtaining screen/tab ids!")
            sys.exit()