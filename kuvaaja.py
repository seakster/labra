from scipy.optimize import curve_fit
import statistics as stat
import math
import sys
import numpy as np
import matplotlib.pyplot as plt

ajat = []
virrat = []
jännitteet = []
taajuudet = []
for arg in sys.argv:
    if arg == "kuvaaja.py":
        continue
    else:
        if arg == "50hz.csv":
            taajuudet.append(50)
        else:
            taajuudet.append(float(arg[0:3]))
        aika = []
        virta = []
        jännite = []
        with open(arg, 'r') as kuv:
            for line in kuv:
                a = line.split(',')
                aika.append(float(a[0]))
                jännite.append(float(a[1]))
                virta.append(float(a[2]))
        ajat.append(aika)
        virrat.append(virta)
        jännitteet.append(jännite)


def calcw(data):
    lastval = 0
    lastlastval = 0
    peaks = []
    rec = False
    for val in data:
        if val < lastval:
            if rec:
                peaks.append(lastval)
                rec = False
            else:
                continue
        else:
            rec = True
        lastval = val
    return np.mean(peaks), stat.stdev(peaks)


amp = []
for virt in virrat:
    aa, yerr = calcw(virt)
    amp.append(1e3*aa)
knopeus = []
for taajuus in taajuudet:
    knopeus.append(2*math.pi*taajuus)


def teoria(x, l):
    return (1e3*((2*math.pi*x)*4.1) / np.sqrt((l * (2*math.pi*x)**2 - 1/6.8e-6)**2 + (220**2 * (2*math.pi*x)**2)))


yerr += 0.0005
yerr *= 1e3
popt, pcov = curve_fit(teoria, taajuudet, amp)
print(popt)
print(np.sqrt(pcov))
x = np.linspace(taajuudet[0], taajuudet[-1])
plt.errorbar(taajuudet, amp, yerr=yerr, fmt='o', label='Mittaukset')
plt.plot(x, teoria(x, 0.0972 ), label='Teoreettinen')
plt.xlabel('Taajuus (Hz)', fontsize=16)
plt.ylabel('Virran amplitudi (mA)', fontsize=16)
plt.legend()

plt.show()
