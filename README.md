# attack2jira
Updated Version Fixing Several Issues


The following issues have been found in jirahandler.py, then addresses and fixed:

1) lower() string method was used on dictionary - previously data likely arrived in string format but it apparently changed

2) overwritten Python "dict" keyword, later creation of dictionary was impossible because of that

3) get_project_screen_tab_ids() function was operating on the old Jira API endpoint
--> it ended up writing several new function to provide the same functionality (projectid -> screentabids translation)

4) it looks like the Attack API currently (Jan 2023) provides inconsistent data:
- datasources obtained via the get_data_sources() function are different than the ones that are returned by get_techniques()
--> that led to errors in creating Jira issues -> completely different set of values of datasources, obtained from get_techniques() was attempted to be mapped on the "datasources" custom field (or more precisely, the field's options to be selected) that had been created based on datasources values taken from get_data_sources() 
