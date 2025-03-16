# This is a UART periperhal.

import bluetooth
from ble_advertising import advertising_payload
from micropython import const
import machine
import time
from math import log

_IRQ_CENTRAL_CONNECT = const(1)
_IRQ_CENTRAL_DISCONNECT = const(2)
_IRQ_GATTS_WRITE = const(3)

_FLAG_READ = const(0x0002)
_FLAG_WRITE_NO_RESPONSE = const(0x0004)
_FLAG_WRITE = const(0x0008)
_FLAG_NOTIFY = const(0x0010)

_UART_UUID = bluetooth.UUID("6E400001-B5A3-F393-E0A9-E50E24DCCA9E")
_UART_TX = (
    bluetooth.UUID("6E400003-B5A3-F393-E0A9-E50E24DCCA9E"),
    _FLAG_READ | _FLAG_NOTIFY,
)
_UART_RX = (
    bluetooth.UUID("6E400002-B5A3-F393-E0A9-E50E24DCCA9E"),
    _FLAG_WRITE | _FLAG_WRITE_NO_RESPONSE,
)
_UART_SERVICE = (
    _UART_UUID,
    (_UART_TX, _UART_RX),
)

class BLESimplePeripheral():
    def __init__(self, ble, name="mpy-uart"):
        self._ble = ble
        self._ble.active(True)
        self._ble.irq(self._irq)
        ((self._handle_tx, self._handle_rx),) = self._ble.gatts_register_services((_UART_SERVICE,))
        self._connections = set()
        self._write_callback = None
        self._payload = advertising_payload(name=name, services=[_UART_UUID])
        self._connected = False
        self._advertising = False
        self._advertise()

    def _irq(self, event, data):
        # Track connections so we can send notifications.
        if event == _IRQ_CENTRAL_CONNECT:
            conn_handle, _, _ = data
            self._connected = True
            self._advertising = False
            self._connections.add(conn_handle)
        elif event == _IRQ_CENTRAL_DISCONNECT:
            conn_handle, _, _ = data
            self._connected = False
            self._connections.remove(conn_handle)
            # Start advertising again to allow a new connection.
            self._advertise()
        elif event == _IRQ_GATTS_WRITE:
            conn_handle, value_handle = data
            value = self._ble.gatts_read(value_handle)
            if value_handle == self._handle_rx and self._write_callback:
                self._write_callback(value)

    def send(self, data):
        for conn_handle in self._connections:
            self._ble.gatts_notify(conn_handle, self._handle_tx, data)

    def is_connected(self):
        return len(self._connections) > 0

    def _advertise(self, interval_us=500000):
        self._ble.gap_advertise(interval_us, adv_data=self._payload)
        self._advertising = True

    def on_write(self, callback):
        self._write_callback = callback
        
    def get_connected(self):
        return self._connected
    
    def get_advertising(self):
        return self._advertising
        
#
# RGB led class
#

class RGBleds():
    def __init__(self, leds):
        self.leds = leds
        self.max_value = const(65535)
        self.min_value = const(0)
        self.current_red = self.max_value
        self.current_green = self.max_value
        self.current_blue = self.max_value
    
    def pulse(self, duration, red_duty=0, green_duty=0, blue_duty=0):
        brightness = self.max_value
        state = -1
        for _ in range(2):
            state *= -1
            for j in range(63):
                brightness = brightness - (1000 * state)
                red_multiplier = red_duty 		/ self.max_value
                green_multiplier = green_duty 	/ self.max_value
                blue_multiplier = blue_duty 	/ self.max_value
                for led in self.leds:
                    self.change_RGB(
                        int(red_multiplier 		* brightness),
                        int(green_multiplier 	* brightness),
                        int(blue_multiplier 	* brightness))
                time.sleep_ms(duration)

    def blink(self, duration, red_duty=0, green_duty=0, blue_duty=0):
        switch = True
        for _ in range(2):
            switch = not switch
            for led in leds:
                self.change_RGB(
                    red_duty 	* switch,
                    green_duty 	* switch,
                    blue_duty 	* switch)
            time.sleep_ms(duration)
            
    def change_RGB(self, red_duty, green_duty, blue_duty):
        for ledDuty, led in zip((red_duty, green_duty, blue_duty), self.leds):
            led.init(freq = 2000, duty_u16 = ledDuty)
        self.current_red 	= red_duty
        self.current_green 	= green_duty
        self.current_blue 	= blue_duty
        
    def on(self):
        self.change_RGB(self.current_red, self.current_green, self.current_blue)
        
    def off(self):
        self.change_RGB(self.min_value, self.min_value, self.min_value)
        
#
# Functions for PWM-LED
#

def on_rx(value):
    global rx_message
    value = value.decode("strict").replace("\r\n","")
    rx_message = value
    print("RX", rx_message)
    
def is_number(input_value):
    try:
        if input_value == "0":
            return 0
        int_value = int(input_value)
        return int_value
    except ValueError:
        pass
    return None

def play_tone(buzzer, freq, duration, pause = 0):
        buzzer.init(freq = freq, duty_u16 = 2**15)
        time.sleep_ms(duration)
        buzzer.duty_u16(0)
        time.sleep_ms(pause)
        
def sound_connect(buzzer):
    for freq_increment in range(600, 2000, 300):
        play_tone(buzzer = buzzer, freq = freq_increment, duration = 150)

def sound_disconnect(buzzer):
    for freq_increment in range(0, 1500, 1000):
        play_tone(buzzer = buzzer, freq = 2000 - freq_increment, duration = 150)
    
def set_device_duty(device, duty, freq = 2000):
    device.init(duty = duty, freq = freq)
    
def set_duty_to_maximum(device, freq = 2000):
    set_device_duty(device, duty = 1023, freq = freq)

def set_duty_to_minimum(device, freq = 2000):
    set_device_duty(device, duty = 0,  freq = freq)

#
# Main for PWM-LED
#
buzzer_gpio = const(10)
mosfet_gpio = const(9)
red_led_gpio = const(3)
green_led_gpio = const(4)
blue_led_gpio = const(5)

buzzer 		= 	machine.PWM(machine.Pin(buzzer_gpio, machine.Pin.OUT), freq = 200)
mosfet 		= 	machine.PWM(machine.Pin(mosfet_gpio, machine.Pin.OUT), freq = 200)
red_led 	= 	machine.PWM(machine.Pin(red_led_gpio, machine.Pin.OUT), freq = 200)
green_led 	= 	machine.PWM(machine.Pin(green_led_gpio, machine.Pin.OUT), freq = 200)
blue_led 	= 	machine.PWM(machine.Pin(blue_led_gpio, machine.Pin.OUT), freq = 200)

buzzer.deinit()
mosfet.deinit()
red_led.deinit()
green_led.deinit()
blue_led.deinit()

rgb_leds = RGBleds(leds = (red_led, green_led, blue_led))

ble = bluetooth.BLE()
bluethooth = BLESimplePeripheral(ble, name = "PWM-LED")
rx_message = None
bluethooth.on_write(on_rx)

previous_connected = False
previous_advertising = False
previous_duty = None

while True:
    if bluethooth.get_connected() and not previous_connected:
        previous_connected = True
        print("Device is connected")
        sound_connect(buzzer)
        
    elif not bluethooth.get_connected() and previous_connected:
        previous_connected = False
        print("Device is disconnected")
        sound_disconnect(buzzer)
        
    if bluethooth.get_advertising() and not previous_advertising:
        previous_advertising = True
        print("Starting advertising")
        set_duty_to_minimum(device = mosfet)
        previous_duty = None
        
    elif not bluethooth.get_advertising() and previous_advertising:
        previous_advertising = False
        print("Ending advertising")
        rgb_leds.change_RGB(red_duty = 5000, green_duty = 4000, blue_duty = 20000)
    
    if previous_advertising:
        rgb_leds.pulse(duration = 20, red_duty = 5000, green_duty = 4000, blue_duty = 20000)
        
    
    if not rx_message:
        time.sleep_ms(100)
        continue
    
    if rx_message == "ON":
        if not previous_duty:
            set_duty_to_maximum(device = mosfet)
        else:
            set_device_duty(device = mosfet, duty = previous_duty)
            
        print("Turning on the LED")
        rx_message = None
        continue
    
    if rx_message == "OFF":
        set_duty_to_minimum(device = mosfet)
        print("Turning off the LED")
        rx_message = None
        continue

    rx_number = is_number(rx_message)
    if rx_number and rx_number <= 100 and rx_number >= 0:
         duty = int(round(10.23 * rx_number))
         previous_duty = duty
         set_device_duty(device = mosfet, duty  = duty)
         print("Duty set to:", duty)
         rx_message = None

