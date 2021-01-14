# Copyright 2020 M. Ditsworth
#
# Based on original material under the following copyright
#
# Copyright 2018 S. M. Estiaque Ahmed
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import re
import subprocess

# from peg import launchApplicationGrammar
# from tatsu.util import asjson
from adapt.intent import IntentBuilder
from mycroft.skills.core import MycroftSkill
from mycroft.skills.core import intent_handler


class RemoteComputerSkill(MycroftSkill):
    def __init__(self):
        super(RemoteComputerSkill, self).__init__(name="RemoteComputerSkill")
    
    def macToIp(self, mac_address):
       out = subprocess.check_output(['ip','neighbor']).decode('utf-8')
       try:
           ip = re.findall(r'.*{}'.format(mac_address),out)[0].split()[0]
           return ip
       # if mac address is not found, the ARP cache has been cleared.
       except IndexError:
           return None
   
    def runSSHCommand(self, command, ip_address, port, user, key):
        ssh_command = ['ssh', '-i', '/home/pi/.ssh/{}'.format(key),
                        '{}@{}'.format(user,ip_address), '-p',
                        '{}'.format(port), command]
        try:
            subprocess.run(ssh_command, check=True)
            return
        except Exception as e:
            self.speak_dialog("connection.error")
            self.log.error(e)
            return
    
    def runSSHCommandWithResult(self, command, ip_address, port, user, key):
        ssh_command = ['ssh', '-i', '/home/pi/.ssh/{}'.format(key),
                        '{}@{}'.format(user,ip_address),
                         '-p', '{}'.format(port), command]
        try:
            output = subprocess.run(ssh_command, capture_output=True, check=True)
            return output.stdout
        
        except Exception as e:
            self.speak_dialog("connection.error")
            self.log.error(e)
            return None
        
    def remoteAction(self, command, voice_response):
        try:
            config = self.config_core.get("RemoteComputerSkill", {})
            if not config == {}:
                mac_address = str(config.get("mac_address"))
                port = int(config.get("port"))
                user = str(config.get("user"))
                key_file = str(config.get("key_file"))

            else:
                mac_address = str(self.settings.get("mac_address"))
                port = int(self.settings.get("port"))
                user = str(self.settings.get("user"))
                key_file = str(self.settings.get("key_file"))
            
        except Exception as e:
            self.speak_dialog('settings.error')
            self.log.error(e)
            return
        
        ip_addr = self.macToIp(mac_address)
        if ip_addr is None:
            self.speak_dialog("ip.not.found")
        else:
            if len(voice_response) > 1:
                self.speak_dialog(voice_response[0], voice_response[1])
            else:
                self.speak_dialog(voice_response[0])
                
            res = self.runSSHCommand(command,ip_addr,port,user,key_file)  
    
    # def parseLaunchApplicationCommand(self, utt):
    #     parser = launchApplicationGrammar.LaunchApplicationGrammarParser()
    #     return asjson(parser.parse(utt))
    
    def createNewProject(self, project_name):
        project_name_string = ' '.join(project_name)
        project_name_ = '_'.join(project_name)
        self.remoteAction('mkdir /home/markd/Projects/{}'.format(project_name_),
                          ['creating.project',{'word':project_name_string}])
        
    @intent_handler(IntentBuilder("LaunchTerminal").require("Open").
                    require("Terminal"))
    def handle_launch_terminal_intent(self, message):
        self.remoteAction('export DISPLAY=:0 && terminator',
                          ['launch.app',{'word':'terminal'}])
    
    @intent_handler(IntentBuilder("LaunchSpyder").require("Open").
                    require("Spyder"))
    def handle_launch_spyder_intent(self, message):
        cmd = 'export DISPLAY=:0 && spyder --workdir=/home/markd/Projects/'
        self.remoteAction(cmd, ['launch.app',{'word':'spider'}])
    
    @intent_handler(IntentBuilder("LaunchCCS").require("Open").require("Code").
                    require("Composer").optionally("Studio"))
    def handle_launch_ccs_intent(self, message):
        # get working directory if supplied use PEG to pull out the workspace, if any
        #utt = message.data['utterance']
        #self.log.info("{}".format(utt))
        self.remoteAction('export DISPLAY=:0 && /home/markd/ti/ccs1000/ccs/eclipse/ccstudio',
                          ['launch.app',{'word':'code composer studio'}])
    
    @intent_handler(IntentBuilder("CreateNewProject").require("Create").
                    require("Project").optionally("New"))
    def handle_create_new_project_intent(self, message):
        utt = message.data['utterance'].split(' ')
        idx = utt.index('project') + 1
        self.createNewProject(utt[idx:])
        
    @intent_handler(IntentBuilder("LaunchJupyterNotebook").require("Open").
                    require("Jupyter").optionally("Notebook"))
    def handle_launch_jupyter_notebook_intent(self, message):
        cmd = 'export DISPLAY=:0 && jupyter-notebook --notebook-dir /home/markd/Projects',
        self.remoteAction(cmd, ['launch.app',{'word':'jupiter notebook'}])

    @intent_handler(IntentBuilder("LaunchVSCode").require("Open").require("Code").
                    optionally("VisualStudio"))
    def handle_launch_vscode_intent(self, message):
        cmd = 'export DISPLAY=:0 && code -a /home/markd/Projects/'
        self.remoteAction(cmd, ['launch.app',{'word':'visual studio code'}])

    def stop(self):
        pass


def create_skill():
    return RemoteComputerSkill()
