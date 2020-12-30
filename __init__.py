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
#import sys
import paramiko
import subprocess
#import ipaddress
#from wakeonlan import send_magic_packet

from adapt.intent import IntentBuilder
from mycroft.skills.core import MycroftSkill
from mycroft.skills.core import intent_handler


class RemoteComputerSkill(MycroftSkill):
    def __init__(self):
        super(RemoteComputerSkill, self).__init__(name="RemoteComputerSkill")
    
    def macToIp(self, mac_address):
       out = subprocess.check_output(['ip','neighbor']).decode('utf-8')
       ip = re.findall(r'.*{}'.format(mac_address),out)[0].split()[0]
       return ip
   
    def runSSHCommand(self, command, ip_address, port, user, key):
        ssh_command = ['ssh', '-i', '/home/pi/.ssh/{}'.format(key), '{}@{}'.format(user,ip_address), '-p', '{}'.format(port), command]
        try:
            subprocess.run(ssh_command, check=True)
            return
        except Exception as e:
            self.speak_dialog("connection.error")
            self.log.error(e)
            return
    
    def runSSHCommandParamiko(self,command,ip_address,port,user,key):
        try:
            client = paramiko.SSHClient()
            pk = paramiko.RSAKey.from_private_key_file(open('/home/pi/.ssh/{}'.format(key)))
            client.set_missing_host_key_policy(paramiko.AutoAddPolicy()) 
            client.connect(ip_address, username=user, port=port, pkey=pk)
            stdin, stdout, stderr = client.exec_command(command)
            client.close()
            return stdin, stdout, stderr
        except Exception as e:
            self.speak_dialog("connection.error")
            self.log.error(e)
            return
        
    def remoteAction(self, command, voice_response):
        try:
            config = self.config_core.get("RemoteComputerSkill", {})
            if not config == {}:
                self.log.info('config not empty')
                mac_address = str(config.get("mac_address"))
                port = int(config.get("port"))
                user = str(config.get("user"))
                key_file = str(config.get("key_file"))

            else:
                self.log.info('config empty')
                mac_address = str(self.settings.get("mac_address"))
                port = int(self.settings.get("port"))
                user = str(self.settings.get("user"))
                key_file = str(self.settings.get("key_file"))
            
        except Exception as e:
            self.speak_dialog('settings.error')
            self.log.error(e)
            return
        
        ip_addr = self.macToIp(mac_address)
        self.speak_dialog(voice_response)
        _ = self.runSSHCommand(command,ip_addr,port,user,key_file)
        
    @intent_handler(IntentBuilder("LaunchTerminal").require("Open").require("Terminal"))
    def handle_launch_terminal_intent(self, message):
        self.remoteAction('export DISPLAY=:0 && terminator','launching.terminal')
    
    @intent_handler(IntentBuilder("LaunchSpyder").require("Open").require("Spyder"))
    def handle_launch_spyder_intent(self, message):
        self.remoteAction('export DISPLAY=:0 && spyder --workdir=/home/markd/Projects', 'launching.spyder')
                
#    @intent_handler(IntentBuilder("ComputerOnIntent").require("Computer")
#                    .require("On").optionally("Turn"))
#    def handle_turn_on_intent(self, message):
#        try:
#            config = self.config_core.get("RemoteComputerSkill", {})
#
#            if not config == {}:
#                mac_address = str(config.get("mac_address"))
#
#            else:
#                mac_address = str(self.settings.get("mac_address"))
#
#            if not mac_address:
#                raise Exception("None found.")
#
#        except Exception as e:
#            self.speak_dialog("settings.error")
#            self.log.error(e)
#            return
#
#        re_mac = "[0-9a-f]{2}([-:]?)[0-9a-f]{2}(\\1[0-9a-f]{2}){4}$"
#
#        if re.match(re_mac, mac_address.lower()):
#            if ':' in mac_address:
#                mac_address.replace(':', '.')
#
#            elif '-' in mac_address:
#                mac_address.replace('-', '.')
#
#        else:
#            self.speak_dialog("invalid", {"word": "mac"})
#            return
#
#        prompt_response = self.ask_yesno("ask.confirmation",
#                                         {"word": "turn on"})
#
#        if prompt_response == "yes":
#            try:
#                send_magic_packet(mac_address)
#                self.speak_dialog("computer.on")
#
#            except Exception as e:
#                self.speak_dialog("connection.error")
#                self.log.error(e)
#
#        elif prompt_response == "no":
#            self.speak_dialog("okay")
#
#    @intent_handler(IntentBuilder("ComputerOffIntent").require("Computer")
#                    .require("Off").optionally("Turn"))
#    def handle_turn_off_intent(self, message):
#        try:
#            config = self.config_core.get("RemoteComputerSkill", {})
#
#            if not config == {}:
#                ip_address = str(self.config.get("ip_address"))
#                port = int(self.config.get("port"))
#                user = str(self.config.get("user"))
#                user_password = str(self.config.get("user_password"))
#                sudo_password = str(self.config.get("sudo_password"))
#
#            else:
#                ip_address = str(self.settings.get("ip_address"))
#                port = int(self.settings.get("port"))
#                user = str(self.settings.get("user"))
#                user_password = str(self.settings.get("user_password"))
#                sudo_password = str(self.settings.get("sudo_password"))
#
#            if not ip_address or not port or not user \
#                    or not user_password or not sudo_password:
#                raise Exception("None found.")
#
#        except Exception as e:
#            self.speak_dialog("settings.error")
#            self.log.error(e)
#            return
#
#        try:
#            ip = ipaddress.ip_address(ip_address)
#
#        except ValueError:
#            self.speak_dialog("invalid", {"word": "I.P"})
#            return
#
#        prompt_response = self.ask_yesno("ask.confirmation",
#                                         {"word": "shut down"})
#
#        if prompt_response == "yes":
#            try:
#                client = paramiko.SSHClient()
#                client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
#                client.connect(
#                            hostname=str(ip),
#                            port=port,
#                            username=user,
#                            password=user_password)
#
#                transport = client.get_transport()
#
#                session = transport.open_session()
#                session.set_combine_stderr(True)
#                session.get_pty()
#
#                if sys.platform.startswith("win"):
#                    session.exec_command("shutdown /s")
#
#                else:
#                    session.exec_command("sudo -k shutdown -h now")
#
#                stdin = session.makefile('wb', -1)
#                stdout = session.makefile('rb', -1)
#                stdin.write(sudo_password + '\n')
#                stdin.flush()
#                stdout.read()
#
#                client.close()
#
#                self.speak_dialog("computer.off")
#
#            except Exception as e:
#                self.speak_dialog("connection.error")
#                self.log.error(e)
#
#        elif prompt_response == "no":
#            self.speak_dialog("okay")

    def stop(self):
        pass


def create_skill():
    return RemoteComputerSkill()
