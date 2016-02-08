# Rhinoceros-Python-Scripts
A set of RhinoPython scripts for various transformations (flows) of 2D and 3D objects.


## Repository structure
  - *code/*: The actual Rhino Python scripts.
    - *curves/*: Flow implementations for 2D curves.
    - *meshes/*: Flow implementations for 3D meshes.
    - *utils/*: Various helper methods.
  - *shapes/*: Simple shapes that can be used for testing.
    - *curves/*: 2D curves: a basic polyline, a rectangle etc.
    - *meshes/*: 3D meshes: a cube, a dipyramid, a sphere etc.


## Usage
The code to be executed in Rhinoceros should go to *code/launcher.py*.
To launch it:
  1. Load the shape you want to transform (curve/mesh) to Rhinoceros
  2. Type *"_EditPythonScript"* in the command prompt of Rhinoceros
  3. Load & run the Python module *code/launcher.py*
  4. Click on the shape loaded to the Rhinoceros editor
     to apply the corresponding transformation to it.

## Notes
These scripts have been developed and tested on Rhinoceros 5 for Windows;
there may be some issues with running the same code on Rhinoceros 5 for Mac.
You are welcome to report any of them on GitHub.
