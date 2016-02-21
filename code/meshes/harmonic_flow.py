import rhinoscriptsyntax as rs

from utils.math_utils import cotan
from utils import mesh_utils as mu
from utils import vector_utils as vu

""" Harmonic Flow a.k.a. Mean Curvature Flow (MCF) """


def flow(mesh_id=None, step=1):
    """Performs one step of the harmonic flow of the given mesh,
    replacing that mesh with a new one.
    """
    # TODO(mikhaildubov): This flow results in a degenerate case at the poles of sphere134.3dm.
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


def vertex_face_index(mesh_id):
    """Returns an auxiliary index containing sets of adjacent faces for each vertex."""
    n = rs.MeshVertexCount(mesh_id)
    adj = [set() for _ in xrange(n)]
    for face_index, face_vertices in enumerate(rs.MeshFaceVertices(mesh_id)):
        for vertex_index in face_vertices:
            adj[vertex_index].add(face_index)
    return adj


def get_adjacent_vertices_in_order(mesh_id, adj_list, vertex_face_ind, i):
    adj_vertices = adj_list[i].copy()
    adj_vertices_in_order = [adj_vertices.pop()]
    face_vertices = rs.MeshFaceVertices(mesh_id)

    def get_next_vertex(last_vertex):
        for adj_face in vertex_face_ind[last_vertex]:
            for vertex in face_vertices[adj_face]:
                if vertex in adj_vertices:
                    return vertex
        # NOTE(mikhaildubov): Depending on the mesh, we may need to get the last one manually
        #                     (e.g. this is the case for a dipyramid).
        return list(adj_vertices)[0]

    while adj_vertices:
        last_vertex = adj_vertices_in_order[-1]
        next_vertex = get_next_vertex(last_vertex)
        adj_vertices.remove(next_vertex)
        adj_vertices_in_order.append(next_vertex)
        last_vertex = next_vertex

    return adj_vertices_in_order


def get_motion_vectors(mesh_id, step):
    """Returns a list of motion vectors in the same order as the vertices in the
    Rhino representation of the input mesh. Uses adjacency list instead of adjacency
    matrix, thus improving the running time from O(|V|^2) to O(|V|+|E|).
    """
    adj_list = adjacency_list(mesh_id)
    vertex_face_ind = vertex_face_index(mesh_id)
    v = rs.MeshVertices(mesh_id)
    n = len(v)
    harmonic_vectors = []
    for i in xrange(n):
        p = v[i]
        # Initialize the harmonic vector as a zero vector
        harmonic_vector = rs.VectorCreate([0, 0, 0], [0, 0, 0])
        # Sum up all the vectors pointing to adjacent vertices
        adj = get_adjacent_vertices_in_order(mesh_id, adj_list, vertex_face_ind, i)
        for j in xrange(len(adj)):
            # q_j vertices
            q_prev = v[adj[(j - 1) % len(adj)]]
            q_curr = v[adj[j]]
            q_next = v[adj[(j + 1) % len(adj)]]
            # pq vectors
            pq_prev = rs.VectorCreate(q_prev, p)
            pq = rs.VectorCreate(q_curr, p)
            pq_next = rs.VectorCreate(q_next, p)
            # vectors between q vertices
            q_prev_q_curr = rs.VectorCreate(q_curr, q_prev)
            q_next_q_curr = rs.VectorCreate(q_curr, q_next)
            # Angles needed for MCF
            alpha = vu.VectorAngleRadians(rs.VectorReverse(pq), q_prev_q_curr)
            beta = vu.VectorAngleRadians(rs.VectorReverse(pq), q_next_q_curr)
            # Continue computing the sum for the harmonic vector
            # TODO(mikhaildubov): The formula with cotangents fails on sphere134.3dm.
            #                     Check it and also ensure that the input mesh is triangulated.
            harmonic_coeff = 1 #(cotan(alpha) + cotan(beta)) / 2
            harmonic_vector = rs.VectorScale(rs.VectorAdd(harmonic_vector, pq), harmonic_coeff)
        # Rescale
        # TODO(mikhaildubov): use this for true MCF:
        #harmonic_vector = rs.VectorScale(harmonic_vector, step)
        harmonic_vector = vu.VectorResize(harmonic_vector, step)
        harmonic_vectors.append(harmonic_vector)
    return harmonic_vectors


def draw_motion_vectors(mesh_id=None, step=1):
    """Draws the motion vectors for the harmonic flow of the given mesh."""
    mesh_id = mu.get_and_check_mesh(mesh_id)
    harmonic_vectors = get_motion_vectors(mesh_id, step)
    v = rs.MeshVertices(mesh_id)
    n = len(v)
    for i in xrange(n):
        vu.VectorDraw(harmonic_vectors[i], v[i])
