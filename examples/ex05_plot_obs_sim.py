#! /usr/bin/env python
# -*- coding: utf-8 -*-
# Exercise 5: Calculate and plot model performance indexes with PyGeoC
import os

import matplotlib

from pygeoc.utils import MathClass

if os.name != 'nt':  # Force matplotlib to not use any Xwindows backend.
    matplotlib.use('Agg')
import matplotlib.pyplot as plt


def cal_model_performance(obsl, siml):
    nse = MathClass.nashcoef(obsl, siml)
    r2 = MathClass.rsquare(obsl, siml)
    rmse = MathClass.rmse(obsl, siml)
    pbias = MathClass.pbias(obsl, siml)
    rsr = MathClass.rsr(obsl, siml)
    plt.rcParams['xtick.direction'] = 'out'
    plt.rcParams['ytick.direction'] = 'out'
    plt.rcParams['font.family'] = 'Times New Roman'
    fig, ax = plt.subplots(figsize=(4, 4))
    plt.scatter(obsl, siml, marker='.', s=50, color='black')
    plt.xlabel('Observation', fontsize=20)
    plt.ylabel('Simulation', fontsize=20)
    plt.title('\nNSE: %.2f, R$^2$: %.2f, PBIAS: %.2f%%\nRMSE: %.2f, RSR: %.2f' %
              (nse, r2, pbias, rmse, rsr), color='red', loc='right')
    minv = min(min(obsl), min(siml))
    maxv = max(max(obsl), max(siml))
    ax.set_xlim(left=minv, right=maxv)
    ax.set_ylim(bottom=minv, top=maxv)
    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    obs_list = [2.92, 2.75, 2.01, 1.09, 2.87, 1.43, 1.96, 4.00, 2.24, 17.00, 5.88, 0.86, 13.21,
                10.00, 11.00, 6.60]
    sim_list = [0.40, 4.88, 1.92, 0.49, 0.28, 5.36, 1.89, 4.08, 1.50, 10.00, 7.02, 0.33, 8.40,
                7.8, 12, 3.8]
    cal_model_performance(obs_list, sim_list)
