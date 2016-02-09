import os
import rhinoscriptsyntax as rs
import shutil
import tempfile


def iterate(flow_func, iterations, gif_path=None, *args, **kwargs):
    """Performs the given number of iterations of an arbitrary flow function,
    passing specific arguments to that function (those may include the curve/mesh id).
    Useful for animated flow rendering in RhinoPython.
    """
    can_generate_gif = gif_path is not None
    
    if can_generate_gif:
        # Generate a temporary folder to store frames captured during each iteration.
        temp_dir = tempfile.mkdtemp()

    # Iterate the flow function. If the user wants to generate the gif animation,
    # capture each frame into a file in the temporary folder.
    obj_id = None
    for i in range(iterations):
        if can_generate_gif:
            rs.Command("-ViewCaptureToFile %s _Enter" % os.path.join(temp_dir, "%08i.png" % i))
        obj_id = flow_func(obj_id, *args, **kwargs)

    if can_generate_gif:
        # Don't forget to capture the last frame.
        rs.Command("-ViewCaptureToFile %s _Enter" % os.path.join(temp_dir, "%08i.png" % i))

        # NOTE(mikhaildubov): The Pillow (PIL) package should be installed to generate gif animation.
        # NOTE(mikhaildubov): We make a system call to the python interpreter to launch the gif
        #                     compilation script here. That's because Rhinoceros 5 uses its own
        #                     IronPython interpreter, and it may be rather difficult to make 
        #                     third-party libraries available to it.
        script = os.path.join(os.path.dirname(os.path.abspath(__file__)), "scripts", "create_gif.py")
        os.system('python "%s" "%s" "%s"' % (script, gif_path, temp_dir))

        # Delete the temporary folder with all the frames inside it.
        shutil.rmtree(temp_dir)

    return obj_id
