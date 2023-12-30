import numpy as np
from scipy import signal

class Filter:
    def __init__(self):
        self.zeros = []
        self.poles = []
        self.gain = 1
        # Initialize variables for real-time filtering
        self.temporal_resolution = 1  # Default temporal resolution (1 point per second)
        self.filtering_index = 0  # Index indicating the progress of filtering

    def set_filter_components(self, zeros: list, poles: list, gain: float) -> None:
        """Set the filter components."""
        self.zeros = zeros
        self.poles = poles
        self.gain = gain

    def get_filter_components(self) -> tuple:
        """Get the filter components."""
        return self.zeros, self.poles, self.gain

    def get_frequency_response(self) -> tuple:
        """Get the frequency response components."""
        frequency, freq_response = signal.freqz_zpk(self.zeros, self.poles, self.gain)
        magnitude = 20 * np.log(np.abs(freq_response))
        phase = np.unwrap(np.angle(freq_response))
        return frequency, magnitude, phase

    def apply_filter(self, input_arr: np.ndarray):
        """Apply the filter to the input signal."""
        numerator, denominator = signal.zpk2tf(self.zeros, self.poles, self.gain)
        output_signal = signal.lfilter(numerator, denominator, input_arr)
        return output_signal.real
    
    def apply_real_time_filtering(self, input_signal: np.ndarray):
        """apply the real-time filtering process."""
        # Determine the number of points to process in each iteration based on temporal resolution
        points_per_iteration = int(self.temporal_resolution)

        # Calculate the end index for the current iteration
        end_index = min(self.filtering_index + points_per_iteration, len(input_signal))

        # Get the portion of the signal to process in this iteration
        signal_chunk = input_signal[self.filtering_index:end_index]

        # Apply the filter to the signal chunk
        filtered_chunk = self.process.apply_filter(signal_chunk)

        # # Update the graphs with the current chunk of the original and filtered signals
        # self.update_graphs(signal_chunk, filtered_chunk)

        # Update the filtering index for the next iteration
        self.filtering_index = end_index

        # Check if filtering is complete
        if self.filtering_index >= len(input_signal):
            self.stop_real_time_filtering()

    def start_real_time_filtering(self):
        # Reset the filtering index
        self.filtering_index = 0

        # Start a timer to periodically update the real-time filtering process
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_real_time_filtering)
        self.timer.start(1000)  # Timer interval in milliseconds (adjust as needed)

    def stop_real_time_filtering(self):
        # Stop the timer when filtering is complete
        self.timer.stop()
        self.timer = None

    
