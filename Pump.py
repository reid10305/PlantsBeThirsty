class Pump(object):
    """class to define the pump object"""

    # pump flag placeholder for digital IO pin
    pump_flag = False
    pump_rate = 1


    #gpio_pin = gp.DigitalOutputDevice(pin = pin)

    # constructor
    def __init__(self, pin, pump_rate):
        ''' class constructor
            pin : pin to control the pump with GPIO
            pump_rate : pump rate in G/Hr '''

        self.pump_flag = pin
        self.pump_rate = pump_rate

        return

    def pump_on(self):
        ''' turn the pump on '''

        self.pump_flag = True
        print(self.pump_flag)

        return

    def pump_off(self):
        ''' turn the pump off'''

        self.pump_flag = False
        print(self.pump_flag)

        return

    def tostring(self):
        ''' print string '''

        print("Is pumping currently: " + str(self.pump_flag))
        print("Control Pin: " + "17")
        print("Pump rate: " + str(self.pump_rate))

        return 

