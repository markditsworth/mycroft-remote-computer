# <img src='https://raw.githack.com/FortAwesome/Font-Awesome/master/svgs/solid/desktop.svg' card_color='#000000' width='50' height='50' style='vertical-align:bottom'/> Remote Computer
Control a remote computer via SSH.

## About 
Launch applications, manage your filesystem, turn off your computer by instructing Mycroft.

## Installation
You should be able to install skill via `mycroft-msm install https://github.com/markditsworth/mycroft-remote-computer.git`

## Configuration
You can configure this skill via web interface (home.mycroft.ai). After a few minutes of having the skill installed, you should see configuration options in the https://home.mycroft.ai/#/skill location.

Fill this out with your appropriate information and hit save.

OR

If you desire total privacy, please edit your config file located at:

        ~/.mycroft/mycroft.conf

If it does not exist, create it. This file must be contain a valid json, add the following to it:

        "RemoteComputerSkill": {
            "mac_address": "YOUR COMPUTER's MAC ADDRESS",
            "port": 22,
            "user": "USER NAME",
            "ssh key": "private ssh key file name"
        }  

You will need to modify `__init__.py` to use your preffered directory locations. Copy/tweak the intents to have Mycroft use your preffered applications.
You will also need to ensure your computer's ssh server is up and running and you have it configured for using an RSA key. Copy the private key to your mycroft at `~/.ssh/<key name>`.

It is recommended to use this skill with a Picroft.

## Examples 
* "launch a terminal"
* "create a new project file"
* "open Spyder"
* "open up a Jupyter Notebook"

## Credits
Mark Ditsworth (@markditsworth)

Forked from: 
S. M. Estiaque Ahmed (@smearumi)



## Category
Daily
**IoT**

## Tags
#mycroft
#skill
#remote
#computer
#home
#voice
#assistant
