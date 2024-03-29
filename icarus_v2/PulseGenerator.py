from PySide6.QtCore import QThread
from time import sleep, time


# DIGITAL
# CH0: high pressure pump
# CH1: depressurize valve
# CH2: pressurize valve
# CH3: spare
# CH4: log
# CH5: spare
# CH6: spare

class PulseGenerator(QThread):
    PUMP = 0
    DEPRESSURIZE = 1
    PRESSURIZE = 2
    LOG = 4


    def __init__(self, device, pressurize_width = 5., depressurize_width = 5., period_width = 5., delay_width = 2.) -> None:
        super().__init__()

        self.device = device

        # duration to hold valves open in ms
        self.pressurize_width = pressurize_width
        self.depressurize_width = depressurize_width

        # period timings in s
        self.period_width = period_width    # Time between depressurize pulses
        self.delay_width = delay_width      # Time between depressurize and pressurize

        # Whether or not the device should be currently generating pulses
        self.pulsing = False


    # Pressurizes and depressurizes at regular intervals
    def run(self):
        self.pulsing = True
        while self.pulsing:
            # Get time before setting DIO for more precise timing
            current_time = time()

            self._pulse_low(self.DEPRESSURIZE, self.depressurize_width)

            # Sleep for remaining time out of delay
            time_elapsed = time() - current_time
            remaining_time = self.delay_width - time_elapsed
            sleep(remaining_time)

            self._pulse_low(self.PRESSURIZE, self.pressurize_width)

            # Sleep for remaining time
            time_elapsed = time() - current_time
            remaining_time = self.period_width - time_elapsed
            sleep(remaining_time)


    def set_pressurize_low(self):
        self._set_low(self.PRESSURIZE)


    def set_pressurize_high(self):
        self._set_high(self.PRESSURIZE)


    def set_depressurize_low(self):
        self._set_low(self.DEPRESSURIZE)


    def set_depressurize_high(self):
        self._set_high(self.DEPRESSURIZE)


    def set_pump_low(self):
        self._set_low(self.PUMP)


    def set_pump_high(self):
        self._set_high(self.PUMP)


    def set_pressurize_width(self, pressurize_width):
        try:
            pressurize_width = float(pressurize_width)
        except:
            return
        self.pressurize_width = pressurize_width


    def set_depressurize_width(self, depressurize_width):
        try:
            depressurize_width = float(depressurize_width)
        except:
            return
        self.depressurize_width = depressurize_width


    def set_period_width(self, period_width):
        try:
            period_width = float(period_width)
        except:
            return
        self.period_width = period_width


    def set_delay_width(self, delay_width):
        try:
            delay_width = float(delay_width)
        except:
            return
        self.delay_width = delay_width


    # Sets channel low for duration milliseconds
    # Raises RuntimeError if channel is already low
    def _pulse_low(self, channel, duration):
        # int representing the current state of dio
        current_dio = self.device.get_current_dio()
        # binary representation of channel to pulse
        channel_bit = 2 ** channel

        # Make sure the channel we are pulsing starts high.
        if not current_dio & channel_bit: # bitwise AND
            raise RuntimeError(f"Error: pulsing low digital channel {channel} which is already low.")

        # Get time before setting DIO for more precise timing
        current_time = time()

        # Set specified channel low
        self.device.set_DIO(current_dio ^ channel_bit) # bitwise XOR

        # Sleep for remaining time
        duration_sec = float(duration) / 1000
        time_elapsed = time() - current_time
        remaining_time = duration_sec - time_elapsed
        sleep(remaining_time)

        # Reset to original DIO
        self.device.set_DIO(current_dio)


    # Sets channel low
    # Raises RuntimeError if channel is already low
    def _set_low(self, channel):
        # int representing the current state of dio
        current_dio = self.device.get_current_dio()
        # binary representation of channel to pulse
        channel_bit = 2 ** channel

        # Make sure the channel we are setting starts high.
        if not current_dio & channel_bit: # bitwise AND
            raise RuntimeError(f"Error: setting low digital channel {channel} which is already low.")

        # set low
        self.device.set_DIO(current_dio ^ channel_bit) # bitwise XOR


    # Sets channel high
    # Raises RuntimeError if channel is already high
    def _set_high(self, channel):
        # int representing the current state of dio
        current_dio = self.device.get_current_dio()
        # binary representation of channel to pulse
        channel_bit = 2 ** channel

        # Make sure the channel we are setting starts low.
        if current_dio & channel_bit: # bitwise AND
            raise RuntimeError(f"Error: setting high digital channel {channel} which is already high.")

        # set high
        self.device.set_DIO(current_dio | channel_bit) # bitwise OR


    def quit(self):
        self.pulsing = False