import rhinoscriptsyntax as rs
from utils import vector_utils as vu
from utils import mesh_utils as mu
from utils import math_utils as maths

""" Face Flow (3D analog of the Edge Flow for curves) """


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

    
def three_planes_intersection(plane_eq_1, plane_eq_2, plane_eq_3):
    """Computes the intersection point for 3 planes."""
    matrix = [
        [plane_eq_1[0], plane_eq_1[1], plane_eq_1[2], -plane_eq_1[3]],
        [plane_eq_2[0], plane_eq_2[1], plane_eq_2[2], -plane_eq_2[3]],
        [plane_eq_3[0], plane_eq_3[1], plane_eq_3[2], -plane_eq_3[3]],
    ]
    return maths.solve_sle(matrix)

    
def four_planes_intersection(plane_eq_1, plane_eq_2, plane_eq_3, plane_eq_4):
    """Computes the intersection point for 4 planes."""
    # TODO(mikhaildubov): Implement this
    raise NotImplementedError()
    

def flow(mesh_id=None, step=1):
    """Preforms one step of the harmonic flow of the given mesh,
    replacing that mesh with a new one.
    """
    # If mesh_id is None, get the mesh from the user.
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
        if len(adj_planes) == 3:
            intersection_point = three_planes_intersection(*adj_planes_eq)
            new_vertices.append(intersection_point)
        elif len(adj_planes) == 4:
            # TODO(mikhaildubov): Check somehow that this intersection is actually possible.
            intersection_point = four_planes_intersection(*adj_planes_eq)
            new_vertices.append(intersection_point)
        else:
            # NOTE(mikhaildubov): We only support cases when each vertex has <= 4 adjacent planes.
            raise NotImplementedError()

    # Update the mesh
    new_mesh_id = rs.AddMesh(new_vertices, rs.MeshFaceVertices(mesh_id))
    rs.DeleteObject(mesh_id)
    return new_mesh_id
