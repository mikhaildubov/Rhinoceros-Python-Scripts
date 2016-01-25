# test file for rhinopython scripting
# Pascal Romon 
# 2015-09-09 

from math import pi
import rhinoscriptsyntax as rs
    
def AddVector(vecdir, base_point=[0,0,0]):
    tip_point = rs.PointAdd(base_point, vecdir)
    line = rs.AddLine(base_point, tip_point)
    if line: return rs.CurveArrows(line, 2) # adds an arrow tip
    
def Laplacemotion():
    pl_id = rs.GetObject("Select a polyline", rs.filter.curve, True, True)
    if pl_id is None: return
    step = 0.3
    length = rs.CurveLength(pl_id)
    #area = rs.CurveArea(pl_id)
    newvertices = []
    vertices = rs.PolylineVertices(pl_id)
    n = len(vertices)   # one more than the actual number of vertices

    # calcul du centre de gravite
    g = (0,0,0)
    for i in range(n-1):
        g = rs.VectorAdd(g,vertices[i])
    g = rs.VectorScale(g,1/(n-1))    
    rs.AddPoint(g)
    
    if vertices:
        for i in range(n-1):    # n-1 to avoid the last extra point
            if i > 0: prev = i-1 
            else:     prev = n-2
            next = i+1
            
            # 1. Computing the flow vector (H or V)
            e_i = rs.VectorSubtract(vertices[next],vertices[i])
            e_i_1 = rs.VectorSubtract(vertices[i],vertices[prev])
            v_i = rs.VectorUnitize(e_i)
            v_i_1 = rs.VectorUnitize(e_i_1)
            #vector = rs.VectorSubtract(e_i, e_i_1) # V = e_i - e_i-1
            vector = rs.VectorSubtract(v_i, v_i_1) # H = v_i - v_i-1

            # 2. Scaling the vecor
            # HOW TO CHOOSE THE NORMALIZATION COEFFICIENT FOR THE VECTOR? 
            # This doesn't work in all cases
            # vector = rs.VectorUnitize(vector)
            # This doesn't either
            # vector = rs.VectorScale(vector, step)
            # We can also square the length of the flow vector
            # (makes sense if it is H, not V)
            vector = rs.VectorScale(vector, rs.VectorLength(vector) ** 2)

            AddVector(vector, vertices[i])  # draws change vectors 
            newvertices.append(rs.PointAdd(vertices[i], vector))

        newvertices.append(newvertices[0]) # first point closes the polyline
#    newpl_id = rs.AddPolyline(newvertices, pl_id)  # replaces previous polyline
    newpl_id = rs.AddPolyline(newvertices)          # keeps previous polyline

    # Scale to preserve the same length
    # (otherwise the polyline converges to a point)
    newlength = rs.CurveLength(newpl_id)
    scaling = length / newlength
    #rs.ScaleObject(newpl_id, g, (scaling, scaling, scaling))
    # Alternatively, one cane scale it by area
    #newarea = rs.CurveArea(newpl_id)
    #scaling_area = area / newarea
    # rs.ScaleObject(newpl_id, g, (scaling_area, scaling_area, scaling_area))

    return(newpl_id)


def Laplacemotion_iterated():
    # TODO: Iterate the Laplacemoion, controlling (decreasing)
    #       the length of the flow vectors
    pass

if __name__ == "__main__":
    Laplacemotion()
