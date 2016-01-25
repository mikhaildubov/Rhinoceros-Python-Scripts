import rhinoscriptsyntax as rs

def VectorDraw(vecdir, base_point=[0,0,0]):
    """Draws a vector starting at the given base point."""
    tip_point = rs.PointAdd(base_point, vecdir)
    line = rs.AddLine(base_point, tip_point)
    if line: return rs.CurveArrows(line, 2) # adds an arrow tip
    
def VectorResize(vector, length):
    """Returns a copy of the vector resized to the given length."""
    return rs.VectorScale(vector, length / rs.VectorLength(vector))
