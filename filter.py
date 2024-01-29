from scipy import signal
import numpy as np

class Filter():
    def __init__(self, poles=None, zeros=None, gain=1):
        self.poles = poles if poles else []
        self.zeros = zeros if zeros else []
        self.gain = gain
        self.all_pass = []

    def add_pole(self, pole):
        self.poles = pole

    def add_zero(self, zero):
        self.zeros = zero

    def add_all_pass(self, all_pass):
        self.all_pass.append(all_pass)

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
        """Return the list of poles."""
        return self.poles


    def get_zeros(self):
        """Return the list of zeros."""
        return self.zeros


    def get_gain(self):
        return self.gain

    def get_response(self):
        # Get the zeros and poles of the filter
        zeros_values = self.get_zeros()
        poles_values = self.get_poles()

        # Calculate the frequency response using signal.freqz_zpk
        w, response = signal.freqz_zpk(zeros_values, poles_values, self.gain)

        # Compute magnitude and phase of the frequency response
        magnitude = 20 * np.log10(np.abs(response))
        phase = np.unwrap(np.angle(response))

        # Return frequency, magnitude, and phase
        return w, magnitude, phase



    def get_all_pass_response(self):
        zeros_values = self.get_zeros()
        poles_values = self.get_poles()
        w, response = signal.freqz_zpk(zeros_values, poles_values, self.gain)
        magnitude = 20 * np.log10(np.abs(response))
        phase = np.unwrap(np.angle(response))
        return w, magnitude, phase
