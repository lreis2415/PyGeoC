# -*- coding: utf-8 -*-
"""
Created on Thu Mar 15 10:09:13 2018

@author: Florian Ulrich Jehn
https://github.com/florianjehn/Flow-Duration-Curve/blob/master/flow_duration_curve.py
"""
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np


def flow_duration_curve(x, comparison=None, axis=0, ax=None, plot=True,
                        log=True, percentiles=(5, 95),
                        fdc_kwargs=None, fdc_range_kwargs=None,
                        fdc_comparison_kwargs=None):
    """
    Calculates and plots a flow duration curve from x.

    All observations/simulations are ordered and the empirical probability is
    calculated. This is then plotted as a flow duration curve.

    When x has more than one dimension along axis, a range flow duration curve
    is plotted. This means that for every probability a min and max flow is
    determined. This is then plotted as a fill between.

    Additionally a comparison can be given to the function, which is plotted in
    the same ax.

    :param x: numpy array or pandas dataframe, discharge of measurements or
    simulations
    :param comparison: numpy array or pandas dataframe of discharge that should
    also be plotted in the same ax
    :param axis: int, axis along which x is iterated through
    :param ax: matplotlib subplot object, if not None, will plot in that
    instance
    :param plot: bool, if False function will not show the plot, but simply
    return the ax object
    :param log: bool, if True plot on loglog axis
    :param percentiles: tuple of int, percentiles that should be used for
    drawing a range flow duration curve
    :param fdc_kwargs: dict, matplotlib keywords for the normal fdc
    :param fdc_range_kwargs: dict, matplotlib keywords for the range fdc
    :param fdc_comparison_kwargs: dict, matplotlib keywords for the comparison
    fdc

    return: subplot object with the flow duration curve in it
    """
    # Convert x to an pandas dataframe, for easier handling
    if not isinstance(x, pd.DataFrame):
        x = pd.DataFrame(x)

    # Get the dataframe in the right dimensions, if it is not in the expected
    if axis != 0:
        x = x.transpose()

    # Convert comparison to a dataframe as well
    if comparison is not None and not isinstance(comparison, pd.DataFrame):
        comparison = pd.DataFrame(comparison)
        # And transpose it is neccesary
        if axis != 0:
            comparison = comparison.transpose()

    # Create an ax is neccesary
    if ax is None:
        fig, ax = plt.subplots(1, 1)

    # Make the y scale logarithmic if needed
    if log:
        ax.set_yscale("log")

    # Determine if it is a range flow curve or a normal one by checking the
    # dimensions of the dataframe
    # If it is one, make a single fdc
    if x.shape[1] == 1:
        plot_single_flow_duration_curve(ax, x[0], fdc_kwargs)

        # Make a range flow duration curve
    else:
        plot_range_flow_duration_curve(ax, x, percentiles, fdc_range_kwargs)

    # Add a comparison to the plot if is present
    if comparison is not None:
        ax = plot_single_flow_duration_curve(ax, comparison[0],
                                             fdc_comparison_kwargs)

        # show if requested
    if plot:
        plt.show()

    return ax


def plot_single_flow_duration_curve(ax, timeseries, kwargs):
    """
    Plots a single fdc into an ax.

    :param ax: matplotlib subplot object
    :param timeseries: list like iterable
    :param kwargs: dict, keyword arguments for matplotlib

    return: subplot object with a flow duration curve drawn into it
    """
    # Get the probability
    exceedence = np.arange(1., len(timeseries) + 1) / len(timeseries)
    exceedence *= 100
    # Plot the curve, check for empty kwargs
    if kwargs is not None:
        ax.plot(exceedence, sorted(timeseries, reverse=True), **kwargs)
    else:
        ax.plot(exceedence, sorted(timeseries, reverse=True))
    return ax


def plot_range_flow_duration_curve(ax, x, percentiles, kwargs):
    """
    Plots a single range fdc into an ax.

    :param ax: matplotlib subplot object
    :param x: dataframe of several timeseries
    :param kwargs: dict, keyword arguments for matplotlib

    return: subplot object with a range flow duration curve drawn into it
    """
    # Get the probabilites
    exceedence = np.arange(1., len(np.array(x)) + 1) / len(np.array(x))
    exceedence *= 100

    # Sort the data
    sort = np.sort(x, axis=0)[::-1]

    # Get the percentiles
    low_percentile = np.percentile(sort, percentiles[0], axis=1)
    high_percentile = np.percentile(sort, percentiles[1], axis=1)

    # Plot it, check for empty kwargs
    if kwargs is not None:
        ax.fill_between(exceedence, low_percentile, high_percentile, **kwargs)
    else:
        ax.fill_between(exceedence, low_percentile, high_percentile)
    return ax


if __name__ == "__main__":
    # Create test data
    np_array_one_dim = np.random.rayleigh(5, [1, 300])
    np_array_75_dim = np.c_[np.random.rayleigh(11, [25, 300]),
    np.random.rayleigh(10, [25, 300]),
    np.random.rayleigh(8, [25, 300])]
    df_one_dim = pd.DataFrame(np.random.rayleigh(9, [1, 300]))
    df_75_dim = pd.DataFrame(np.c_[np.random.rayleigh(8, [25, 300]),
    np.random.rayleigh(15, [25, 300]),
    np.random.rayleigh(3, [25, 300])])
    df_75_dim_transposed = pd.DataFrame(np_array_75_dim.transpose())

    # Call the function with all different arguments
    fig, subplots = plt.subplots(nrows=2, ncols=3)
    ax1 = flow_duration_curve(np_array_one_dim, ax=subplots[0, 0], plot=False,
                              axis=1, fdc_kwargs={"linewidth": 0.5})
    ax1.set_title("np array one dim\nwith kwargs")

    ax2 = flow_duration_curve(np_array_75_dim, ax=subplots[0, 1], plot=False,
                              axis=1, log=False, percentiles=(0, 100))
    ax2.set_title("np array 75 dim\nchanged percentiles\nnolog")

    ax3 = flow_duration_curve(df_one_dim, ax=subplots[0, 2], plot=False, axis=1,
                              log=False, fdc_kwargs={"linewidth": 0.5})
    ax3.set_title("\ndf one dim\nno log\nwith kwargs")

    ax4 = flow_duration_curve(df_75_dim, ax=subplots[1, 0], plot=False, axis=1,
                              log=False)
    ax4.set_title("df 75 dim\nno log")

    ax5 = flow_duration_curve(df_75_dim_transposed, ax=subplots[1, 1],
                              plot=False)
    ax5.set_title("df 75 dim transposed")

    ax6 = flow_duration_curve(df_75_dim, ax=subplots[1, 2], plot=False,
                              comparison=np_array_one_dim, axis=1,
                              fdc_comparison_kwargs={"color": "black",
                                                     "label": "comparison",
                                                     "linewidth": 0.5},
                              fdc_range_kwargs={"label": "range_fdc"})
    ax6.set_title("df 75 dim\n with comparison\nwith kwargs")
    ax6.legend()

    # Show the beauty
    fig.tight_layout()
    plt.show()