# Curve decomposition to lengths/angles; contruction of curves from them
# Mikhail Dubov
# 2015-11-24

from math import pi, radians
import rhinoscriptsyntax as rs


# Some shortcuts for vector operations to improve code readability
subtract = rs.VectorSubtract
rev = rs.VectorReverse
length = rs.VectorLength

def angle(v1, v2):
    # rs.VectorAngle returns degrees which is not very convenient
    return radians(rs.VectorAngle(v1, v2))

    
def decompose(polyline=None):
    # Returns a pair (lengths, angles). Angles are in radians.
    polyline = polyline or rs.GetObject("Select a polyline", rs.filter.curve, True, True)
    if polyline is None: return
    
    vertices = rs.PolylineVertices(polyline)
    n = len(vertices)
    
    lengths = []
    angles = []
    
    if vertices:
        for i in range(n-1):    # n-1 to avoid the last extra point
            if i > 0: prev = i-1 
            else:     prev = n-2
            next = i+1
            
            l_i = subtract(vertices[next], vertices[i])
            l_j = subtract(vertices[i], vertices[prev])
            
            lengths.append(length(l_i))
            # TODO: assumes that we have always a left turn.
            #       what if the polyline is not convex?
            angles.append(pi - angle(rev(l_i), l_j))
    
    return lengths, angles


def construct(lengths, angles):
    # TODO: Construct a polyline
    pass

if __name__ == "__main__":
    print decompose()
