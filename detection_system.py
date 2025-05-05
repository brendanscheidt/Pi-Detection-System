import sys
import warnings
from gpiozero.exc import PWMSoftwareFallback
from gpiozero import DistanceSensor
from sms_sender import SMSSender
import time
import threading

class DetectionSystem():
    def __init__(self, echo_pin=24, trigger_pin=23, name="Default"):
        self.echo_pin = echo_pin
        self.trigger_pin = trigger_pin
        warnings.filterwarnings("ignore", category=PWMSoftwareFallback)
        self.sensor = DistanceSensor(echo=echo_pin, trigger=trigger_pin)
        self.sensor.when_in_range = self._trigger_detection
        self.sensor.when_out_of_range = self._trigger_clear
        self.sms_sender = SMSSender(name)
        self.last_alert = 0
        self.cooldown = 60

    def _trigger_detection(self):
        now = time.time()
        if now - self.last_alert < self.cooldown:
            return
        
        print("OPEN")
        self.last_alert = now

        threading.Thread(
            target=self.sms_sender.send_message,
            args=("Intrusion Detected!",),
            daemon=True
        ).start()

    def _trigger_clear(self):
      print("CLOSE")

    def _meters_to_centimeters(self, meters):
        return meters * 100
    
    def _centimeters_to_meters(self, cm):
        return cm / 100
    
    def ping_distance(self):
        return self._meters_to_centimeters(self.sensor.distance)

    def set_trigger_threshold(self, threshold_distance_cm):
        threshold_meters = self._centimeters_to_meters(threshold_distance_cm)
        self.sensor.threshold_distance = min(threshold_meters, self.sensor.max_distance - 0.00001)

    def get_trigger_threshold_distance(self):
        return self._meters_to_centimeters(self.sensor.threshold_distance)

    def set_max_distance(self, max_distance_cm):
        max_distance_meters = self._centimeters_to_meters(max_distance_cm)
        if self.get_trigger_threshold_distance() >= max_distance_cm:
            self.set_trigger_threshold(max_distance_cm - 0.00001)
        self.sensor.max_distance = max_distance_meters

    def get_max_distance(self):
        return self._meters_to_centimeters(self.sensor.max_distance)

    def run(self):
        while True:
            print(self.ping_distance())
            time.sleep(1)

