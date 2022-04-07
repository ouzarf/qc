import matplotlib.pyplot as plt

def show_figure(fig):
    """
       Function outputs the given plot

       Note: this should only be used with the "mpl" output type
    """
    new_fig = plt.figure()
    new_mngr = new_fig.canvas.manager
    new_mngr.canvas.figure = fig
    fig.set_canvas(new_mngr.canvas)
    plt.show(fig)
