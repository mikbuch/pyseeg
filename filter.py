#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np

prev_x = np.zeros((8, 5))
prev_y = np.zeros((8, 5))
prev_x2 = np.zeros((8, 5))
prev_y2 = np.zeros((8, 5))

flt_type = 6


def filterIIR(data, nrk):
    # b = 0.0
    # a = 0.0
    # b2 = 0.0
    # a2 = 0.0

    j = 5 - 1
    while j > 0:
        prev_x[nrk, j] = prev_x[nrk, j - 1]
        prev_y[nrk, j] = prev_y[nrk, j - 1]
        prev_x2[nrk, j] = prev_x2[nrk, j - 1]
        prev_y2[nrk, j] = prev_y2[nrk, j - 1]
        j -= 1

    prev_x[nrk, 0] = data

    if (flt_type == 1):  # 1-50Hz
        b = np.array(
            0.2001387256580675,
            0,
            -0.4002774513161350,
            0,
            0.2001387256580675
            )
        a = np.array(
            1,
            -2.355934631131582,
            1.941257088655214,
            -0.7847063755334187,
            0.1999076052968340
            )

    elif (flt_type == 2):  # 7-13Hz
        b = np.array(
            0.005129268366104263,
            0,
            -0.01025853673220853,
            0,
            0.005129268366104263)
        a = np.array(
            1, -3.678895469764040,
            5.179700413522124,
            -3.305801890016702,
            0.8079495914209149
            )

    elif (flt_type == 3):  # 15-50Hz
        b = np.array(
            0.1173510367246093,
            0,
            -0.2347020734492186,
            0,
            0.1173510367246093
            )
        a = np.array(
            1,
            -2.137430180172061,
            2.038578008108517,
            -1.070144399200925,
            0.2946365275879138
            )

    elif (flt_type == 4):  # 5-50Hz
        b = np.array(
            0.1750876436721012,
            0,
            -0.3501752873442023,
            0,
            0.1750876436721012
            )
        a = np.array(
            1,
            -2.299055356038497,
            1.967497759984450,
            -0.8748055564494800,
            0.2196539839136946
            )

    elif (flt_type == 5):  # none
        b = np.array(1, 1, 1, 1, 1)
        a = np.array(1, 1, 1, 1, 1)

    elif (flt_type == 6):  # 50 Hz
        b2 = np.array(
            0.96508099,
            -1.19328255,
            2.29902305,
            -1.19328255,
            0.96508099
            )
        a2 = np.array(
            1,
            -1.21449347931898,
            2.29780334191380,
            -1.17207162934772,
            0.931381682126902
            )

    elif (flt_type == 7):  # 60 Hz
        b2 = np.array(
            0.9650809863447347,
            -0.2424683201757643,
            1.945391494128786,
            -0.2424683201757643,
            0.9650809863447347
            )
        a2 = np.array(
            1,
            -0.2467782611297853,
            1.944171784691352,
            -0.2381583792217435,
            0.9313816821269039
            )

    elif (flt_type == 8):  # none
        b2 = np.array(1, 1, 1, 1, 1)
        a2 = np.array(1, 1, 1, 1, 1)

    filtered = filter_data(b2, a2, b, a, nrk)
    return filtered


def filter_data(b2, a2, b, a, nrk):
    wynik = 0.0
    for j in range(5):
        wynik += b2[j] * prev_x[nrk, j]
        if j > 0:
            wynik -= a2[j] * prev_y[nrk, j]
    prev_y[nrk, 0] = wynik
    prev_x2[nrk, 0] = wynik
    wynik = 0.0
    for j in range(5):
        wynik += b[j] * prev_x2[nrk, j]
        if j > 0:
            wynik -= a[j] * prev_y2[nrk, j]
    prev_y2[nrk, 0] = wynik
    return wynik

x = -581.32344338
filterIIR(x, 0)
