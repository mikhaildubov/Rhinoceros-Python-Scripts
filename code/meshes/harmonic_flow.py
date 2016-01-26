import rhinoscriptsyntax as rs
from utils import vector_utils as vu
from utils import mesh_utils as mu

""" Harmonic Flow a.k.a. Mean Curvature Flow (MCF) """


def flow(mesh_id=None, step=1):
    """Performs one step of the harmonic flow of the given mesh,
    replacing that mesh with a new one.
    """
    # TODO(mikhaildubov): This flow results in a degenerate case at the poles of sphere86.3dm.
    #                     Fix this by making it a true MCF (i.e. by using the angles).
    
    # If mesh_id is None, then get the mesh from the user.
    # Check that all its faces are correctly set up.
    mesh_id = mu.get_and_check_mesh(mesh_id)
    
    # Various precomputations (including motion vectors for each vertex)
    v = rs.MeshVertices(mesh_id)
    n = len(v)
    harmonic_vectors = get_motion_vectors(mesh_id, step)
    
    # Move each vertex by its motion vector
    new_vertices = []
    for i in xrange(n):
        new_vertices.append(rs.PointAdd(v[i], harmonic_vectors[i]))

    # Update the mesh
    new_mesh_id = rs.AddMesh(new_vertices, rs.MeshFaceVertices(mesh_id))
    rs.DeleteObject(mesh_id)
    return new_mesh_id


def adjacency_list(mesh_id):
    """Builds an adjacency list of the mesh, taking O(|V|+|E|) space."""
    n = rs.MeshVertexCount(mesh_id)
    adj = [set() for _ in xrange(n)]
    for face in rs.MeshFaceVertices(mesh_id):
        for i in xrange(len(face)):
            a = face[i]
            b = face[(i + 1) % len(face)]
            # NOTE: Rhinoceros occasionally has duplicate vertices in face representations,
            #       so we should prevent vertices from being adjacent to themselves in the list.
            if a != b:
                adj[a].add(b)
                adj[b].add(a)
    return adj


def get_motion_vectors(mesh_id, step):
    """Returns a list of motion vectors in the same order as the vertices in the
    Rhino representation of the input mesh. Uses adjacency list instead of adjacency
    matrix, thus improving the running time from O(|V|^2) to O(|V|+|E|).
    """
    adj_list = adjacency_list(mesh_id)
    v = rs.MeshVertices(mesh_id)
    n = len(v)
    harmonic_vectors = []
    for i in xrange(n):
        # Initialize the harmonic vector as a zero vector
        harmonic_vector = rs.VectorCreate([0, 0, 0], [0, 0, 0])
        # Sum up all the vectors pointing to adjacent vertices
        adj = get_adjacent_vertices_in_order(adj_list, i)
        for j in xrange(len(adj)):
            prev = v[adj[(j - 1) % len(adj)]]
            curr = v[adj[j]]
            next = v[adj[(j + 1) % len(adj)]]
            pq = rs.VectorCreate(curr, v[i])
            # TODO: the cotangent formula should go here
            harmonic_vector = rs.VectorAdd(harmonic_vector, pq)
        # Reverse & rescale
        harmonic_vector = rs.VectorReverse(harmonic_vector)
        harmonic_vector = vu.VectorResize(harmonic_vector, step)
        harmonic_vectors.append(harmonic_vector)
    return harmonic_vectors


def get_adjacent_vertices_in_order(adj_list, i):
    # TODO: This is a stub
    # TODO: Consider building the list in order right from the beginning?
    return list(adj_list[i])


def draw_motion_vectors(mesh_id=None, step=1):
    """Draws the motion vectors for the harmonic flow of the given mesh."""
    mesh_id = mu.get_and_check_mesh(mesh_id)
    harmonic_vectors = get_motion_vectors(mesh_id, step)
    v = rs.MeshVertices(mesh_id)
    n = len(v)
    for i in xrange(n):
        vu.VectorDraw(harmonic_vectors[i], v[i])
