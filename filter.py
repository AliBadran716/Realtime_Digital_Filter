from scipy import signal
import numpy as np
from math import sin, cos

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
        for all_pass in self.all_pass:
            self.poles.append(all_pass)
        return self.poles


    def get_zeros(self):
        """Return the list of zeros."""
        all_pass_zeros = [1 / np.conj(all_pass) for all_pass in self.all_pass]
        for zeros in all_pass_zeros:
            self.zeros.append(zeros)
        return self.zeros


    def get_gain(self):
        return self.gain

    def get_response(self):
        # Get the zeros and poles of the filter
        zeros_values = self.get_zeros()
        poles_values = self.get_poles()

        # # Calculate the frequency response using signal.freqz_zpk
        # freqs, response = signal.freqz_zpk(zeros_values, poles_values, self.gain)

        # # Compute magnitude and phase of the frequency response
        # magnitude = np.abs(response)
        # phase = np.unwrap(np.angle(response))
        magnitude, freqs = self.get_mag_response()
        phase = self.get_phase_response()

        # Return frequency, magnitude, and phase
        return freqs, magnitude, phase

    def get_mag_response(self):
        # Get the zeros and poles of the filter
        zeros_values = self.get_zeros()
        poles_values = self.get_poles()
        freqs=[]
        magnitude = []
        # loop on the unit circle
        for point in np.linspace(0, np.pi, 100):
            freqs.append(point)
            y = sin(point)
            x = cos(point)
            point = complex(x, y)
            numerator = 1
            denominator = 1
            for zero in zeros_values:
                numerator *= self.calculate_eclidian_distance(zero, point)
            for pole in poles_values:
                denominator *= self.calculate_eclidian_distance(pole, point)
            magnitude.append(numerator/denominator)
        return magnitude, freqs

    def calculate_eclidian_distance(self, point1, point2):
        return np.sqrt((point1.real - point2.real) ** 2 + (point1.imag - point2.imag) ** 2)

    def get_phase_response(self):
        # Get the zeros and poles of the filter
        zeros_values = self.get_zeros()
        poles_values = self.get_poles()
        phase = []
        # loop on the unit circle
        for point in np.linspace(0,np.pi, 100):
            numerator = 0
            denominator = 0
            y = sin(point)
            x = cos(point)
            point = complex(x, y)
            for zero in zeros_values:
                numerator += self.calculate_phase(zero, point)
            for pole in poles_values:
                denominator -= self.calculate_phase(pole, point)
            phase.append(numerator + denominator)
        return phase


    def calculate_phase(self, point1, point2):
        return np.arctan2(point1.imag - point2.imag, point1.real - point2.real)

    def get_all_pass_phase_response(self):
        # Get the zeros and poles of the filter
        all_pass_poles = self.all_pass
        all_pass_zeros = [1 / np.conj(all_pass) for all_pass in self.all_pass]
        phase = []
        freqs = []
        # loop on the unit circle
        for point in np.linspace(0, np.pi, 100):
            numerator = 0
            denominator = 0
            y = sin(point)
            x = cos(point)
            freqs.append(point)
            point = complex(x, y)
            for all_pass in all_pass_zeros:
                numerator += self.calculate_phase(all_pass, point)
            for all_pass in all_pass_poles:
                denominator -= self.calculate_phase(all_pass, point)
            phase.append(numerator + denominator)
        return phase, freqs

    # apply filter to signal
    def apply_filter(self, input_signal):
        if input_signal is None:
            return None
        zeros_values = self.get_zeros()
        poles_values = self.get_poles()
        b, a = signal.zpk2tf(zeros_values, poles_values, 1)
        filtered_signal = signal.lfilter(b, a, input_signal)
        return filtered_signal