from meshes import harmonic_flow, face_flow
from utils import flow_utils
import rhinoscriptsyntax as rs


""" The entry point to be launched in Rhinoceros. """


if __name__ == '__main__':
    # NOTE(mikhaildubov): The code to be executed in Rhinoceros should go here.
    #
    # To launch any of the commands below:
    #   1. Load the shape you want to transform (curve/mesh) to Rhinoceros
    #   2. Type "EditPythonScript" in the command prompt of Rhinoceros
    #   3. Load & run this python module
    #   4. Click on the shape loaded to the Rhinoceros editor
    #      to apply the corresponding transformation to it.

    # ===== MESHES =====

    # -- Harmonic flow (a.k.a. Mean Curvature flow) --
    #harmonic_flow.draw_motion_vectors(step=10)
    #flow_utils.iterate(harmonic_flow.flow, 100, step=0.05)

    # --               Face flow                    --
    #face_flow.draw_motion_vectors(step=10)
    flow_utils.iterate(face_flow.flow, 100, step=0.05)


    # To record the flow animation into a gif file, just provide the path to the file
    # to be created via the 'gif_path' argument. Note that the Pillow (PIL) package
    # should be installed in your default Python interpreter in order for this to work.
    # If the Pillow package is missing, this code will not fail but no GIF file will be produced.
    #flow_utils.iterate(face_flow.flow, 100, step=0.05,
    #                   gif_path="path/to/your/animation.gif")
