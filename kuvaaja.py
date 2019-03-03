import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
import numpy as np

voltit = []
aika = []
pvoltit = []
paika = []
resistor = []
tmp = []

with open('data/vastus.csv') as vast:
    for line in vast:
        virta, voltti = line.split(',')
        virta, voltti = float(virta), float(voltti)
        resistor.append(voltti / virta)

    sisvastus = sum(resistor)/len(resistor)
    for resist in resistor:
        tmp.append((resist - sisvastus)**2)
    othaj = np.sqrt(sum(tmp) / (len(resistor) - 1))
    vv = othaj / np.sqrt(len(resistor))

with open('data/ac1ko.csv') as data:
    viimevoltti = 0
    purkaus = False
    lisää = True
    for line in data:
        sec, voltti = line.split(',')
        sec, voltti = float(sec), float(voltti)
        aika.append(sec)
        voltit.append(voltti)

        if viimevoltti - voltti > 0.065:
            purkaus = True

        if purkaus:
            if viimevoltti - voltti < 0.0005:
                purkaus = False
                lisää = False
            elif lisää:
                paika.append(sec)
                pvoltit.append(voltti)
        viimevoltti = voltti

pvoltit = np.array(pvoltit)
paika = np.array(paika)


pervastus = 1/1000 + 1/sisvastus
kokv = 1/pervastus
print(kokv)


def func(x, r, c):
    return pvoltit[0] * np.exp(-x / (r*c))


def idealfunc(x, c):
    return pvoltit[0] * np.exp(-x / (kokv*c))


nx = paika - paika[0]
px = nx*1000
ny = []
ay = []
yy = []
o, u = curve_fit(
                func, nx, pvoltit,
                bounds=([kokv-vv, 2e-8], [kokv+vv, 6e-5])
                )
io, iu = curve_fit(idealfunc, nx, pvoltit)
iaah = np.sqrt(np.diag(iu))
iuuh = iaah[0]/np.sqrt(len(pvoltit))
print('ideal: %s' % (io))
print('ideal: %s' % (iuuh))

for x in nx:
    ny.append(func(x, *o))
print(*o)
print(sisvastus)
print(u)
aah = np.sqrt(np.diag(u))
uuh = aah[1]/np.sqrt(len(pvoltit))
print('kapasitorin virhe: %s' % (uuh))
print('vastuksen virhe: %s' % (vv))
# for x in nx:
    # ny.append(func(x, pvoltit[0], 4.75*10**(-7)))

# plt.plot(aika, voltit)
a = plt.plot(px, ny, label='y = Vo*exp(-t/%s*%sE-6)' % (round(o[0], 3), round(o[1]*10**6, 3)))
plt.xlabel('Aika (ms)', fontsize=18)
b = plt.scatter(px, pvoltit, color='orange')
plt.ylabel('Jännite (V)', fontsize=18)

for x in nx:
    ay.append(func(x, kokv, o[1]-uuh))
for x in nx:
    yy.append(func(x, kokv, o[1]+uuh))

c = plt.plot(px, ay, color='red', dashes=[3, 3], label='virheet')
d = plt.plot(px, yy, color='red', dashes=[3, 3])

plt.legend()
plt.show()
