#! /usr/bin/env python
# -*- coding: utf-8 -*-
# Exercise 6: Calculate model performance indexes with PyGeoC
from pygeoc.utils import MathClass


def cal_model_performance(obsl, siml):
    """Calculate model performance indexes."""
    nse = MathClass.nashcoef(obsl, siml)
    r2 = MathClass.rsquare(obsl, siml)
    rmse = MathClass.rmse(obsl, siml)
    pbias = MathClass.pbias(obsl, siml)
    rsr = MathClass.rsr(obsl, siml)
    print ('NSE: %.2f, R$^2$: %.2f, PBIAS: %.2f%%, RMSE: %.2f, RSR: %.2f' %
           (nse, r2, pbias, rmse, rsr))


if __name__ == "__main__":
    obs_list = [2.92, 2.75, 2.01, 1.09, 2.87, 1.43, 1.96, 4.00, 2.24, 17.00, 5.88, 0.86, 13.21,
                10.00, 11.00, 6.60]
    sim_list = [0.40, 4.88, 1.92, 0.49, 0.28, 5.36, 1.89, 4.08, 1.50, 10.00, 7.02, 0.33, 8.40,
                7.8, 12, 3.8]
    cal_model_performance(obs_list, sim_list)
