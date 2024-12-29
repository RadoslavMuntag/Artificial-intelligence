import matplotlib.pyplot as plt
import numpy as np

# Vykreslenie dát do grafu, Nepotrebné pre hlavný program

y1, x1 = np.loadtxt('data_K-NN_only.txt', unpack=True)
y2, x2 = np.loadtxt("data_whole.txt", unpack=True)

plt.plot(x1, y1, label='Čas behu po klasifikáci bodov')
plt.plot(x2, y2, label="Čas behu celého programu")
plt.xlabel("POINTS_TO_GENERATE")
plt.ylabel("čas v sekundách")
plt.title("Analýza zložitosti")
plt.legend()
plt.show()