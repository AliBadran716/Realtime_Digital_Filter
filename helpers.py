# Certainly! Below is a simplified version of the backend logic from the Flask web app that you can integrate into your PyQt desktop application. I've removed the web-specific code and provided the core logic. Please note that you'll need to adapt this code based on your PyQt application structure.

# python
# Copy code
from scipy import signal
import numpy as np

class FilterManager:
    def __init__(self):
        self.input_signal = []
        self.combined_poles = []
        self.combined_zeros = []
        self.allPassZeros = []
        self.allPassPoles = []
        self.appliedAPFZeros = []
        self.appliedAPFPoles = []
        self.signal_output = [1 for i in range(15)]

    def set_combined_zeros_poles(self, zeros, poles):
        self.combined_zeros = zeros
        self.combined_poles = poles

    def set_allpass_zeros_poles(self, zeros, poles):
        self.allPassZeros = zeros
        self.allPassPoles = poles

    def apply_filter(self, input_point):
        self.signal_output.append(input_point)
        filter_order = max(len(self.combined_poles), len(self.combined_zeros))

        if len(self.signal_output) > 2 * filter_order and len(self.signal_output) > 50:
            del self.signal_output[0:filter_order]

        final_filter_zeros = self.combined_zeros + self.appliedAPFZeros
        final_filter_poles = self.combined_poles + self.appliedAPFPoles
        num, den = signal.zpk2tf(final_filter_zeros, final_filter_poles, 1)
        output_signal = signal.lfilter(num, den, self.signal_output).real
        output_point = output_signal[-1]
        return output_point

    def generate_signal(self, input_point):
        self.input_signal.append(input_point)
        filter_order = max(len(self.combined_poles), len(self.combined_zeros))

        if filter_order < 1:
            return input_point

        if len(self.input_signal) > 2 * filter_order and len(self.input_signal) > 50:
            del self.input_signal[0:filter_order]

        final_filter_zeros = self.combined_zeros + self.appliedAPFZeros
        final_filter_poles = self.combined_poles + self.appliedAPFPoles

        num, den = signal.zpk2tf(final_filter_zeros, final_filter_poles, 1)
        output_signal = signal.lfilter(num, den, self.input_signal).real

        output_point = output_signal[-1]
        return output_point

    def set_allpass_filters(self, zeros, poles):
        self.appliedAPFZeros = zeros
        self.appliedAPFPoles = poles

    def get_final_phase_response(self):
        final_filter_zeros = self.combined_zeros + self.appliedAPFZeros
        final_filter_poles = self.combined_poles + self.appliedAPFPoles
        freq, complex_gain = signal.freqz_zpk(final_filter_zeros, final_filter_poles, 1)
        result_phase = np.unwrap(np.angle(complex_gain))
        return freq, result_phase

    def get_allpass_phase_response(self):
        freq, complex_gain = signal.freqz_zpk(self.allPassZeros, self.allPassPoles, 1)
        Ap_phase = np.unwrap(np.angle(complex_gain))
        return freq, Ap_phase

# Now you can use FilterManager in your PyQt application like this:
# filter_manager = FilterManager()
# filter_manager.set_combined_zeros_poles(zeros, poles)
# filter_manager.set_allpass_zeros_poles(allpass_zeros, allpass_poles)
# filter_manager.set_allpass_filters(appliedAPFZeros, appliedAPFPoles)
# result = filter_manager.apply_filter(input_point)
# result = filter_manager.generate_signal(input_point)
# freq, result_phase = filter_manager.get_final_phase_response()
# freq, Ap_phase = filter_manager.get_allpass_phase_response()