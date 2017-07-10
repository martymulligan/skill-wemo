# Wemo Skill

Detection and control of Wemo devices

## Requirements:
- python2 + pip / development libraries
- [ouimeaux](http://ouimeaux.readthedocs.io/en/latest/) - open source WeMo Control

## Installing:
These have only been tested on a picroft build but
they should basically work on debian flavors generally:
```
cd /PATH/TO/SKILLS/

git clone https://github.com/martymulligan/mycroft-skill-wemo.git

cd mycroft-skill-wemo

source requirements.sh

sudo pip install -r requirements.txt
```


## Current state

Working features:
 - **discover wemo devices** or **discover my devices**
 - **list wemo devices**
 - **toggle *\<device-name\>***


Known issues:
 - None

Up Next:
 - Implement motion devices
 - Implement "On" and "Off" explicitly
