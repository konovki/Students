import numpy as np
import pandas as pd
import os.path
import arxive.calc_lib as c_l
from multiprocessing import Pool
import datetime
import arxive.Properties as Prop
import matplotlib.pyplot as plt
import math as m

path0 = ''
for item in os.getcwd().split(Prop.splitter)[:-1]:
    path0 += item + '/'

Xs, Ys = 0, 0
Xf, Yf = 0, 0
# drowing
Calc_freq = 1
board = 1
x_bmax, y_bmax, z_bmax = 7.79, 16.43, board
x_bmin, y_bmin, z_bmin = -14.93, -20, -board


class ClassEpsilon():

    def LunebergLenzADD(Coordinates, ray_freq, Norm=True):
        if Norm == True:
            pass
        else:
            x, y, z = Coordinates[0], Coordinates[1], Coordinates[2]
        LensXcoordinate, LensYcoordinate = 1.01, 0
        Eps = np.ones_like(y) * 1
        r = np.sqrt((x - LensXcoordinate) ** 2 + (y - LensYcoordinate) ** 2)
        R = 0.5  # Luneberg Lenz Radius
        Eps_Luneberg = np.where(r <= R, 2 - (r / R) ** 2, Eps)
        LensXcoordinate, LensYcoordinate = 3.5, 0
        R = 0.5  # Luneberg Lenz Radius
        r = np.sqrt((x - LensXcoordinate) ** 2 + (y - LensYcoordinate) ** 2)
        Eps_Luneberg = np.where(r <= R, -(2 - (r / R) ** 2), Eps_Luneberg)
        return Eps_Luneberg

    def EpsilonEngineOn(Coordinates, ray_freq, Norm=True):  # Norm = True get norm values need to be trans in usual
        if Norm == True:
            pass
        else:
            x_c, y_c, z_c = Coordinates[0], Coordinates[1], Coordinates[2]
        x, z = x_c - Xf, -y_c + Yf
        koeff = 22.1119  # last 2.21119 * (10 ** 19). included factor (10^9)^2 from freq
        r_source = -0.938854
        x2_y2 = x ** 2
        teta = np.degrees(np.where(z > 0, np.arctan2(np.sqrt(x2_y2), z), 0))
        f_teta = np.where((teta >= 0) & (teta <= 85), 2,
                          np.where((teta > 85) & (teta < 90), -0.1 * teta + 10.5, 1))
        n_teta = np.where((teta >= 0) & (teta <= 20), -0.7 * teta + 32,
                          np.where((teta > 20) & (teta <= 40), 0.2 * teta + 14,
                                   np.where((teta > 40) & (teta <= 60), 0.5 * teta + 2,
                                            np.where((teta > 60) & (teta <= 90), 0.23 * teta + 46, 1))))
        p = np.where(z <= 0, 0,
                     ((np.cos(np.radians(teta / f_teta)) ** n_teta) / ((np.sqrt(x2_y2 + z ** 2) + r_source) ** 2)))
        wp = koeff * p
        wp_w = wp / (ray_freq ** 2)
        exp = 1 - wp_w
        return exp

    def EpsilonEngineOnXminus(Coordinates, ray_freq,
                              Norm=True):  # Norm = True get norm values need to be trans in usual
        if Norm == True:
            pass
        else:
            x_c, y_c, z_c = Coordinates[0], Coordinates[1], Coordinates[2]
        x, z = x_c - Xf - 0.1, -y_c + Yf
        koeff = 22.1119  # last 2.21119 * (10 ** 19). included factor (10^9)^2 from freq
        r_source = -0.938854
        x2_y2 = x ** 2
        teta = np.degrees(np.where(z > 0, np.arctan2(np.sqrt(x2_y2), z), 0))
        f_teta = np.where((teta >= 0) & (teta <= 85), 2,
                          np.where((teta > 85) & (teta < 90), -0.1 * teta + 10.5, 1))
        n_teta = np.where((teta >= 0) & (teta <= 20), -0.7 * teta + 32,
                          np.where((teta > 20) & (teta <= 40), 0.2 * teta + 14,
                                   np.where((teta > 40) & (teta <= 60), 0.5 * teta + 2,
                                            np.where((teta > 60) & (teta <= 90), 0.23 * teta + 46, 1))))
        p = np.where(z <= 0, 0,
                     ((np.cos(np.radians(teta / f_teta)) ** n_teta) / ((np.sqrt(x2_y2 + z ** 2) + r_source) ** 2)))
        wp = koeff * p
        wp_w = wp / (ray_freq ** 2)
        exp = 1 - wp_w
        return exp

    def EpsilonONES(Coordinates, ray_freq, Norm=True):  # Norm = True get norm values need to be trans in usual
        if Norm == True:
            pass
        else:
            x_c, y_c, z_c = Coordinates[0], Coordinates[1], Coordinates[2]

        return np.ones_like(x_c)

    def EpsilonEngineOnYminus(Coordinates, ray_freq,
                              Norm=True):  # Norm = True get norm values need to be trans in usual
        if Norm == True:
            pass
        else:
            x_c, y_c, z_c = Coordinates[0], Coordinates[1], Coordinates[2]
        x, z = x_c - Xf, -y_c + Yf - 0.1
        koeff = 22.1119  # last 2.21119 * (10 ** 19). included factor (10^9)^2 from freq
        r_source = -0.938854
        x2_y2 = x ** 2
        teta = np.degrees(np.where(z > 0, np.arctan2(np.sqrt(x2_y2), z), 0))
        f_teta = np.where((teta >= 0) & (teta <= 85), 2,
                          np.where((teta > 85) & (teta < 90), -0.1 * teta + 10.5, 1))
        n_teta = np.where((teta >= 0) & (teta <= 20), -0.7 * teta + 32,
                          np.where((teta > 20) & (teta <= 40), 0.2 * teta + 14,
                                   np.where((teta > 40) & (teta <= 60), 0.5 * teta + 2,
                                            np.where((teta > 60) & (teta <= 90), 0.23 * teta + 46, 1))))
        p = np.where(z <= 0, 0,
                     ((np.cos(np.radians(teta / f_teta)) ** n_teta) / ((np.sqrt(x2_y2 + z ** 2) + r_source) ** 2)))
        wp = koeff * p
        wp_w = wp / (ray_freq ** 2)
        exp = 1 - wp_w
        return exp

    def EpsilonEngineOnYplus(Coordinates, ray_freq, Norm=True):  # Norm = True get norm values need to be trans in usual
        if Norm == True:
            pass
        else:
            x_c, y_c, z_c = Coordinates[0], Coordinates[1], Coordinates[2]
        x, z = x_c - Xf, -y_c + Yf + 0.1
        koeff = 22.1119  # last 2.21119 * (10 ** 19). included factor (10^9)^2 from freq
        r_source = -0.938854
        x2_y2 = x ** 2
        teta = np.degrees(np.where(z > 0, np.arctan2(np.sqrt(x2_y2), z), 0))
        f_teta = np.where((teta >= 0) & (teta <= 85), 2,
                          np.where((teta > 85) & (teta < 90), -0.1 * teta + 10.5, 1))
        n_teta = np.where((teta >= 0) & (teta <= 20), -0.7 * teta + 32,
                          np.where((teta > 20) & (teta <= 40), 0.2 * teta + 14,
                                   np.where((teta > 40) & (teta <= 60), 0.5 * teta + 2,
                                            np.where((teta > 60) & (teta <= 90), 0.23 * teta + 46, 1))))
        p = np.where(z <= 0, 0,
                     ((np.cos(np.radians(teta / f_teta)) ** n_teta) / ((np.sqrt(x2_y2 + z ** 2) + r_source) ** 2)))
        wp = koeff * p
        wp_w = wp / (ray_freq ** 2)
        exp = 1 - wp_w
        return exp

    def EpsilonEngineOnXplus(Coordinates, ray_freq, Norm=True):  # Norm = True get norm values need to be trans in usual
        if Norm == True:
            pass
        else:
            x_c, y_c, z_c = Coordinates[0], Coordinates[1], Coordinates[2]
        x, z = x_c - Xf + 0.1, -y_c + Yf
        koeff = 22.1119  # last 2.21119 * (10 ** 19). included factor (10^9)^2 from freq
        r_source = -0.938854
        x2_y2 = x ** 2
        teta = np.degrees(np.where(z > 0, np.arctan2(np.sqrt(x2_y2), z), 0))
        f_teta = np.where((teta >= 0) & (teta <= 85), 2,
                          np.where((teta > 85) & (teta < 90), -0.1 * teta + 10.5, 1))
        n_teta = np.where((teta >= 0) & (teta <= 20), -0.7 * teta + 32,
                          np.where((teta > 20) & (teta <= 40), 0.2 * teta + 14,
                                   np.where((teta > 40) & (teta <= 60), 0.5 * teta + 2,
                                            np.where((teta > 60) & (teta <= 90), 0.23 * teta + 46, 1))))
        p = np.where(z <= 0, 0,
                     ((np.cos(np.radians(teta / f_teta)) ** n_teta) / ((np.sqrt(x2_y2 + z ** 2) + r_source) ** 2)))
        wp = koeff * p
        wp_w = wp / (ray_freq ** 2)
        exp = 1 - wp_w
        return exp

    def EpsilonEngineOn0_1(Coordinates, ray_freq, Norm=True):  # Norm = True get norm values need to be trans in usual
        if Norm == True:
            pass
        else:
            x_c, y_c, z_c = Coordinates[0], Coordinates[1], Coordinates[2]
        x, z = x_c - Xf, -y_c + Yf
        koeff = 22.1119  # last 2.21119 * (10 ** 19). included factor (10^9)^2 from freq
        r_source = -0.938854
        x2_y2 = x ** 2
        teta = np.degrees(np.where(z > 0, np.arctan2(np.sqrt(x2_y2), z), 0))
        f_teta = np.where((teta >= 0) & (teta <= 85), 2,
                          np.where((teta > 85) & (teta < 90), -0.1 * teta + 10.5, 1))
        n_teta = np.where((teta >= 0) & (teta <= 20), -0.7 * teta + 32,
                          np.where((teta > 20) & (teta <= 40), 0.2 * teta + 14,
                                   np.where((teta > 40) & (teta <= 60), 0.5 * teta + 2,
                                            np.where((teta > 60) & (teta <= 90), 0.23 * teta + 46, 1))))
        p = np.where(z <= 0, 0,
                     ((np.cos(np.radians(teta / f_teta)) ** n_teta) / ((np.sqrt(x2_y2 + z ** 2) + r_source) ** 2)))
        wp = koeff * p
        wp_w = wp / (ray_freq ** 2)
        exp = 1 - wp_w
        return exp

    def LunebergLenz400(Coordinates, ray_freq, Norm=True):
        if Norm == True:
            pass
        else:
            x, y, z = Coordinates[0], Coordinates[1], Coordinates[2]
        R = 0.4  # Luneberg Lenz Radius
        LensXcoordinate, LensYcoordinate = -(40 + 100) / 1000 - R, 0.6005  # 0.54, 0.6005
        Eps = np.ones_like(y) * 1
        r = np.sqrt((x - LensXcoordinate) ** 2 + (y - LensYcoordinate) ** 2)
        Eps_Luneberg = np.where(r <= R, 2 - (r / R) ** 2, Eps)
        # LensXcoordinate,LensYcoordinate = 3.5,0
        # R = 1.5 #Luneberg Lenz Radius
        # r = np.sqrt((x-LensXcoordinate)**2+(y-LensYcoordinate)**2)
        # Eps_Luneberg = np.where(r <= R,-(2 - (r / R) ** 2),Eps_Luneberg)
        return Eps_Luneberg

    def LunebergLenz300Old(Coordinates, ray_freq, Norm=True):
        if Norm == True:
            pass
        else:
            x, y, z = Coordinates[0], Coordinates[1], Coordinates[2]
        R = 0.3  # Luneberg Lenz Radius
        LensXcoordinate, LensYcoordinate = -(40 + 100) / 1000 - R, 0.6005  # 0.54, 0.6005
        Eps = np.ones_like(y) * 1
        r = np.sqrt((x - LensXcoordinate) ** 2 + (y - LensYcoordinate) ** 2)
        Eps_Luneberg = np.where(r <= R, 2 - (r / R) ** 2, Eps)
        # LensXcoordinate,LensYcoordinate = 3.5,0
        # R = 1.5 #Luneberg Lenz Radius
        # r = np.sqrt((x-LensXcoordinate)**2+(y-LensYcoordinate)**2)
        # Eps_Luneberg = np.where(r <= R,-(2 - (r / R) ** 2),Eps_Luneberg)
        return Eps_Luneberg

    def LunebergLenz300(Coordinates, ray_freq, Norm=True):
        if Norm == True:
            pass
        else:
            x, y, z = Coordinates[0], Coordinates[1], Coordinates[2]
        R = 0.3  # Luneberg Lenz Radius
        LensXcoordinate, LensYcoordinate = -R, 0.1485  # 0.54, 0.6005
        Eps = np.ones_like(y) * 1
        r = np.sqrt((x - LensXcoordinate) ** 2 + (y - LensYcoordinate) ** 2)
        Eps_Luneberg = np.where(r <= R, np.sqrt(2 - (r / R) ** 2), Eps)
        # LensXcoordinate,LensYcoordinate = 3.5,0
        # R = 1.5 #Luneberg Lenz Radius
        # r = np.sqrt((x-LensXcoordinate)**2+(y-LensYcoordinate)**2)
        # Eps_Luneberg = np.where(r <= R,-(2 - (r / R) ** 2),Eps_Luneberg)
        return Eps_Luneberg

    def LunebergLenz500(Coordinates, ray_freq, Norm=True):
        if Norm == True:
            pass
        else:
            x, y, z = Coordinates[0], Coordinates[1], Coordinates[2]
        R = 0.5  # Luneberg Lenz Radius
        LensXcoordinate, LensYcoordinate = -(40 + 100) / 1000 - R, 0.6005  # 0.54, 0.6005
        Eps = np.ones_like(y) * 1
        r = np.sqrt((x - LensXcoordinate) ** 2 + (y - LensYcoordinate) ** 2)
        Eps_Luneberg = np.where(r <= R, 2 - (r / R) ** 2, Eps)
        # LensXcoordinate,LensYcoordinate = 3.5,0
        # R = 1.5 #Luneberg Lenz Radius
        # r = np.sqrt((x-LensXcoordinate)**2+(y-LensYcoordinate)**2)
        # Eps_Luneberg = np.where(r <= R,-(2 - (r / R) ** 2),Eps_Luneberg)
        return Eps_Luneberg


    def EPS2(Coordinates, ray_freq, Norm=True):
        if Norm == True:
            pass
        else:
            x, y, z = Coordinates[0], Coordinates[1], Coordinates[2]
        LensXcoordinate, LensYcoordinate = -0.4, 0.6005  # 0.54, 0.6005
        Eps = np.ones_like(y) * 1
        r = np.sqrt((x - LensXcoordinate) ** 2 + (y - LensYcoordinate) ** 2)
        R = 0.4  # Luneberg Lenz Radius
        Eps_Luneberg = np.where(r <= R, 2, 1)
        # LensXcoordinate,LensYcoordinate = 3.5,0
        # R = 1.5 #Luneberg Lenz Radius
        # r = np.sqrt((x-LensXcoordinate)**2+(y-LensYcoordinate)**2)
        # Eps_Luneberg = np.where(r <= R,-(2 - (r / R) ** 2),Eps_Luneberg)
        return Eps_Luneberg

    def EPSsqrt2(Coordinates, ray_freq, Norm=True):
        if Norm == True:
            pass
        else:
            x, y, z = Coordinates[0], Coordinates[1], Coordinates[2]
        LensXcoordinate, LensYcoordinate = -0.4, 0.6005  # 0.54, 0.6005
        Eps = np.ones_like(y) * 1
        r = np.sqrt((x - LensXcoordinate) ** 2 + (y - LensYcoordinate) ** 2)
        R = 0.4  # Luneberg Lenz Radius
        Eps_Luneberg = np.where(r <= R, m.sqrt(2), 1)
        # LensXcoordinate,LensYcoordinate = 3.5,0
        # R = 1.5 #Luneberg Lenz Radius
        # r = np.sqrt((x-LensXcoordinate)**2+(y-LensYcoordinate)**2)
        # Eps_Luneberg = np.where(r <= R,-(2 - (r / R) ** 2),Eps_Luneberg)
        return Eps_Luneberg



    func_list = [EpsilonONES, EpsilonEngineOn, EpsilonEngineOnXminus, EpsilonEngineOnXplus, EpsilonEngineOnYminus,
                 EpsilonEngineOnYplus]
