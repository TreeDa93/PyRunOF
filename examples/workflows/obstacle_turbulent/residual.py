import matplotlib
matplotlib.use('TkAgg')

import matplotlib.pyplot as plt
import pandas as pd
import pathlib as pl
import time
import sys



def dynamic_plot(data_path, *name_cols, name_figure = 'Figure 1', time_delay=0.5):
    fig, ax = plt.subplots(num=name_figure)
    ax.grid()
    ax.set_yscale('log')

    while not data_path.exists():
        time.sleep(time_delay)

    if len(name_cols) == 0:
        data = pd.read_csv(path, sep='\s+', escapechar='#', skiprows=1)
        time_key = data.keys()[0]
        ax.set_xlabel(time_key)
        ax.set_ylabel('Residual')
        plot_list = {}
        for var in data.keys()[1:]:
            plot_list[var],  = ax.plot(data[time_key], data[var], label=var)

    while plt.fignum_exists(name_figure):
        if len(name_cols) == 0:
            data = pd.read_csv(path, sep='\s+', escapechar='#', skiprows=1)
            for var in data.keys()[1:]:
                plot_list[var].set_ydata(data[var])
                plot_list[var].set_xdata(data[time_key])
        #  rescale
        ax.relim()
        ax.autoscale_view()
        #  fig.canvas.draw()
        fig.canvas.flush_events()
        ax.legend()
        plt.draw()
        plt.pause(time_delay)


if __name__ == "__main__":
    name = sys.argv[1]
    path = pl.Path.cwd() / name / 'postProcessing/residuals/0/residuals.dat'
    dynamic_plot(path, name_figure=name)