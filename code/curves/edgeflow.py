# Edge flow
# Mikhail Dubov
# 2015-11-24

from math import pi, sin, tan, degrees
import rhinoscriptsyntax as rs

from utils import vector_utils as vu


# Some shortcuts for vector operations to improve code readability
unit = rs.VectorUnitize
subtract = rs.VectorSubtract
scale = rs.VectorScale
rev = rs.VectorReverse
length = rs.VectorLength
angle = vu.VectorAngleRadians


def AddVector(vecdir, base_point=None):
    # Draws a vector (for visualization purposes)
    base_point = base_point or [0, 0, 0]
    tip_point = rs.PointAdd(base_point, vecdir)
    line = rs.AddLine(base_point, tip_point)
    if line: return rs.CurveArrows(line, 2) # adds an arrow tip


def edgeflow(pl_id=None, step="unit"):
    # Step type should be one of: "unit", "curvature"
    # TODO: just numbers instead of "unit"

    # NOTE: By convention, we expect a ccw-oriented curve here
    pl_id = pl_id or rs.GetObject("Select a polyline", rs.filter.curve, True, True)
    if pl_id is None: return
    
    newvertices = []
    vertices = rs.PolylineVertices(pl_id)
    n = len(vertices)
    
    if vertices:
        # We will need two vertices after and two before vertex[i]
        for i in range(n - 1):    # (n - 1) to avoid the last extra point
            if i > 1:
                prev = i - 1
                prev_prev = i - 2
            elif i == 1:
                prev = 0
                prev_prev = n - 2
            elif i == 0:
                prev = n - 2
                prev_prev = n - 3
            next = i + 1
            if i < n - 2:
                next_next = i + 2
            else:
                next_next = 1
            
            # Edge [unit] vectors and the angle between them
            l_i = subtract(vertices[next], vertices[i])
            l_j = subtract(vertices[i], vertices[prev])
            v_i = unit(l_i)
            v_j = unit(l_j)
            a = angle(rev(v_i), v_j)
            
            # Lengths of normal vectors
            if step == "unit":
                n_i_len = 1.0
                n_j_len = 1.0
            elif step == "curvature":
                # Two more edges needed for the computation
                v_i_next = unit(subtract(vertices[next_next], vertices[next]))
                v_j_prev = unit(subtract(vertices[prev], vertices[prev_prev]))
                # Exterior angles
                t1 = pi - angle(rev(v_j), v_j_prev)
                t2 = pi - a
                t3 = pi - angle(rev(v_i_next), v_i)
                n_i_len = (tan(t2 / 2) + tan(t3 / 2)) / length(l_i)
                n_j_len = (tan(t1 / 2) + tan(t2 / 2)) / length(l_j)
            
            # The solution to the edge flow problem obtained geometrically in class
            motion_vec = subtract(scale(v_i, n_i_len / sin(a)), scale(v_j, n_j_len / sin(a)))

            AddVector(motion_vec, vertices[i])  # draws change vectors 
            newvertices.append(rs.PointAdd(vertices[i], motion_vec))

        newvertices.append(newvertices[0]) # first point closes the polyline

#    newpl_id = rs.AddPolyline(newvertices, pl_id)  # replaces previous polyline
    newpl_id = rs.AddPolyline(newvertices)          # keeps previous polyline
    
    return newpl_id


def iterate(flow_func, iterations, *args):
    pl_id = None
    for i in range(10):
        pl_id = flow_func(pl_id, *args)
    return pl_id


if __name__ == "__main__":
    iterate(edgeflow, None, "curvature")
    #iterate(edgeflow, None, "unit")
