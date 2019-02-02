import numpy as np
import math
import statistics as stat
import pygame as pg
import sys

arr = np.loadtxt('/home/roni/Documents/labrajuttu/mittaus.csv', delimiter=', ')


class solu:

    sähkövektori = None
    sähkösuuruus = None
    nx = None
    ny = None

    def __init__(self, mittaus, x, y):
        self.mittaus = mittaus
        self.x = x
        self.y = y

    def näyttötila(self, leveys, korkeus):

        self.nx = (self.x * leveys / 28)
        self.ny = korkeus - (self.y * korkeus / 20)


def sähkökentät(matrix):
    for rivi in matrix:
        for solu in rivi:
            y = np.where(matrix == solu)[0][0]
            x = np.where(matrix == solu)[1][0]

            if (x > 0 and x < len(rivi) - 1) and (y > 0 and y < len(matrix) - 1):
                dVxl = solu.mittaus - rivi[x - 1].mittaus
                dVxr = solu.mittaus - rivi[x + 1].mittaus
                dxl = rivi[x - 1].x - solu.x
                dxr = rivi[x + 1].x - solu.x
                El = (dVxl / dxl)
                Er = (dVxr / dxr)

                dVyu = solu.mittaus - matrix[y - 1][x].mittaus
                dVyd = solu.mittaus - matrix[y + 1][x].mittaus
                dyu = matrix[y - 1][x].y - solu.y
                dyd = matrix[y + 1][x].y - solu.y
                Eu = (dVyu / dyu)
                Ed = (dVyd / dyd)

                Es1 = math.hypot(El, Eu)
                Es2 = math.hypot(Er, Ed)
                Es3 = math.hypot(El, Ed)
                Es4 = math.hypot(Er, Eu)
                Es = [Es1, Es2, Es3, Es4]
                solu.sähkösuuruus = stat.mean(Es)

                if Es1 != 0 or 0.:
                    Ev1 = [El/Es1, -Eu/Es1]
                else:
                    Ev1 = [0, 0]
                if Es2 != 0 or 0.:
                    Ev2 = [Er/Es2, -Ed/Es2]
                else:
                    Ev2 = [0, 0]
                if Es3 != 0 or 0.:
                    Ev3 = [El/Es3, -Ed/Es3]
                else:
                    Ev3 = [0, 0]
                if Es4 != 0 or 0.:
                    Ev4 = [Er/Es4, -Eu/Es4]
                else:
                    Ev4 = [0, 0]

                sx = [Ev1[0], Ev2[0], Ev3[0], Ev4[0]]
                sxm = stat.mean(sx)
                sy = [Ev1[1], Ev2[1], Ev3[1], Ev4[1]]
                sym = stat.mean(sy)
                solu.sähkövektori = [sxm, sym]

                # ang1 = math.degrees(np.arccos(np.clip(np.dot(Ev1, [1, 0]), -1.0, 1.0)))
                # ang2 = math.degrees(np.arccos(np.clip(np.dot(Ev2, [1, 0]), -1.0, 1.0)))
                # ang3 = math.degrees(np.arccos(np.clip(np.dot(Ev3, [1, 0]), -1.0, 1.0)))
                # ang4 = math.degrees(np.arccos(np.clip(np.dot(Ev4, [1, 0]), -1.0, 1.0)))


def paikannus(matrix):

    solulista = []
    j = 20
    for rivi in matrix:
        solurivi = []
        i = 0
        for tulos in rivi:
            ob = solu(tulos, i, j)
            solurivi.append(ob)
            i += 2
        solulista.append(solurivi)
        j -= 2
    return np.array(solulista)


def tihennys(matrix):

    uusimatriisi1 = []
    uusimatriisi2 = []

    for rivi in matrix:

        uusimatriisi1.append([])

        for sol in rivi:

            y = np.where(matrix == sol)[0][0]
            x = np.where(matrix == sol)[1][0]

            uusimatriisi1[y].append(sol)

            if x < len(rivi) - 1:
                mittausx = (sol.mittaus + matrix[y][x+1].mittaus) / 2
                uusix = (sol.x + matrix[y][x+1].x) / 2

                ob1 = solu(mittausx, uusix, sol.y)
                uusimatriisi1[y].append(ob1)

    uusimatriisi1 = np.array(uusimatriisi1)

    for rivi in uusimatriisi1:

        uusimatriisi2.append(rivi.tolist())
        uusimatriisi2.append([])

        for sol2 in rivi:

            y = np.where(uusimatriisi1 == sol2)[0][0]
            x = np.where(uusimatriisi1 == sol2)[1][0]

            if y < len(uusimatriisi1) - 1:

                mittausy = (sol2.mittaus + uusimatriisi1[y+1][x].mittaus) / 2
                uusiy = (sol2.y + uusimatriisi1[y+1][x].y) / 2
                ob2 = solu(mittausy, sol2.x, uusiy)
                uusimatriisi2[len(uusimatriisi2)-1].append(ob2)

    uusimatriisi2.pop()
    return np.array(uusimatriisi2)


def tasapotentiaali(matrix, volt):

    volat = []

    for rivi in matrix:
        volarivi = []
        for sol in rivi:
            if abs(sol.mittaus - volt) < 0.05:
                volarivi.append(sol)
        if volarivi != []:
            volat.append(volarivi)

    return volat


def piirrätasapotentiaalit(screen, *args):

    for arg in args:

        pisteet = []

        for rivi in arg:

            rivipisteet = []

            for sol in rivi:
                rivipisteet.append(sol.nx)
                uy = sol.ny

            ux = stat.mean(rivipisteet)
            pisteet.append([ux, uy])

        pg.draw.lines(screen, musta, False, pisteet, 2)


def piirräkoordinaatisto(screen, väri, leveys, korkeus):
    i = 28
    j = 20
    for y in range(j):
        ny = korkeus - (y * korkeus / 20)
        if y % 2 == 0:
            pg.draw.line(screen, väri, [0, ny], [leveys, ny])
        for x in range(i):
            nx = (x * leveys / 28)
            if x % 2 == 0:
                pg.draw.line(screen, väri, [nx, 0], [nx, korkeus])


solulista = paikannus(arr)
solulista = tihennys(solulista)
solulista = tihennys(solulista)
solulista = tihennys(solulista)
solulista = tihennys(solulista)
sähkökentät(solulista)
volat2 = tasapotentiaali(solulista, 2)
volat3 = tasapotentiaali(solulista, 3)
volat4 = tasapotentiaali(solulista, 4)
volat5 = tasapotentiaali(solulista, 5)
volat6 = tasapotentiaali(solulista, 6)
volat7 = tasapotentiaali(solulista, 7)
volat8 = tasapotentiaali(solulista, 8)

musta = (0, 0, 0)
valk = (255, 255, 255)

leveys = 1000
korkeus = 600
koko = [leveys, korkeus]

for rivi in solulista:
    for sol in rivi:
        sol.näyttötila(leveys, korkeus)

pg.init()
screen = pg.display.set_mode(koko)
pg.display.set_caption('Sähkökentät')

voltit = False
valmis = False
p = 0

while not valmis:

    for event in pg.event.get():
        if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
            valmis = True
        if event.type == pg.KEYDOWN and event.key == pg.K_p:
            pg.image.save(screen, 'sähkö'+str(p)+'.jpg')
            p += 1
        if event.type == pg.KEYDOWN and event.key == pg.K_v:
            if voltit:
                voltit = False
            else:
                voltit = True

    screen.fill(valk)

    if voltit:
        piirrätasapotentiaalit(screen, volat2, volat3, volat4, volat5, volat6, volat7, volat8)
    else:
        for rivi in solulista:
            for sol in rivi:
                if sol.sähkövektori:
                    # import pdb; pdb.set_trace()
                    alku = [int(sol.nx), int(sol.ny)]
                    loppu = [int((alku[0] + 15*sol.sähkövektori[0])),
                             int((alku[1] + 15*sol.sähkövektori[1]))]
                    if sol.mittaus <= 1:
                        väri = [0, 0, 255]
                    elif 1 < sol.mittaus <= 2:
                        väri = [28, 0, 226]
                    elif 2 < sol.mittaus <= 3:
                        väri = [56, 0, 198]
                    elif 3 < sol.mittaus <= 4:
                        väri = [85, 0, 170]
                    elif 4 < sol.mittaus <= 5:
                        väri = [113, 0, 141]
                    elif 5 < sol.mittaus <= 6:
                        väri = [141, 0, 113]
                    elif 6 < sol.mittaus <= 7:
                        väri = [170, 0, 85]
                    elif 7 < sol.mittaus <= 8:
                        väri = [198, 0, 56]
                    elif 8 < sol.mittaus <= 9:
                        väri = [226, 0, 28]
                    elif 9 < sol.mittaus <= 10:
                        väri = [255, 0, 0]

                    # pg.draw.aaline(screen, musta, alku, loppu, 2)
                    pg.draw.circle(screen, väri, alku, 4)

    piirräkoordinaatisto(screen, musta, leveys, korkeus)
    nollax = int((4 * leveys / 28))
    nollay = int(korkeus - (10 * korkeus / 20))
    pg.draw.circle(screen, musta, (nollax, nollay), 7)
    pg.draw.circle(screen, (0, 0, 255), (nollax, nollay), 6)
    kymppix = int((24 * leveys / 28))
    kymppiy = int(korkeus - (10 * korkeus / 20))
    pg.draw.circle(screen, musta, (kymppix, kymppiy), 7)
    pg.draw.circle(screen, (255, 0, 0), (kymppix, kymppiy), 6)

    pg.display.flip()

sys.exit(0)
