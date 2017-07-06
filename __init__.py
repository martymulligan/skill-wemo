# Copyright 2016 Mycroft AI, Inc.
#
# This file is part of Mycroft Core.
#
# Mycroft Core is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Mycroft Core is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Mycroft Core.  If not, see <http://www.gnu.org/licenses/>.


# Visit https://docs.mycroft.ai/skill.creation for more detailed information
# on the structure of this skill and its containing folder, as well as
# instructions for designing your own skill based on this template.


# Import statements: the list of outside modules you'll be using in your
# skills, whether from other files in mycroft-core or from external libraries
import re

from os.path import dirname, join

from adapt.intent import IntentBuilder
from mycroft.skills.core import MycroftSkill
from mycroft.util.log import getLogger
from ouimeaux.environment import Environment

__author__ = 'martymulligan'

# Logger: used for debug lines, like "LOGGER.debug(xyz)". These
# statements will show up in the command line when running Mycroft.
LOGGER = getLogger(__name__)

# The logic of each skill is contained within its own class, which inherits
# base methods from the MycroftSkill class with the syntax you can see below:
# "class ____Skill(MycroftSkill)"
class WemoSkill(MycroftSkill):

    # The constructor of the skill, which calls MycroftSkill's constructor
    def __init__(self):
        super(WemoSkill, self).__init__(name="WemoSkill")

    def on_switch(self, switch):
        LOGGER.debug("Switch detected: %s" % switch.name)
        self.speak('detected switch called ' + switch.name)

    def on_motion(self, motion):
        LOGGER.debug("Motion detected on ", motion.name)

    # This method loads the files needed for the skill's functioning, and
    # creates and registers each intent that the skill uses
    def initialize(self):
        LOGGER.debug("Initializing WeMo Environment");

        self.env = Environment(self.on_switch, self.on_motion)
        self.env.start()
        self.env.discover(seconds=15)

        self.load_data_files(dirname(__file__))
        prefixes = [
            'toggle', 'tockle', 'taco']
        self.__register_prefixed_regex(prefixes, "(?P<ToggleWords>.*)")

        listprefixes = [
            'list', 'list wemo', 'identify', 'identify wemo', 'get', 'get wemo']
        self.__register_prefixed_regex(listprefixes, "(?P<ListWords>.*)")

        # switch intent
        intent = IntentBuilder("WemoSwitchIntent").require(
            "WemoSwitchKeyword").require("ToggleWords").build()
        self.register_intent(intent, self.handle_wemo_switch_intent)

        # discover intent
        intent = IntentBuilder("WemoDiscoverIntent").require(
            "WemoDiscoverKeyword").build()
        self.register_intent(intent, self.handle_wemo_discover_intent)

        # list switches intent
        intent = IntentBuilder("WemoListSwitchesIntent").require(
            "WemoListKeyword").require("ListWords").build()
        self.register_intent(intent, self.handle_wemo_list_intent)


    def __register_prefixed_regex(self, prefixes, suffix_regex):
        for prefix in prefixes:
            self.register_regex(prefix + ' ' + suffix_regex)


    def handle_wemo_switch_intent(self, message):
        togglewords = message.data.get("ToggleWords")
        try:
            device = self.env.get_switch(togglewords)
            device.toggle()

        except:
            LOGGER.debug("Unknown WeMo device: ", togglewords)
            self.speak("I don't know a device called ", togglewords)

    def handle_wemo_list_intent(self, message):
        listwords = message.data.get("ListWords")
        if(listwords.index("switch") > 0 or listwords.index("plug") > 0):
            try:
                switches = self.env.list_switches();
                for switch in switches:
                    self.speak("Wemo switch ".switch)
            except:
                LOGGER.debug("Error occurred listing switches")
                self.speak("uh uh")



    def handle_wemo_discover_intent(self, message):
        try:
            self.env = Environment(self.on_switch, self.on_motion)
            self.env.start()
            self.env.discover(seconds=15)

        except:
            LOGGER.debug("Error occurred discovering devices")
            self.speak("uh uh")

    # The "stop" method defines what Mycroft does when told to stop during
    # the skill's execution. In this case, since the skill's functionality
    # is extremely simple, the method just contains the keyword "pass", which
    # does nothing.
    def stop(self):
        pass

# The "create_skill()" method is used to create an instance of the skill.
# Note that it's outside the class itself.
def create_skill():
    return WemoSkill()
