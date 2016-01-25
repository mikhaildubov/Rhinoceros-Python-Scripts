
def iterate(flow_func, iterations, *args, **kwargs):
    """Performs the given number of iterations of an arbitrary flow function,
    passing specific arguments to that function (those may include the curve/mesh id).
    Useful for animated flow rendering in RhinoPython.
    """
    obj_id = None
    for i in range(iterations):
        obj_id = flow_func(obj_id, *args, **kwargs)
    return obj_id
