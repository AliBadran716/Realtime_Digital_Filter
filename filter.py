from scipy import signal
import numpy as np

class Filter():
    def __init__(self, poles=None, zeros=None, gain=1):
        self.poles = poles if poles else []
        self.zeros = zeros if zeros else []
        self.gain = gain
        self.all_pass = []

    def add_pole(self, pole):
        self.poles.append(pole)

    def add_zero(self, zero):
        self.zeros.append(zero)

    def add_all_pass(self, all_pass):
        self.all_pass_append(all_pass)

    def delete_pole(self, pole):
        """Delete a specific pole from the filter."""
        if pole in self.poles:
            self.poles.remove(pole)

    def delete_zero(self, zero):
        """Delete a specific zero from the filter."""
        if zero in self.zeros:
            self.zeros.remove(zero)

    def delete_all_pass(self, all_pass):
        if all_pass in self.all_pass:
            self.all_pass.remove(all_pass)

    def delete_poles(self):
        """Delete all poles from the filter."""
        self.poles.clear()

    def delete_zeros(self):
        """Delete all zeros from the filter."""
        self.zeros.clear()

    def delete_all_passes(self):
        self.all_pass.clear()

    def delete_all_components(self):
        self.delete_poles()
        self.delete_zeros()
        self.delete_all_passes()

    def get_poles(self):
        original_poles = [complex(pole.real, pole.imag) for pole in self.poles]
        all_pass_poles = [all_pass.a for all_pass in self.all_pass]
        return [*original_poles, *all_pass_poles]

    def get_zeros(self):
        original_zeros = [complex(zero.real, zero.imag) for zero in self.zeros]
        all_pass_zeros = [1 / np.conj(all_pass.a) for all_pass in self.all_pass]
        return [*original_zeros, *all_pass_zeros]

    def get_gain(self):
        return self.gain

    def get_response(self):
        zeros_values = self.get_zeros()
        poles_values = self.get_poles()
        w, response = signal.freqz_zpk(zeros_values, poles_values, self.gain)
        magnitude = 20 * np.log10(np.abs(response))
        phase = np.unwrap(np.angle(response))
        return w, magnitude, phase

    def get_all_pass_response(self):
        zeros_values = self.get_zeros()
        poles_values = self.get_poles()
        w, response = signal.freqz_zpk(zeros_values, poles_values, self.gain)
        magnitude = 20 * np.log10(np.abs(response))
        phase = np.unwrap(np.angle(response))
        return w, magnitude, phase
    



