# Rhinoceros Python Scripts
This is a set of Python scripts for various transformations (flows) of 2D and 3D objects in [Rhinoceros 5](https://www.rhino3d.com/), a popular 3D modeler.


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
  2. Type *"EditPythonScript"* in the command prompt of Rhinoceros
  3. Load & run the Python module *code/launcher.py*
  4. Click on the shape loaded to the Rhinoceros editor
     to apply the corresponding transformation to it.


## Examples
Here is how harmonic flows and face flows of a cube, a dipyramid, and a sphere look like. The harmonic flows are presented on the left while face flows are on the right:

|                                                             **Harmonic flow**                                                             |                                                             **Face flow**                                                             |
|:-------------------------------------------------------------------------------------------------------------------------------------:|:---------------------------------------------------------------------------------------------------------------------------------:|
| ![Harmonic flow of a cube](https://cloud.githubusercontent.com/assets/1047242/13200353/319d6496-d844-11e5-9ad6-e5317edb81d6.gif)      | ![Face flow of a cube](https://cloud.githubusercontent.com/assets/1047242/13200352/31996be8-d844-11e5-926f-587c97803682.gif)      |
| ![Harmonic flow of a dipyramid](https://cloud.githubusercontent.com/assets/1047242/13200355/319ee654-d844-11e5-8fd4-b51797d5a2fe.gif) | ![Face flow of a dipyramid](https://cloud.githubusercontent.com/assets/1047242/13200354/319da744-d844-11e5-9c2f-9d462ef80af8.gif) |
| ![Harmonic flow of a sphere](https://cloud.githubusercontent.com/assets/1047242/13200357/31a48244-d844-11e5-8764-fbcb19464d80.gif)    | ![Face flow of a sphere](https://cloud.githubusercontent.com/assets/1047242/13200356/31a3ae00-d844-11e5-8832-d085dcaaaf6a.gif)    |


## Dependencies
  - [Pillow (PIL)](https://pypi.python.org/pypi/Pillow/3.1.1): required
    for the flow animation export to GIF in the *flow_utils.iterate()* function.
    In case this package is missing, the code will not fail but no GIF files will be produced.


## Notes
This repository has been inspired by the course "Discrete Differential Geometry",
taught by Pascal Romon at Université Paris-Est Marne-la-Vallée in the Fall 2015.

The scripts have been developed and tested on Rhinoceros 5 for Windows, so
there may be some issues with running the same code on Rhinoceros 5 for Mac.
You are welcome to report any of them here.


## References
- [Rhino Python Programmer's Reference](http://4.rhino3d.com/5/ironpython/index.html)
- [Pascal Romon - Introduction à la géométrie différentielle discrète](http://www.amazon.fr/Introduction-%C3%A0-G%C3%A9ometrie-Diff%C3%A9rentielle-Discr%C3%A8te/dp/272988307X)
