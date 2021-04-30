# attack2jira

The MITRE ATT&CK Framework is a great tool security teams can leverage to, among many other things, measure the security posture of an organization against tactics and techniques used in the wild by real threat actors.

At the time of writing, ATT&CK covers 266 Techniques across 12 Tactics. If done manually, tracking this posture's state over time can become a tedious and challenging task. Blue/Purple teams require the proper tools that allow them to efficiently tackle this challenge and focus on whats important.

attack2jira automates the process of standing up a Jira environment that can be used to track and measure ATT&CK coverage. No more spreadsheets !

Visit the Wiki to view the [Demos](https://github.com/mvelazc0/attack2jira/wiki/Demos). attack2jira was first presented at [ATT&CKCon 2.0](https://www.youtube.com/watch?v=hrzR8TpnjAw&t=1198s). For more context, read this [blog post](https://medium.com/@mvelazco/tracking-and-measuring-att-ck-coverage-with-attack2jira-fe700e2a1654).

To allow the community to experiment with this approach, I created a Jira instance hosting the ATTACK project with attack2jira: [https://attack.atlassian.net](https://attack.atlassian.net/projects/ATT/issues)

attack2jira was designed to be used with Jira Cloud. Specifically, [Jira Software](https://www.atlassian.com/software). 

Tested on Kali Linux 2018.4 and Windows 10 1830 under Python 3.6 and Python 3.7.

## Quick Start Guide

### Installation

```
$ git clone https://github.com/mvelazc0/attack2jira.git
$ pip3 install -r attack2jira/requirements.txt
```
 ### Jira Software
 
 - You will need a [Jira Software Cloud](https://www.atlassian.com/software) environment.
 - You can set up a [free trial](https://www.atlassian.com/software/jira/free) environment for up to 10 users [here](https://www.atlassian.com/try/cloud/signup?bundle=jira-software&edition=free). 
 - Admin access is required

### Usage
 
 Print the help menu
  ```
 $ python3 attack2jira.py -h
 ```
 Create the Jira ATTACK project and issues
 ```
 $ python3 attack2jira.py -url https://yourjiracloud.atlassian.net -u user@domain.com -a initialize
 ```
  Create the Jira ATTACK project with custom project and key 
 ```
 $ python3 attack2jira.py -url https://yourjiracloud.atlassian.net -u user@domain.com -a initialize -p 'ATTACK Coverage' -k ATT
 ```
 Create a Jira Kanban board on existing project and issues
 ```
 $ python3 attack2jira.py -url https://yourjiracloud.atlassian.net -u user@domain.com -a board 
 ```
 >It will then prompt you for the [FilterID](https://community.atlassian.com/t5/Jira-questions/Where-to-find-Filter-ID/qaq-p/81945) and BoardID (if there is not an existing board you'd like to add the tickets to, it will create one for you if you leave blank).
 Reminder: FilterIDs are neccesary because it specifies the filter for the board. They could be like Select * from PROJECTNAME or you can also specify them to only contain "MITRE".

 Export an ATTACK Navigator JSON layer
 ```
 $ python3 attack2jira.py -url https://yourjiracloud.atlassian.net -u user@domain.com -a export
 
 $ python3 attack2jira.py -url https://yourjiracloud.atlassian.net -u user@domain.com -a export -hide
 ```
 
 ## Demo
 
 [![Demo1 @att&ckcon 2019](https://img.youtube.com/vi/2f6AxLtr_3k/0.jpg)](https://www.youtube.com/watch?v=2f6AxLtr_3k)

 
 ## Acknoledgments
 
* [MITRE ATT&CK Framework](https://attack.mitre.org)
* [ATTACK-Python-Client](https://github.com/hunters-forge/ATTACK-Python-Client)
 
 ## Authors

* **Mauricio Velazco** - [@mvelazco](https://twitter.com/mvelazco)
* **Olindo Verrillo** - [@olindoverrillo](https://twitter.com/olindoverrillo)

## License

This project is licensed under the BSD 3-Clause License - see the [LICENSE](LICENSE) file for details
