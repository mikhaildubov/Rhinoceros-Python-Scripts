from meshes import harmonic_flow, face_flow
from utils import flow_utils
import rhinoscriptsyntax as rs


""" The entry point to be launched in Rhinoceros. """


if __name__ == '__main__':
    # NOTE(mikhaildubov): The code to be executed in Rhinoceros should go here

    #harmonic_flow.draw_motion_vectors(step=10)
    #flow_utils.iterate(harmonic_flow.flow, 200, step=0.05)
    #face_flow.draw_motion_vectors(step=10)
    flow_utils.iterate(face_flow.flow, 200, step=0.05)
