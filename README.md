# Random Open Circles Generator

### Overview
The **Random Open Circles Generator** is a Python script for Autodesk Maya that generates randomized, open NURBS circles on selected polygon mesh surfaces. This tool provides customization options and utilities for live updates and curve management.

### Features
- Generate **randomized open NURBS circles** aligned to surface normals and positioned randomly across polygon faces.
- Customizable parameters:
  - Number of circles
  - Minimum and maximum radius
  - Number of sections (4–100)
  - Random seed for reproducibility
- Integrated live update mode for real-time adjustments.
- Curve management utilities:
  - Reverse curves
  - Attach curves
  - Smooth curves
  - Curl curves
  - Delete history
- Reset parameters to default values with a single click.

### Installation
1. Clone this repository:
   ```bash
   git clone https://github.com/hsuehyt/RandomOpenCirclesGenerator.git
   ```
2. Locate the script file:
   - `random_open_circles_generator.py`
3. Open Autodesk Maya.
4. Load the script in Maya:
   - Copy and paste the script into Maya's Script Editor or load it via the Python tab.

### Usage
1. **Run the Script**:
   - Execute the script to open the user interface (UI).
2. **Select a Mesh**:
   - Select a polygon mesh where you want the circles to be generated.
3. **Adjust Parameters**:
   - Set the number of circles, radius range, sections, and other options in the UI.
4. **Generate Circles**:
   - Click the `Generate Circles` button to create the circles on the selected mesh.
5. **Use Curve Management Tools**:
   - Utilize buttons like `Reverse Curves`, `Attach Curves`, `Curl Curves`, `Smooth Curves`, or `Delete History` to manage generated curves.

### Buttons Description
- **Generate Circles**: Creates randomized open NURBS circles based on the current settings.
- **Reverse Curves**: Opens Maya's `Reverse Curve Options` window to reverse the direction of selected curves.
- **Attach Curves**: Opens Maya's `Attach Curves Options`.
- **Delete History**: Deletes construction history of the selected objects.
- **Curl Curves**: Opens Maya's `Curl Curves Options`.
- **Smooth Curves**: Opens Maya's `Smooth Curves Options`.
- **Reset to Default**: Resets all parameters to their default values.

### Requirements
- Autodesk Maya 2023 or later.
- Python 2.7+ (integrated with Maya).

### License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

### Contribution
Feel free to submit pull requests or raise issues for enhancements or bug fixes. Contributions are welcome!

### Author
[Hsuehyt](https://github.com/hsuehyt)