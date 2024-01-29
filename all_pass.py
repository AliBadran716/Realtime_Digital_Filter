import numpy as np

class AllPassFilter:
    def __init__(self, a=None, name=None):
        self.a = a
        self.name = name

    def get_a(self):
        return self.a
    
    def get_name(self):
        return self.name
    

def calculate_phase_response(frequency, all_pass_filter):
    """
    Calculate the phase response of an all-pass filter.
    
    Args:
    - frequency (ndarray): Array of frequencies.
    - all_pass_filter (AllPassFilter): An instance of the AllPassFilter class.
    
    Returns:
    - phase_response (ndarray): Phase response corresponding to the given frequencies.
    """
    poles = all_pass_filter.get_poles()
    zeros = all_pass_filter.get_zeros()
    gain = all_pass_filter.get_gain()
    a = all_pass_filter.get_a()
    
    phase_response = np.zeros_like(frequency)
    for f_idx, f in enumerate(frequency):
        s = 1j * 2 * np.pi * f
        num = np.polyval([1, -a], s)
        den = np.polyval([1, a], s)
        H = gain * num / den
        phase_response[f_idx] = np.angle(H)
    
    return phase_response




