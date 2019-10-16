# attack2jira

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
 ```
 
 ## Authors

* **Mauricio Velazco** - [@mvelazco](https://twitter.com/mvelazco)
* **Olindo Verrillo** - [@olindoverrillo](https://twitter.com/olindoverrillo)

## License

This project is licensed under the BSD 3-Clause License - see the [LICENSE](LICENSE) file for details
