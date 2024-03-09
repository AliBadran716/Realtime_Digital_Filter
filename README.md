# Realtime Digital Filter Design Application
![Digital-Filter](https://github.com/Muhannad159/Realtime-Digital-Filter/assets/104541242/c755c7bd-3fdc-4214-a0b5-8ac6c747df28)

## Overview

The Realtime Digital Filter Design Application is a powerful tool designed for engineers and researchers to design and analyze digital filters in real-time. This application provides a comprehensive set of features for designing, visualizing, and optimizing digital filters, making it an invaluable resource for signal processing tasks.

## Features

### Graphical User Interface (GUI)
- Utilizes a GUI library to create an intuitive main window with interactive elements.
- Includes a canvas for the z-plane plot with the unit circle, providing a visual representation of filter design.

### Zeros/Poles Placement
- Allows users to interactively place zeros and poles by clicking on the canvas.
- Supports dragging for easy modification of zero and pole positions.
- Provides options to add/delete zeros and poles, enhancing flexibility in filter design.

### Clear and Conjugate Options
- Offers buttons to clear all zeros, all poles, or both, facilitating quick adjustments to the filter design.
- Includes a checkbox to enable/disable adding conjugates, allowing users to customize filter characteristics.

### Frequency Response Plot
- Displays separate graphs for magnitude and phase responses, enabling detailed analysis of filter performance.
- Updates plots dynamically as users modify zeros and poles, providing real-time feedback during design iterations.

### Real-time Filtering
- Implements signal processing functions using the designed filter for real-time filtering.
- Visualizes the time progress of the input signal and filtered output, facilitating performance evaluation.
- Includes a slider for controlling the speed/temporal-resolution of the filtering process, offering flexibility in real-time analysis.
- Allows users to input real-time signals by moving the mouse, providing an intuitive interface for signal generation.
- Maps mouse motion to signal frequency, enabling users to control the input signal characteristics.

### All-Pass Filters
- Provides a library of pre-defined all-pass filters with visualizations, offering users a range of options for phase correction.
- Implements a feature to design custom all-pass filters by specifying parameters, allowing for fine-tuning of phase correction.
- Offers drop-down menus or checkboxes to enable/disable added all-pass elements, providing control over filter configuration.

### Phase Correction
- Implements the addition of all-pass filters to correct phase distortions in the signal, enhancing filter performance.
- Allows users to pick and visualize all-pass filters from the library, facilitating easy integration into the filter design.

### Testing and Optimization
- Enables thorough testing of the application with various scenarios, ensuring robust performance under different conditions.
- Validates real-time processing functionality to meet user expectations.
- Optimizes the application for performance, especially during real-time signal processing, ensuring smooth and efficient operation.

## How to Use

1. **Download and Installation:** Clone the repository and install any required dependencies.
2. **Launch the Application:** Run the main script to launch the application.
3. **Design Filters:** Use the intuitive user interface to design digital filters, placing zeros and poles as needed.
4. **Visualize Responses:** View magnitude and phase responses in real-time, adjusting filter parameters as necessary.
5. **Apply Real-time Filtering:** Utilize the application for real-time filtering of input signals, monitoring time progress and output characteristics.
6. **Experiment with All-Pass Filters:** Explore the library of pre-defined and custom all-pass filters for phase correction.
7. **Test and Optimize:** Thoroughly test the application with various scenarios and optimize performance for seamless user experience.

## Dependencies

- Python
- PyQt
- NumPy
- Matplotlib
- SciPy

## Contributors <a name = "Contributors"></a>

<table>
  <tr>
    <td align="center">
    <a href="https://github.com/Muhannad159" target="_black">
    <img src="https://avatars.githubusercontent.com/u/104541242?v=4" width="150px;" alt="Muhannad Abdallah"/>
    <br />
    <sub><b>Muhannad Abdallah</b></sub></a>
    </td>
  <td align="center">
    <a href="https://github.com/AliBadran716" target="_black">
    <img src="https://avatars.githubusercontent.com/u/102072821?v=4" width="150px;" alt="Ali Badran"/>
    <br />
    <sub><b>Ali Badran</b></sub></a>
    </td>
     <td align="center">
    <a href="https://github.com/ahmedalii3" target="_black">
    <img src="https://avatars.githubusercontent.com/u/110257687?v=4" width="150px;" alt="Ahmed Ali"/>
    <br />
    <sub><b>Ahmed Ali</b></sub></a>
    </td>
<td align="center">
    <a href="https://github.com/ossama971" target="_black">
    <img src="https://avatars.githubusercontent.com/u/40814982?v=4" width="150px;" alt="Hassan Hussein"/>
    <br />
    <sub><b>Osama Badawi</b></sub></a>
    </td>
      </tr>
 </table>




