from meshes import harmonic_flow, face_flow
from utils import flow_utils
import rhinoscriptsyntax as rs


""" The entry point to be launched in Rhinoceros. """


if __name__ == '__main__':
    # NOTE(mikhaildubov): The code to be executed in Rhinoceros should go here.
    #
    #                     To launch any of the commands below:
    #                       1. Load the corresponding shape (curve/mesh) to Rhinoceros
    #                       2. Type "_EditPythonScript" in the command prompt of Rhinoceros
    #                       3. Load & run this python module
    #                       4. Click on the shape loaded to the Rhinoceros editor
    #                          to apply the corresponding transformation to it.

    # MESHES

    # Harmonic flow (Mean Curvature flow)
    #harmonic_flow.draw_motion_vectors(step=10)
    #flow_utils.iterate(harmonic_flow.flow, 200, step=0.05)

    # Face flow
    #face_flow.draw_motion_vectors(step=10)
    flow_utils.iterate(face_flow.flow, 200, step=0.05)
