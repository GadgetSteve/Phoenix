"""
demo.py
=======

This is a demo showing some of the capabilities of matokitlib
package within wx. It is intended to be run as a standalone script via::

  user@host:.../site-packages/wx/lib/mpl_plot$ python examples/mpl_demo.py

"""
__docformat__ = "restructuredtext en"


import wx
import wx.lib.agw.aui as aui
import wx.lib.mixins.inspection as wit

# Needs NumPy
try:
    import numpy as np
except ImportError:
    msg = """
    This module requires the NumPy module, which could not be
    imported.  It probably is not installed (it's not part of the
    standard Python distribution). See the Numeric Python site
    (http://numpy.scipy.org) for information on downloading source or
    binaries, or just try `pip install numpy` and it will probably
    work."""
    raise ImportError("NumPy not found.\n" + msg)

# Needs matplotlib
try:
    import matplotlib as mpl
except ImportError:
    msg = """
    This module requires the matplotlib module, which could not be
    imported.  It probably is not installed (it's not part of the
    standard Python distribution). See the Mat Plot Lib site
    (http://matplotlib.org) for information on downloading source or
    binaries, or just try `pip install matplotlib` and it will probably
    work."""
    raise ImportError("matplotlib not found.\n" + msg)
# If the above works the following shouldn't have a problem
from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as FigureCanvas
from matplotlib.backends.backend_wxagg import NavigationToolbar2WxAgg as NavigationToolbar
from matplotlib.ticker import AutoMinorLocator, MultipleLocator, FuncFormatter

from matplotlib import cm
try: # Just in case the user doesn't have mpl_toolkits
    from mpl_toolkits.mplot3d import Axes3D
except ImportError:
    Axes3D = None


class Plot(wx.Panel):
    def __init__(self, parent, id=-1, dpi=None, **kwargs):
        wx.Panel.__init__(self, parent, id=id, **kwargs)
        self.figure = mpl.figure.Figure(dpi=dpi, figsize=(4, 4))
        self.canvas = FigureCanvas(self, -1, self.figure)
        self.toolbar = NavigationToolbar(self.canvas)
        self.toolbar.Realize()

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.canvas, 1, wx.EXPAND)
        sizer.Add(self.toolbar, 0, wx.LEFT | wx.EXPAND)
        self.SetSizer(sizer)


class PlotNotebook(wx.Panel):
    def __init__(self, parent, id=-1):
        wx.Panel.__init__(self, parent, id=id)
        self.nb = aui.AuiNotebook(self)
        sizer = wx.BoxSizer()
        sizer.Add(self.nb, 1, wx.EXPAND)
        self.SetSizer(sizer)

    def add(self, name="plot"):
        page = Plot(self.nb)
        self.nb.AddPage(page, name)
        return page.figure


def demo():
    # alternatively you could use
    #app = wx.App()
    # InspectableApp is a great debug tool, see:
    # http://wiki.wxpython.org/Widget%20Inspection%20Tool
    app = wit.InspectableApp()
    frame = wx.Frame(None, -1, 'Plotter')
    plotter = PlotNotebook(frame)
    page1(plotter)
    page2(plotter)
    if Axes3D:
        page3d(plotter)
    page4(plotter)
    frame.SetMinSize((400, 400))
    
    frame.Show()
    app.MainLoop()


def page4(plotter):
    """ Add a plot anatomy  page."""

    def minor_tick(x, pos):
        if not x % 1.0:
            return ""
        return "%.2f" % x    
    
    def circle(x, y, radius=0.15):
        from matplotlib.patches import Circle
        from matplotlib.patheffects import withStroke
        circle = Circle((x, y), radius, clip_on=False, zorder=10, linewidth=1,
                        edgecolor='black', facecolor=(0, 0, 0, .0125),
                        path_effects=[withStroke(linewidth=5, foreground='w')])
        ax.add_artist(circle)
    
    
    def text(x, y, text):
        ax.text(x, y, text, backgroundcolor="white",
                ha='center', va='top', weight='bold', color='blue')
            
    ax = plotter.add('Anatomy').gca()
    np.random.seed(19680801)
    
    X = np.linspace(0.5, 3.5, 100)
    Y1 = 3+np.cos(X)
    Y2 = 1+np.cos(1+X/0.75)/2
    Y3 = np.random.uniform(Y1, Y2, len(X))    
    ax.xaxis.set_major_locator(MultipleLocator(1.000))
    ax.xaxis.set_minor_locator(AutoMinorLocator(4))
    ax.yaxis.set_major_locator(MultipleLocator(1.000))
    ax.yaxis.set_minor_locator(AutoMinorLocator(4))
    ax.xaxis.set_minor_formatter(FuncFormatter(minor_tick))
    
    ax.set_xlim(0, 4)
    ax.set_ylim(0, 4)
    
    ax.tick_params(which='major', width=1.0)
    ax.tick_params(which='major', length=10)
    ax.tick_params(which='minor', width=1.0, labelsize=10)
    ax.tick_params(which='minor', length=5, labelsize=10, labelcolor='0.25')
    
    ax.grid(linestyle="--", linewidth=0.5, color='.25', zorder=-10)
    
    ax.plot(X, Y1, c=(0.25, 0.25, 1.00), lw=2, label="Blue signal", zorder=10)
    ax.plot(X, Y2, c=(1.00, 0.25, 0.25), lw=2, label="Red signal")
    ax.plot(X, Y3, linewidth=0,
            marker='o', markerfacecolor='w', markeredgecolor='k')
    
    ax.set_title("Anatomy of a figure", fontsize=20, verticalalignment='bottom')
    ax.set_xlabel("X axis label")
    ax.set_ylabel("Y axis label")
    
    ax.legend()
    
    # Minor tick
    circle(0.50, -0.10)
    text(0.50, -0.32, "Minor tick label")
    
    # Major tick
    circle(-0.03, 4.00)
    text(0.03, 3.80, "Major tick")
    
    # Minor tick
    circle(0.00, 3.50)
    text(0.00, 3.30, "Minor tick")
    
    # Major tick label
    circle(-0.15, 3.00)
    text(-0.15, 2.80, "Major tick label")
    
    # X Label
    circle(1.80, -0.27)
    text(1.80, -0.45, "X axis label")
    
    # Y Label
    circle(-0.27, 1.80)
    text(-0.27, 1.6, "Y axis label")
    
    # Title
    circle(1.60, 4.13)
    text(1.60, 3.93, "Title")
    
    # Blue plot
    circle(1.75, 2.80)
    text(1.75, 2.60, "Line\n(line plot)")
    
    # Red plot
    circle(1.20, 0.60)
    text(1.20, 0.40, "Line\n(line plot)")
    
    # Scatter plot
    circle(3.20, 1.75)
    text(3.20, 1.55, "Markers\n(scatter plot)")
    
    # Grid
    circle(3.00, 3.00)
    text(3.00, 2.80, "Grid")
    
    # Legend
    circle(3.70, 3.80)
    text(3.70, 3.60, "Legend")
    
    # Axes
    circle(0.5, 0.5)
    text(0.5, 0.3, "Axes")
    
    # Figure
    circle(-0.3, 0.65)
    text(-0.3, 0.45, "Figure")
    
    color = 'blue'
    ax.annotate('Spines', xy=(4.0, 0.35), xytext=(3.3, 0.5),
                weight='bold', color=color,
                arrowprops=dict(arrowstyle='->',
                                connectionstyle="arc3",
                                color=color))
    
    ax.annotate('', xy=(3.15, 0.0), xytext=(3.45, 0.45),
                weight='bold', color=color,
                arrowprops=dict(arrowstyle='->',
                                connectionstyle="arc3",
                                color=color))
    
    ax.text(4.0, -0.4, "Made with http://matplotlib.org",
            fontsize=10, ha="right", color='.5')
    

def page3d(plotter):
    """ Add a 3-D plot page."""
    fig3 = plotter.add('Plot 3d')
    axes3 = Axes3D(fig3)
    X = np.arange(-5, 5, 0.25)
    Y = np.arange(-5, 5, 0.25)
    X, Y = np.meshgrid(X, Y)
    R = np.sqrt(X**2 + Y**2)
    Z = np.sin(R)
    axes3.plot_surface(X, Y, Z, rstride=1, cstride=1, cmap=cm.viridis)

def page2(plotter):
    """ Add the second page."""
    ax = plotter.add('Math Text').gca()
    ax.plot([1, 2, 3], label=r'$\sqrt{x^2}$')
    ax.legend()
    
    ax.set_xlabel(r'$\Delta_i^j$', fontsize=20)
    ax.set_ylabel(r'$\Delta_{i+1}^j$', fontsize=20)
    ax.set_title(r'$\Delta_i^j \hspace{0.4} \mathrm{versus} \hspace{0.4} '
                 r'\Delta_{i+1}^j$', fontsize=20)
    
    tex = r'$\mathcal{R}\prod_{i=\alpha_{i+1}}^\infty a_i\sin(2 \pi f x_i)$'
    ax.text(1, 1.6, tex, fontsize=20, va='bottom')
    

def page1(plotter):
    """ Add the first page."""
    labels = ['G1', 'G2', 'G3', 'G4', 'G5']
    men_means = [20, 35, 30, 35, 27]
    women_means = [25, 32, 34, 20, 25]
    men_std = [2, 3, 4, 1, 2]
    women_std = [3, 5, 2, 3, 3]
    width = 0.35       # the width of the bars: can also be len(x) sequence
    ax = plotter.add('Stacked Bars').gca()
    ax.bar(labels, men_means, width, yerr=men_std, label='Men')
    ax.bar(labels, women_means, width, yerr=women_std, bottom=men_means,
           label='Women')
    
    ax.set_ylabel('Scores')
    ax.set_title('Scores by group and gender')
    ax.legend()    

if __name__ == "__main__":
    demo()
