import numpy as np

Xs, Ys = 12.811, 20.3482  # 12,20.15995#
Xf, Yf = 14.86, 19.9975

Calc_freq = 1.0
board = 11.17

x_bmax, y_bmax, z_bmax = 22.72, 36.3, board
x_bmin, y_bmin, z_bmin = 0.02, 0.02, -board


class ClassEpsilon():
    def EpsilonTest(Coordinates, ray_freq, Engine=True, Norm=True):
        if Norm == True:
            pass
        else:
            x, y, z = Coordinates[0], Coordinates[1], Coordinates[2]
        Rocket_positionX, Rocket_positionY = 14.86, 31.2775
        x, y, z = np.array(x), np.array(y), np.array(z)
        d_from_Rocket = np.abs(x - Rocket_positionX)
        P1x, P1y = 14.86, 31.2775
        P2x, P2y = 13.42, 29.1775
        P3x, P3y = 13, 27.6975
        P4x, P4y = 13, 20.8775
        P5x, P5y = 13.46, 19.9975
        Metal = -1000 * np.ones_like(x)
        k12, b12 = np.linalg.solve(np.array([[P1x, 1], [P2x, 1]]), np.array([P1y, P2y]))
        k23, b23 = np.linalg.solve(np.array([[P2x, 1], [P3x, 1]]), np.array([P2y, P3y]))
        k45, b45 = np.linalg.solve(np.array([[P4x, 1], [P5x, 1]]), np.array([P4y, P5y]))
        arr = P1x - (y - b12) / k12
        arr1 = P2x - (y - b23) / k23 - (P2x - P1x)
        arr2 = P5x - (y - b45) / k45 + (Rocket_positionX - P5x)
        Eps = np.where((d_from_Rocket < arr) & (y > P2y) & (y < P1y), Metal, 1 * np.ones_like(x))
        Eps = np.where((d_from_Rocket < arr1) & (y > P3y) & (y < P2y), Metal, Eps)
        Eps = np.where((d_from_Rocket < (Rocket_positionX - P3x)) & (y > P4y) & (y < P3y), Metal, Eps)
        Eps = np.where((d_from_Rocket < arr2) & (y > P5y) & (y < P4y), Metal, Eps)

        # soplo
        def calc_k_b(z1, z2, x1, x3):
            k = (z2 - z1) / (x3 - x1)
            b = z1 - k * x1
            return k, b

        RocketXLoc = P1x
        RocketZLow = P5y
        RocketZHigh = 2.35
        zSopla = 0.3
        xlSopla1 = 0.824
        xlSopla3 = 0.188
        xlSopla2 = 0.736
        xlSopla4 = 0
        kl, bl = calc_k_b(RocketZLow - zSopla, RocketZLow, RocketXLoc - xlSopla1, RocketXLoc - xlSopla3)
        kr, br = calc_k_b(RocketZLow - zSopla, RocketZLow, RocketXLoc - xlSopla2, RocketXLoc - xlSopla4)
        Eps = np.where(((y <= RocketZLow) & (y >= RocketZLow - zSopla) & (y >= kr * x + br) & (y <= kl * x + bl)),
                       Metal, Eps)
        kl, bl = calc_k_b(RocketZLow - zSopla, RocketZLow, RocketXLoc + xlSopla2, RocketXLoc + xlSopla4)
        kr, br = calc_k_b(RocketZLow - zSopla, RocketZLow, RocketXLoc + xlSopla1, RocketXLoc + xlSopla3)
        Eps = np.where(((y <= RocketZLow) & (y >= RocketZLow - zSopla) & (y <= kr * x + br) & (y >= kl * x + bl)),
                       Metal, Eps)
        if Engine:
            x, z = x - Xf, -y + Yf
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
            Eps_f = 1 - wp_w
            Eps = np.where(Eps == 1, Eps_f, Eps)
        return Eps

    def EpsilonEngineOff(Coordinates, ray_freq, Norm=True):
        if Norm == True:
            pass
        else:
            x, y, z = Coordinates[0], Coordinates[1], Coordinates[2]
        Z_c = 0
        X_c = 0.4
        Y_c = 0
        R = 0.4
        dx = (x - X_c)
        dz = (z - Z_c)
        dy = (y - Y_c)
        dz = 0
        r = np.sqrt(dx ** 2 + 0 + dy ** 2)
        with np.errstate(invalid='ignore'):
            # par = 0.3 # used for magnetic calculations
            par = 1
            return np.ones_like(r)  # np.where(r <= R, par * np.sqrt(2 - (r / R) ** 2) ** 2, par)# np.ones_like(r)

    def Metal(Coordinates, ray_freq, Norm=True):
        if Norm == True:
            pass
        else:
            x, y, z = Coordinates[0], Coordinates[1], Coordinates[2]
        y_gr = 0.01 * 20
        metal = -1
        k = (1 - metal) / y_gr
        eps = np.where(y < y_gr, k * y + metal, 1)
        with np.errstate(invalid='ignore'):
            # par = 0.3 # used for magnetic calculations
            par = 1
            return eps  # np.where(r <= R, par * np.sqrt(2 - (r / R) ** 2) ** 2, par)# np.ones_like(r)

    def Metal2(Coordinates, ray_freq, Norm=True):
        if Norm == True:
            pass
        else:
            x, y, z = Coordinates[0], Coordinates[1], Coordinates[2]
        y_gr = 0.01 * 10
        metal = -1
        k = (1 - metal) / y_gr
        eps = np.where(y < y_gr, k * y + metal, 1)
        with np.errstate(invalid='ignore'):
            # par = 0.3 # used for magnetic calculations
            par = 1
            return eps  # np.where(r <= R, par * np.sqrt(2 - (r / R) ** 2) ** 2, par)# np.ones_like(r)

    def Metal5(Coordinates, ray_freq, Norm=True):
        if Norm == True:
            pass
        else:
            x, y, z = Coordinates[0], Coordinates[1], Coordinates[2]
        y_gr = 0.01 * 5
        metal = -1
        k = (1 - metal) / y_gr
        eps = np.where(y < y_gr, k * y + metal, 1)
        with np.errstate(invalid='ignore'):
            # par = 0.3 # used for magnetic calculations
            par = 1
            return eps  # np.where(r <= R, par * np.sqrt(2 - (r / R) ** 2) ** 2, par)# np.ones_like(r)

    def Metal_w5_e10(Coordinates, ray_freq, Norm=True):
        if Norm == True:
            pass
        else:
            x, y, z = Coordinates[0], Coordinates[1], Coordinates[2]
        y_gr = 0.1  # +3*0.02
        metal = -11.25
        k = (1 - metal) / y_gr
        eps = np.where(y < y_gr, k * y + metal, 1)
        with np.errstate(invalid='ignore'):
            # par = 0.3 # used for magnetic calculations
            par = 1
            return eps  # np.where(r <= R, par * np.sqrt(2 - (r / R) ** 2) ** 2, par)# np.ones_like(r)

    def Metal_w5_e1(Coordinates, ray_freq, Norm=True):
        if Norm == True:
            pass
        else:
            x, y, z = Coordinates[0], Coordinates[1], Coordinates[2]
        y_gr = 0.1  # +3*0.02
        metal = -1
        k = (1 - metal) / y_gr
        eps = np.where(y < y_gr, k * y + metal, 1)
        with np.errstate(invalid='ignore'):
            # par = 0.3 # used for magnetic calculations
            par = 1
            return eps  # np.where(r <= R, par * np.sqrt(2 - (r / R) ** 2) ** 2, par)# np.ones_like(r)

    def Metal_w5_e5(Coordinates, ray_freq, Norm=True):
        if Norm == True:
            pass
        else:
            x, y, z = Coordinates[0], Coordinates[1], Coordinates[2]
        y_gr = 0.1  # +3*0.02
        metal = -5
        k = (1 - metal) / y_gr
        eps = np.where(y < y_gr, k * y + metal, 1)
        with np.errstate(invalid='ignore'):
            # par = 0.3 # used for magnetic calculations
            par = 1
            return eps  # np.where(r <= R, par * np.sqrt(2 - (r / R) ** 2) ** 2, par)# np.ones_like(r)

    def Metal_w5_e50(Coordinates, ray_freq, Norm=True):
        if Norm == True:
            pass
        else:
            x, y, z = Coordinates[0], Coordinates[1], Coordinates[2]
        y_gr = 0.1  # +3*0.02
        metal = -50
        k = (1 - metal) / y_gr
        eps = np.where(y < y_gr, k * y + metal, 1)
        with np.errstate(invalid='ignore'):
            # par = 0.3 # used for magnetic calculations
            par = 1
            return eps  # np.where(r <= R, par * np.sqrt(2 - (r / R) ** 2) ** 2, par)# np.ones_like(r)

    def Circle(Coordinates, ray_freq, Norm=True):
        if Norm == True:
            pass
        else:
            x, y, z = Coordinates[0], Coordinates[1], Coordinates[2]
        Z_c = 0
        X_c = Xs
        Y_c = Ys
        R1, R2 = 1, 2
        dx = (x - X_c)
        dy = (y - Y_c)
        r = np.sqrt(dx ** 2 + dy ** 2)
        Eps1, Eps2 = 1, 2

        with np.errstate(invalid='ignore'):
            eps = np.where(r <= R1, Eps1, (np.where((r <= R2) & (y > Ys), Eps2 * (r + R1) / R2, Eps1)))
        return eps

    def plasma(Coordinates, ray_freq, Norm=True):
        if Norm == True:
            pass
        else:
            x, y, z = Coordinates[0], Coordinates[1], Coordinates[2]
        Z_c = 0
        X_c = Xs
        Y_c = Ys
        R1, R2 = 0.25, 0.5
        dx = (x - X_c)
        dy = (y - Y_c)
        r = np.sqrt(dx ** 2 + dy ** 2)
        Eps1, Eps2 = 0.25, 1

        with np.errstate(invalid='ignore'):
            eps = np.where(x <= R1, Eps2,
                           np.where(x >= 0.5, Eps2, Eps1))
        return eps

    def CircleMinus(Coordinates, ray_freq, Norm=True):
        if Norm == True:
            pass
        else:
            x, y, z = Coordinates[0], Coordinates[1], Coordinates[2]
        Z_c = 0
        X_c = Xs
        Y_c = Ys
        R1, R2 = 1, 2
        dx = (x - X_c)
        dy = (y - Y_c)
        r = np.sqrt(dx ** 2 + dy ** 2)
        Eps1, Eps2 = 1, -2

        with np.errstate(invalid='ignore'):
            eps = np.where(r <= R1, Eps1, (np.where((r <= R2) & (y > Ys), Eps2 * (r + R1) / R2, Eps1)))
        return eps

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

    func_list = [plasma, Circle, Metal, Metal2, Metal5, Metal_w5_e1, Metal_w5_e5, Metal_w5_e10, Metal_w5_e50,
                 CircleMinus, EpsilonTest, EpsilonEngineOff,
                 EpsilonEngineOn]
    calc_list = [plasma]
