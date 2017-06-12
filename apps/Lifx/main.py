import logging
from apps import App, action
import requests
import json
logger = logging.getLogger(__name__)
import time

class Main(App):
    """
       Skeleton example app to build other apps off of
    
       Args:
           name (str): Name of the app
           device (list[str]): List of associated device names
           
    """
    def __init__(self, name=None, device=None):
        App.__init__(self, name, device)   # Required to call superconstructor
        self.headers = {"Authorization": "Bearer {0}".format(self.get_device().get_password())}
        self.name = self.get_device().username
        self.base_url = 'https://api.lifx.com/v1/lights/'

    def __api_url(self, endpoint):
        return '{0}{1}'.format(self.base_url, endpoint)

    @action
    def list_lights(self):
        response = requests.get(self.__api_url('all'), headers=self.headers)
        return json.loads(response.text)

    @action
    def set_state(self, power, color, brightness, duration, infrared):
        """
        Sets the state of the light
        power: on or off
        color: color to set the lights to
        brightness: int from 0 to 1
        duration: seconds for the action to last
        infrared: 0 to 1. maximum brightness of infrared channel
        """
        payload = {"power": power,
                   "color": color,
                   "brightness": brightness,
                   "duration": duration,
                   "infrared": infrared}
        response = requests.put(self.__api_url('all/state'.format(self.name)), data=payload, headers=self.headers)
        time.sleep(duration)
        return json.loads(response.text)

    @action
    def toggle_power(self, duration):
        """
        Sets the state of the light
        duration: seconds for the action to last
        """
        payload = {"duration": duration}
        response = requests.post(self.__api_url('all/toggle'.format(self.name)), data=payload, headers=self.headers)
        time.sleep(duration)
        return json.loads(response.text)

    @action
    def breathe_effect(self, color, from_color, period, cycles, persist, power_on, peak):
        """
        Slowly fades between two colors
        color: color to use for the breathe effect
        from_color: color to start the breathe effect from
        period: Time in seconds between cycles
        cycles: Number of times to repeat the effect
        persist: If false set teh light back to its previous value when effect ends. Else leave at last effect
        power_on: If true, turn on the light if not already on
        peak: where in the period the target color is at its maximum. Between 0 and 10
        """
        payload = {"color": color,
                   "from_color": from_color,
                   "period": period,
                   "cycles": cycles,
                   "persist": persist,
                   "power_on": power_on,
                   "peak": peak}
        response = requests.post(self.__api_url('all/effects/breathe'),
                                data=payload,
                                headers=self.headers)
        time.sleep(period*cycles)
        return json.loads(response.text)

    @action
    def pulse_effect(self, color, from_color, period, cycles, persist, power_on):
        """
        Quickly flashes between two colors
        color: color to use for the breathe effect
        from_color: color to start the breathe effect from
        period: Time in milliseconds between cycles
        cycles: Number of times to repeat the effect
        persist: If false set teh light back to its previous value when effect ends. Else leave at last effect
        power_on: If true, turn on the light if not already on
        """
        payload = {"color": color,
                   "from_color": from_color,
                   "period": period,
                   "cycles": cycles,
                   "persist": persist,
                   "power_on": power_on}
        response = requests.post(self.__api_url('all/effects/pulse'),
                                data=payload,
                                headers=self.headers)
        time.sleep(period * cycles)
        return json.loads(response.text)