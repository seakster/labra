import matplotlib.pyplot as plt
import math
import numpy as np
import sys

aika = []
jännite = []
virta = []
with open(sys.argv[1], 'r') as data:
            for line in data:
                a = line.split(',')
                aika.append(1e3*float(a[0]))
                jännite.append(float(a[1]))
                virta.append(float(a[2]))
 
plt.figure(1)
plt.subplot(211)
plt.plot(aika[2000:2100], jännite[2000:2100], 'r')
plt.xlabel('Aika (ms)', fontsize=16)
plt.ylabel('Jännite (V)', fontsize=16)
plt.subplot(212)
plt.plot(aika[2000:2100], virta[2000:2100])
plt.xlabel('Aika (ms)', fontsize=16)
plt.ylabel('Virta (A)', fontsize=16)
plt.show()
