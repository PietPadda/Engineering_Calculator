Markdown

# Engineering Solver

A desktop application designed for mechanical engineering calculations in the building services construction industry. The initial focus is a user-friendly duct sizing solver that calculates key parameters like area and velocity, built from scratch using Python and Tkinter. This tool aims to streamline workflows by replacing cumbersome Excel-based methods with an intuitive interface and robust error handling.

# The Solver in Action

Below is a screenshot of the application running:

* **Top Canvas**: Duct visualisations with input and output labels along with leaders to illustrate the output and issues (TODO)
* **Mid Grid**: Dropdown selector for duct type along with input fields for dimensions and flow rate (Selecting round hides height and reuses Width as Diameter"
* **Bottom Canvas**: "Terminal" simulation of outputs along with warnings, errors and design limitations

![Solver running](https://github.com/PietPadda/Engineering_Calculator/blob/main/Readme_Screenshot.png?raw=true)

## Features

* **Duct Sizing Solver**: Calculate cross-sectional area and airflow velocity for rectangular and round ducts.
* **Interactive UI**: Input fields for duct dimensions (width/diameter, height) and flow rate, with a dropdown for duct type selection.
* **Real-Time Results**: Displays outputs and error messages in a terminal-style canvas.
* **Modular Design**: Built with an MVC (Model-View-Controller) architecture for scalability.
* **Future Potential**: Plans for additional solvers (e.g., pipe sizing, heat loss) and isometric visualizations.

## Why This Project?

This app was born out of a desire to simplify duct sizing—a common task in building services engineering—while practicing core programming skills. It’s my first personal project, designed to break free from tutorial hell and tackle real-world problems I encounter at work. Think of it as a practical, no-nonsense tool with room to grow!

## How to Run

1.  **Clone the Repository**:
    ```bash
    git clone [https://github.com/your-username/engineering-solver](https://github.com/your-username/engineering-solver)
    ```
2.  **Install Dependencies**:
    * Requires Python 3.x (no external libraries needed yet—just pure Python and Tkinter!).
3.  **Launch the App**:
    ```bash
    cd engineering-solver
    python3 main.py
    ```
    * Enter duct parameters (e.g., width, height, flow rate) and hit "Calculate" to see results.

## Project Structure

* `main.py`: Application entry point and core loop.
* `ui.py`: Tkinter-based user interface with input fields and output display.
* `duct.py`: Calculation logic for duct properties (area, velocity, etc.).
* `controller.py`: Mediates between the UI and calculation logic.

## Usage Example

1.  Select "Rectangular" duct type.
2.  Input: Width = 400 mm, Height = 200 mm, Flow Rate = 300 L/s.
3.  Output: Area = 0.08 m², Velocity = 3.75 m/s.

## Roadmap

* Add more input validation and warnings (e.g., high velocity alerts).
* Visualize duct geometry with a simple isometric sketch.
* An arrow representing flow direction
* Add visual tags to duct geometry with values from input fields (Dimensions, Flow rates etc.)
* Expand to include the following inputs
    * Absolute Roughness of duct based on material and wear
    * Ambient temperature
    * Ambient relative humidity
    * Elevation
    * Noise directivity factor
    * Distance to noise source
* Expand to include the following duct calculations
    * Air Pressure
    * Dynamic Viscosity
    * Air Density
    * Aspect Ratio
    * Hydraulic Diameter
    * Reynold's number
    * Flow State based on Re
    * Altshul-Tsal friction factor
    * Pressure drop per unit meter
    * Loss coefficient of static vs dynamic
    * Sound ppwer level
    * Sound pressure level
* Add scrollable terminal canvas output to view output history 
* Add timestamps in terminal output for better history tracking
* Add PDF printout button to generate report with visualisation along with outputs

## Contributing

This is a personal learning project, but feedback is welcome! Feel free to open an issue or submit a pull request if you spot improvements.

## License

* Free to use, modify, and share.
