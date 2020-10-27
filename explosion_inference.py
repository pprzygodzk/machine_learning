import explosion_preparing_the_data as dt
import numpy as np
import matplotlib.pyplot as plt

"""Generating data"""
N = 25
sensors = dt.Sensors(N)
e = dt.ExplosionPoint()
sigma = 0.25
observations = dt.Noises(dt.BlastSignals(sensors, e), sigma)

delta = 0.01
states = np.arange(-1, 1.001, delta)
# wartosci współrzędnych punktu e mieszcza sie w zakresie od -1 do 1, jest to rozklad
# ciagly; dzieki funkcji arange generujemy rownomiernie rozlozone wartosci stanow
# w tym przedziale, rozniace sie co krok rowny delta, rozklad z ciaglego
# staje sie dyskretny (dyskretyzacja)

"""Preparing the grid for coordinates of explosion
   & calculating the likelihood of each point of a grid"""
probabilities = np.zeros((len(states), len(states))) # tworzymy macierz prawdopodobienstw
# o rozmiarze liczby mozliwych stanow (w niej bedzie znajdowac sie prawdopodobienstwo,
# czy punkt o wspolrzednych x, y jest miejscem eksplozji)
sigma2 = sigma*sigma
const1 = 1/(2*sigma2)
const2 = np.sqrt(1/(2*sigma2*np.pi))
for i1, state1 in enumerate(states): # wspolrzedna (stan) dla x
    for i2, state2 in enumerate(states): # wspolrzedna (stan) dla y
        p = 1
        e_distance = dt.SquaredEuclideanDistance([state1, state2], [0, 0])
        if e_distance <= 1: # jezeli potencjalny punkt eksplozji znajduje sie wewnatrz lub na okregu
            d2 = [dt.SquaredEuclideanDistance(sensors[i], [state1, state2]) for i in range(N)]
            # wyliczamy odleglosci sensorow od potencjalnego punktu eksplozji
            signals = [1/(d2[i]+0.1) for i in range(N)]
            # wyliczamy potencjalne wartosci sygnalow odbieranych przez sensory
            p_v = [np.exp((-1/const1)*(observations[i]-signals[i])**2)*const2 for i in range(N)]
            # prawdopodobienstwo sygnalu v[i] pod warunkiem d[i] dla kazdego sensoru (rozklad gaussowski)
            for i in range(N):
                p = p*p_v[i] # prawdopodobienstwo, ze dany punkt jest miejscem eksplozji
        else:
            p = 0 # niemozliwe, zeby punkt eksplozji znajdowal sie poza okregiem
        probabilities[i1, i2] = p
        
"""Finding the coordinates of maximum"""
arg_max = np.argmax(probabilities) # zwraca indeks jednocyfrowy dla najwyzszej wartosci
# prawdopodobienstwa z macierzy prawdopodobienstw (najbardziej prawdopodobny punkt
# jako miejsce eksplozji)
indices = np.unravel_index(arg_max, probabilities.shape) # konwertuje indeks jednocyfrowy
# do krotki skladajacej sie z indeksu rzedu i kolumny
estimated_e_x = states[indices[0]] # znajduje wspolrzedne punktu eksplozji
estimated_e_y = states[indices[1]] # uzyskanego droga inferencji

"""Visualizing the experiment"""
X, Y = np.meshgrid(states, states) # tworzy dwuwymiarowa siatke (grid),
# dwuwymiarowa macierz wspolrzednych (musi byc tego samego rozmiaru co probabilities)
plt.figure(figsize=(7,6))
plt.contour(Y, X, probabilities, levels = 20) # rysuje kontury po wartosciach prawdopodobienstw
# w macierzy probabilities (najwyzszych wokol estymowanego punktu eksplozji)
# parametr levels determinuje liczbe tych konturow wokol punktu
plt.colorbar()
sensors = np.array(sensors)
plt.plot(sensors[:, 0], sensors[:, 1], "ro", label = "sensory") # o to kropka
plt.plot(estimated_e_x, estimated_e_y, "md", label = "z inferencji: ({:.4f}, {:.4f})".format(estimated_e_x, estimated_e_y))
plt.plot(e[0], e[1], "kd", label = "eksplozja: ({:.4f}, {:.4f})".format(e[0], e[1]))
# d to punkt typu diament
plt.xlabel('x') # opisy osi x i y
plt.ylabel('y')
plt.legend(loc = 7, bbox_to_anchor = (1.5, 1.1))
# bbox_to_anchor sprawia, ze legenda wychodzi poza wykres
plt.show()