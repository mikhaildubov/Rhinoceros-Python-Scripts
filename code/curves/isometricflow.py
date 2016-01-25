# Edge flow
# Mikhail Dubov
# 2015-11-24

from math import radians, pi, sin, tan
import rhinoscriptsyntax as rs


# Some shortcuts for vector operations to improve code readability
unit = rs.VectorUnitize
subtract = rs.VectorSubtract
scale = rs.VectorScale
rev = rs.VectorReverse
length = rs.VectorLength
rotate = rs.VectorRotate

def angle(v1, v2):
    # rs.VectorAngle returns degrees which is not very convenient
    return radians(rs.VectorAngle(v1, v2))


def AddVector(vecdir, base_point=None):
    # Draws a vector (for visualization purposes)
    base_point = base_point or [0, 0, 0]
    tip_point = rs.PointAdd(base_point, vecdir)
    line = rs.AddLine(base_point, tip_point)
    if line: return rs.CurveArrows(line, 2) # adds an arrow tip


def isometricflow(polyline=None, t=0.1):

    polyline = polyline or rs.GetObject("Select a polyline", rs.filter.curve, True, True)
    if polyline is None: return
    
    vertices = rs.PolylineVertices(polyline)
    n = len(vertices) - 1
    
    lengths = []
    angles = []
    
    if vertices:
        for i in range(n):
            if i > 0: prev = i-1 
            else:     prev = n-1
            next = i+1
            
            l_i = subtract(vertices[next], vertices[i])
            l_j = subtract(vertices[i], vertices[prev])
            
            lengths.append(length(l_i))
            # TODO: Is this working only for convex polygons? Does rs.VectorAngle return negative values when it's not convex?
            angles.append(angle(l_i, l_j))
    
        angles_sum = sum(angles)
        
        for a in angles:
            a = a - t * (a - angles_sum / n)
            
        prev_edge = subtract(vertices[1], vertices[0])
        newvertices = [vertices[0]]
        for i in range(1, n):
            newvertices.append(rs.PointAdd(newvertices[-1], prev_edge))
            next_edge = scale(unit(rotate(prev_edge, angles[i], [0, 0, 1])), lengths[i])
            prev_edge = next_edge

        newvertices.append(newvertices[0]) # first point closes the polyline

#    new_polyline = rs.AddPolyline(newvertices, polyline)  # replaces previous polyline
    new_polyline = rs.AddPolyline(newvertices)          # keeps previous polyline
    
    return new_polyline
    
    
def iterate(flow_func, iterations, *args):
    pl_id = None
    for i in xrange(iterations):
        pl_id = flow_func(pl_id, *args)
    return pl_id



if __name__ == "__main__":
    iterate(isometricflow, 1)
    #iterate(isometricflow, 1)
