#!/usr/bin/env python
from pylab import *

def spectrogram(data, Fs, colormap=cm.Accent, show_plot=True, ylim=50):
    Pxx, freqs, bins, im = specgram(data, NFFT=256, Fs=Fs, noverlap=Fs-1,
                                    cmap=cm.jet)

    plt.ylim(0, ylim)
    plt.xlim(0, len(data)/Fs)

    if show_plot:
        show()


# available color maps
# http://matplotlib.org/examples/color/colormaps_reference.html
color_maps = [
    cm.Accent, cm.Oranges_r, cm.RdBu_r, cm.YlGnBu_r, cm.cool, cm.gist_stern, cm.pink,
    cm.Accent_r, cm.PRGn, cm.RdGy, cm.YlGn_r, cm.cool_r, cm.gist_stern_r, cm.pink_r,
    cm.Blues, cm.PRGn_r, cm.RdGy_r, cm.YlOrBr, cm.coolwarm, cm.gist_yarg, cm.prism,
    cm.Blues_r, cm.Paired, cm.RdPu, cm.YlOrBr_r, cm.coolwarm_r, cm.gist_yarg_r, cm.prism_r,
    cm.BrBG, cm.Paired_r, cm.RdPu_r, cm.YlOrRd, cm.copper, cm.gnuplot, cm.rainbow,
    cm.BrBG_r, cm.Pastel1, cm.RdYlBu, cm.YlOrRd_r, cm.copper_r, cm.gnuplot2, cm.rainbow_r,
    cm.BuGn, cm.Pastel1_r, cm.RdYlBu_r, cm.afmhot, cm.cubehelix, cm.gnuplot2_r, cm.register_cmap,
    cm.BuGn_r, cm.Pastel2, cm.RdYlGn, cm.afmhot_r, cm.cubehelix_r, cm.gnuplot_r, cm.revcmap,
    cm.BuPu, cm.Pastel2_r, cm.RdYlGn_r, cm.autumn, cm.datad, cm.gray, cm.seismic,
    cm.BuPu_r, cm.PiYG, cm.Reds, cm.autumn_r, cm.flag, cm.gray_r, cm.seismic_r,
    cm.Dark2, cm.PiYG_r, cm.Reds_r, cm.binary, cm.flag_r, cm.hot, cm.spec,
    cm.Dark2_r, cm.PuBu, cm.ScalarMappable, cm.binary_r, cm.get_cmap, cm.hot_r, cm.spec_reversed,
    cm.GnBu, cm.PuBuGn, cm.Set1, cm.bone, cm.gist_earth, cm.hsv, cm.spectral,
    cm.GnBu_r, cm.PuBuGn_r, cm.Set1_r, cm.bone_r, cm.gist_earth_r, cm.hsv_r, cm.spectral_r,
    cm.Greens, cm.PuBu_r, cm.Set2, cm.brg, cm.gist_gray, cm.jet, cm.spring,
    cm.Greens_r, cm.PuOr, cm.Set2_r, cm.brg_r, cm.gist_gray_r, cm.jet_r, cm.spring_r,
    cm.Greys, cm.PuOr_r, cm.Set3, cm.bwr, cm.gist_heat, cm.ma, cm.summer,
    cm.Greys_r, cm.PuRd, cm.Set3_r, cm.bwr_r, cm.gist_heat_r, cm.mpl, cm.summer_r,
    cm.LUTSIZE, cm.PuRd_r, cm.Spectral, cm.cbook, cm.gist_ncar, cm.np, cm.terrain,
    cm.OrRd, cm.Purples, cm.Spectral_r, cm.cmap_d, cm.gist_ncar_r, cm.ocean, cm.terrain_r,
    cm.OrRd_r, cm.Purples_r, cm.YlGn, cm.cmapname, cm.gist_rainbow, cm.ocean_r, cm.winter,
    cm.Oranges, cm.RdBu, cm.YlGnBu, cm.colors, cm.gist_rainbow_r, cm.os, cm.winter_r
    ]
