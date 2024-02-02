from matplotlib import rcParams, cycler
import matplotlib.pyplot as plt
from matplotlib.ticker import AutoMinorLocator

class Plotter():
    def __init__(self):
        rcParams['text.usetex'] = True
        rcParams['font.family'] = 'sans-serif'
        rcParams['font.sans-serif'] = ['Arial']
        rcParams['font.size'] = 26
        rcParams['legend.fontsize'] = 24
        rcParams['axes.linewidth'] = 1.1
        rcParams['axes.labelpad'] = 10.0
        rcParams['legend.frameon'] = False
        plot_color_cycle = cycler('color', ['000000', '0000FE', 'FE0000', '008001', 'FD8000', '8c564b', 
                                            'e377c2', '7f7f7f', 'bcbd22', '17becf'])
        rcParams['errorbar.capsize'] = 5
        rcParams['axes.prop_cycle'] = plot_color_cycle
        rcParams['axes.xmargin'] = 0
        rcParams['axes.ymargin'] = 0
        rcParams.update({"figure.figsize" : (10,8),
                        "figure.subplot.left" : 0.177, "figure.subplot.right" : 0.946,
                        "figure.subplot.bottom" : 0.156, "figure.subplot.top" : 0.965,
                        "axes.autolimit_mode" : "round_numbers",
                        "xtick.major.size"     : 7,
                        "xtick.minor.size"     : 3.5,
                        "xtick.major.width"    : 1.1,
                        "xtick.minor.width"    : 1.1,
                        "xtick.major.pad"      : 5,
                        "xtick.minor.visible"  : True,
                        "xtick.direction"      : 'in',
                        "xtick.top"          : True,
                        "ytick.major.size"     : 7,
                        "ytick.minor.size"     : 3.5,
                        "ytick.major.width"    : 1.1,
                        "ytick.minor.width"    : 1.1,
                        "ytick.major.pad"      : 5,
                        "ytick.minor.visible"  : True,
                        "ytick.direction"      : 'in',
                        "ytick.right"          : True,
                        "lines.markersize"     : 10,
                        "lines.markerfacecolor" : "none",
                        "lines.markeredgewidth" : 0.8})