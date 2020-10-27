import numpy as np
import random as rd
import matplotlib.pyplot as plt

def Sensors(N):
    """randomizes coordinates of N sensors evenly spread out on the surface of Earth"""
    sensors = []
    for i in range(N):
        if sensors == []:
            theta = rd.uniform(0.0, 2.0*np.pi) # losujemy kat theta, promien r domyslnie
            # ustawiony na 1 (Ziemia ma stala wielkosc, wiec dlugosc okregu jest niezmienna)
        else:
            theta = theta + (2.0*np.pi)/N # sensory maja byc rownomiernie rozlozone
            # na powierzchni Ziemi (czyli na okregu)
        x = np.cos(theta) # cos(theta) = x / r  --> x = cos(theta)*r
        y = np.sin(theta) # sin(theta) = x / r  --> y = sin(theta)*r
        sensors.append([x, y])
    return sensors

def SquaredEuclideanDistance(A, B):
    """calculates dᵢ² (squared euclidean distance) between points A and B"""
    return (A[0]-B[0])**2 + (A[1]-B[1])**2

def ExplosionPoint():
    """randomizes coordinates of an explosion point e which needs to be within
    a circle of a radius with value 1"""
    ex, ey = 1, 1 # punkt (1,1) jest poza okregiem
    e_distance = np.sqrt(2) # odleglosc od punktu (0, 0) wynosi √2
    while e_distance > 1:
        ex = rd.uniform(-1.0, 1.0)
        ey = rd.uniform(-1.0, 1.0)
        e_distance = np.sqrt(SquaredEuclideanDistance([ex, ey], [0, 0])) # obliczamy odleglosc od punktu (0, 0)
    return [ex, ey]

def BlastSignals(sensors, e):
    """calculates blast signals for each sensor i, ..., N"""
    d2 = [SquaredEuclideanDistance(sensor, e) for sensor in sensors]
    blast_signals = [1 / (dist_sqr + 0.1) for dist_sqr in d2]
    return blast_signals

def Noises(blast_signals, sigma):
    """stochastically perturbs blast signals with a noise with a standard deviation σ"""
    noises = [signal + rd.gauss(0, sigma) for signal in blast_signals]
    return noises

if __name__ == '__main__':
    plt.figure(figsize = (7,7))
    sensors = Sensors(10)
    e = ExplosionPoint()
    for i in range(len(sensors)):
        plt.plot(sensors[i][0], sensors[i][1], 'ko')
    plt.plot(e[0], e[1], 'rd')
    sigma = 0.2
    print("blast signals")
    blast_signals = BlastSignals(sensors, e)
    print(blast_signals)
    print("\n\nnoises")
    print(Noises(blast_signals, sigma))
    plt.show()