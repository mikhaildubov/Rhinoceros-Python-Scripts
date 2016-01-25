import rhinoscriptsyntax as rs

def get_and_check_mesh(mesh_id=None):
    """If mesh_id is None, retrieves the mesh from the user.
    Checks that all its faces are correctly set up.
    """
    mesh_id = mesh_id or rs.GetObject("Select a mesh")
    check_mesh(mesh_id)
    return mesh_id


def check_mesh(mesh_id):
    """Checks that all the faces are "flat" i.e. each face defines a plane."""
    # TODO(mikhaildubov): Consider adding a check for the normals orientation consistency.
    #                     This seems to be not a trivial problem; see e.g.
    #                     http://jcgt.org/published/0003/04/02/paper.pdf
    if any(plane is None for plane in get_face_planes(mesh_id)):
        raise Exception("There is an invalid face which does not represent any plane.")


def add_cube(side=1):
    """Adds a cube with the given side to Rhinoceros."""
    vertices = [(0, 0, 0), (side, 0, 0), (side, side, 0), (0, side, 0),
                (0, 0, side), (side, 0, side), (side, side, side), (0, side, side)]
    face_vertices = [(0, 3, 2, 1), (4, 5, 6, 7), (0, 1, 5, 4),
                     (1, 2, 6, 5), (2, 3, 7, 6), (3, 0, 4, 7)]
    return rs.AddMesh(vertices, face_vertices)


def get_face_points(mesh_id, face_index):
    """Returns a list of vertices that define the given face. The face_index argument
    should correspond to the order of faces as returned from rs.MeshFaceVertices().
    """
    vertices = rs.MeshVertices(mesh_id)
    face_vertices = rs.MeshFaceVertices(mesh_id)
    return [vertices[i] for i in face_vertices[face_index]]


def get_face_planes(mesh_id):
    """Returns a list of planes corresponding to the faces of the given mesh.
    The elements of the list are Plane objects and come in the same order as
    the faces returned from rs.MeshFaceVertices().
    """
    f = rs.MeshFaceCount(mesh_id)
    return [rs.PlaneFitFromPoints(get_face_points(mesh_id, i)) for i in xrange(f)]
