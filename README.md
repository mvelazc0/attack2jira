# attack2jira

The MITRE ATT&CK Framework is a great tool security teams can leverage to, among many other things, measure the security posture of an organization against tactics and techniques used in the wild by real threat actors.

At the time of writing, ATT&CK covers 266 Techniques across 12 Tactics. If done manually, tracking this posture's state over time can become a tedious and challenging task. Blue/Purple teams require the proper tools that allow them to efficiently tackle this challenge and focus on whats important.

attack2jira was first presented at [ATT&CKCCon 2.0](https://www.mitre.org/attackcon). 

## Quick Start Guide

attack2jira has been tested on Kali Linux 2018.4 and Windows 10 1830 under Python 3.6.

### Installation

```
$ git clone https://github.com/mvelazc0/attack2jira.git
$ pip3 install -r attack2jira/requirements.txt
```
 ### Usage
 
 Print the help menu
  ```
 $ python3 attack2jira.py -h
 ```
 
 Create the Jira ATTACK project and issues
 ```
 $ python3 attack2jira.py -url https://attack.atlassian.net -u user@email.com -a initialize
 ```
 Export an ATTACK Navigator JSON layer
 ```
 $ python3 attack2jira.py -url https://attack.atlassian.net -u user@email.com -a export
 
 $ python3 attack2jira.py -url https://attack.atlassian.net -u user@email.com -a export -hide
 ```
 
 ## Authors

* **Mauricio Velazco** - [@mvelazco](https://twitter.com/mvelazco)
* **Olindo Verrillo** - [@olindoverrillo](https://twitter.com/olindoverrillo)

## License

This project is licensed under the BSD 3-Clause License - see the [LICENSE](LICENSE) file for details
