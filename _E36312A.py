import pyvisa as visa
import time


class Waveform:

    def __init__(self):
        self.rm = visa.ResourceManager()
        # open connection to power supply
        self.E36312A = self.rm.open_resource('TCPIP0::172.30.29.135::inst0::INSTR')

    # REQUIRES: nothing
    # MODIFIES: nothing
    # EFFECTS:  close the resource manager

    def set_parameters(self):
        # set the voltage measurement for channel 1 to use the external sense line
        self.E36312A.write(':SOURce:VOLTage:SENSe:SOURce %s,(%s)' % ('EXTernal', '@1'))
        # set the power supply channel 1 to 1V and 0.01A current limit
        self.E36312A.write(':APPLy %s,%G,%G' % ('CH1', 1.0, 1))
        # turn on output for channel 1
        self.E36312A.write(':OUTPut:STATe %d' % (1))
        # wait for 500ms for the output to stabilize
        time.sleep(0.5)

    def get_voltage(self):
        voltage = self.E36312A.query_ascii_values(':MEASure:SCALar:VOLTage:DC? (%s)' % ('@1'))
        # print("Voltage ", voltage)
        return voltage[0]

    def get_current(self):
        # measure the current
        current = self.E36312A.query_ascii_values(':MEASure:SCALar:CURRent:DC? (%s)' % ('@1'))
        # print("Current ", current)
        return current[0]

    def get_resistance(self):
        voltage = self.get_voltage()
        current = self.get_current()
        return voltage / current

    def close(self):
        # Turn off channels
        self.E36312A.write(':OUTPut:STATe %d' % (0))
        # close connection to instrument
        self.E36312A.close()
        self.rm.close()
