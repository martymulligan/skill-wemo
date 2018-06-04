from mycroft.skills.core import MycroftSkill
from mycroft.util.log import getLogger
from mycroft import intent_file_handler
import pywemo

__author__ = 'martymulligan'

# Logger: used for debug lines, like "LOGGER.debug(xyz)". These
# statements will show up in the command line when running Mycroft.
LOGGER = getLogger(__name__)

# The logic of each skill is contained within its own class, which inherits
# base methods from the MycroftSkill class with the syntax you can see below:
# "class ____Skill(MycroftSkill)"
class WemoSkill(MycroftSkill):

    devices = {}

    # The constructor of the skill, which calls MycroftSkill's constructor
    def __init__(self):
        MycroftSkill.__init__(self)

    def initialize(self):
        if len(self.devices) < 1:
            self.discover_devices()

    def get_device(self, name):
        device = next((dev for dev in self.devices if dev.name == name), None)
        if(device is None):
            raise ValueError("I don't know a device called "+name)
        return device

    @intent_file_handler('switch.on.intent')
    def handle_switch_on(self, message):
        if 'device' not in message.data:
            self.speak("I don't know that device");
            return
        try:
            requested_device = message.data["device"];
            device = self.get_device(requested_device)
            device.on()
        except ValueError as e:
            self.speak(e)

    @intent_file_handler('switch.off.intent')
    def handle_switch_off(self, message):
        if 'device' not in message.data:
            self.speak("I don't know that device");
            return
        try:
            requested_device = message.data.get("device");
            device = self.get_device(requested_device)
            device.off()
        except ValueError as e:
            self.speak(repr(e))

    @intent_file_handler('toggle.intent')
    def handle_wemo_toggle_intent(self, message):
        requested_device = message.data.get("device")
        try:
            device = next((dev for dev in self.devices if dev.name == requested_device), None)
            if device is not None:
                device.toggle()
            else:
                self.speak("I don't know a device called ", device)

        except Exception as e:
            LOGGER.debug("WemoSkill caught an exception" + repr(e))
            self.speak("I don't know that device")

    @intent_file_handler('list.intent')
    def handle_wemo_list_intent(self, message):
        try:
            for device in self.devices:
                feedback = "There is a %s named %s at %s" % (device.model_name, device.name, device.host)
                self.speak(feedback)

        except Exception as e:
            LOGGER.debug("Error occurred listing Wemo devices: " + e)
            LOGGER.debug(e)
            self.speak("An error occurred getting the device list")


    @intent_file_handler('discover.intent')
    def handle_wemo_discover_intent(self, message):
        self.discover_devices()

    # The "stop" method defines what Mycroft does when told to stop during
    # the skill's execution. In this case, since the skill's functionality
    # is extremely simple, the method just contains the keyword "pass", which
    # does nothing.
    def stop(self):
        pass

    def discover_devices(self):
        try:
            devices = pywemo.discover_devices()
            if len(devices) < 1:
                self.speak("I didn't find any We Mo devices")
            else:
                self.devices = []
                for device in devices:
                    feedback = "Discovered a We Mo %s called %s" % (device.model_name, device.name)
                    LOGGER.debug(feedback)
                    self.devices.append(device)
                    self.speak(feedback)

        except Exception as e:
            feedback = "Error occurred discovering Wemo switches: " + e
            self.speak(feedback)

# The "create_skill()" method is used to create an instance of the skill.
# Note that it's outside the class itself.
def create_skill():
    return WemoSkill()
