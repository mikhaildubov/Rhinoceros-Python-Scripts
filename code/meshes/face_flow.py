import rhinoscriptsyntax as rs
from utils import vector_utils as vu
from utils import mesh_utils as mu
from utils import math_utils as maths

""" Face Flow (3D analog of the Edge Flow for curves) """
    

def flow(mesh_id=None, step=1):
    """Performs one step of the face flow of the given mesh,
    replacing that mesh with a new one.
    """
    # If mesh_id is None, then get the mesh from the user.
    # Check that all its faces are correctly set up.
    mesh_id = mu.get_and_check_mesh(mesh_id)
    
    # Various precomputations (including motion vectors for each face)
    normals = get_motion_vectors(mesh_id, step)
    adj_faces = adjacent_faces(mesh_id)
    n = len(rs.MeshVertices(mesh_id))
    face_planes = mu.get_face_planes(mesh_id)
    
    # Shift all the planes by their normal vectors.
    # NOTE(mikhaildubov): This computation relies on the fact that normals are
    #                     listed in the same order as the corresponding faces.
    face_planes_translated = [translate_plane(face_planes[i], normals[i])
                              for i in xrange(len(face_planes))]

    # Calculate the intersections of the shifted planes.
    # Those are going to be the vertices of the updated mesh.
    new_vertices = []
    for i in xrange(n):
        adj_planes = [face_planes_translated[j] for j in adj_faces[i]]
        adj_planes_eq = [rs.PlaneEquation(plane) for plane in adj_planes]
        intersection_point = planes_intersection(adj_planes_eq)
        new_vertices.append(intersection_point)

    # Update the mesh
    new_mesh_id = rs.AddMesh(new_vertices, rs.MeshFaceVertices(mesh_id))
    rs.DeleteObject(mesh_id)
    return new_mesh_id


def get_motion_vectors(mesh_id, step):
    """Returns a list of motion vectors (for face flow, they are just normals)
    in the same order as the faces in the Rhino representation of the input mesh.
    """
    normals = rs.MeshFaceNormals(mesh_id)
    for i in xrange(len(normals)):
        normals[i] = vu.VectorResize(normals[i], step)
    return normals


def draw_motion_vectors(mesh_id=None, step=1):
    """Draws the motion vectors for the face flow of the given mesh."""
    mesh_id = mu.get_and_check_mesh(mesh_id)
    normals = get_motion_vectors(mesh_id, step)
    centers = rs.MeshFaceCenters(mesh_id)
    for i in xrange(len(normals)):
        vu.VectorDraw(normals[i], centers[i])


def translate_plane(plane, vector):
    """Shifts the input plane by the given vector."""
    translation = rs.XformTranslation(vector)
    return rs.PlaneTransform(plane, translation)


def adjacent_faces(mesh_id):
    """Constructs a set of adjacent faces for each vertex.
    Returns a list of form
        [
          [0] set([face_index_1, face_index_2, ...])
          [1] set([face_index_1, ...])
              ...
        ]
    """
    vertices = rs.MeshVertices(mesh_id)
    face_vertices = rs.MeshFaceVertices(mesh_id)
    adjacency_list = [set() for _ in xrange(len(vertices))]
    for face_index in xrange(len(face_vertices)):
        for vertex_index in face_vertices[face_index]:
            adjacency_list[vertex_index].add(face_index)
    return adjacency_list

    
def planes_intersection(plane_eqs):
    """Computes the intersection point for n >= 3 planes."""

    if len(plane_eqs) < 3:
        raise Exception("There should be at least 3 planes to calculate their intersection point.")

    # Compute the intersection of the first three planes.
    matrix = [
        [plane_eqs[0][0], plane_eqs[0][1], plane_eqs[0][2], -plane_eqs[0][3]],
        [plane_eqs[1][0], plane_eqs[1][1], plane_eqs[1][2], -plane_eqs[1][3]],
        [plane_eqs[2][0], plane_eqs[2][1], plane_eqs[2][2], -plane_eqs[2][3]],
    ]
    # NOTE(mikhaildubov): As we are working with mesh geometry, we can be sure there are
    #                     no major degeneracies (like three planes intersecting in a line).
    intersection_candidate = maths.solve_sle(matrix)

    # Check that the rest of the planes are compatible with this intersection.
    for plane_eq in plane_eqs[3:]:
        if not plane_contains(plane_eq, intersection_candidate):
            raise Exception("The motion of planes is incompatible")

    return intersection_candidate


def plane_contains(plane_eq, point):
    return maths.is_approx_zero(plane_eq[0] * point[0] + plane_eq[1] * point[1] +
                                plane_eq[2] * point[2] + plane_eq[3])

