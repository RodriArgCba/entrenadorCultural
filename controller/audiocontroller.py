import threading
import pyaudio
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import speech_recognition as sr
import logging
import time


class ContadorDePalabras(object):
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            with threading.Lock():
                if cls._instance is None:
                    print('Creating the object')
                    cls._instance = super(ContadorDePalabras, cls).__new__(cls)
                    cls._instance.recognizer = sr.Recognizer()
                    cls._instance.microphone = sr.Microphone()
                    cls._instance.nrocaptura = 0
                    cls._instance.acumulado = 0
        return cls._instance

    def resetearcuenta(self):
        self.nrocaptura = 0
        self.acumulado = 0


def contarpalabras():
    contador = ContadorDePalabras()
    with contador.microphone as source:
        while(True):
            ti = time.time()
            audio = contador.recognizer.listen(source)
            duracion = time.time() - ti
            try:
                texto = contador.recognizer.recognize_google(audio, language='es')
                contador.nrocaptura = contador.nrocaptura + 1
                contador.acumulado = contador.acumulado + (len(texto.split(" "))/duracion)
                logging.info(texto)
                logging.info(len(texto.split(" "))/duracion)
            except:
                print("No pasa nada")


class AudioController(object):
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            with threading.Lock():
                if cls._instance is None:
                    print('Creating the object')
                    cls._instance = super(AudioController, cls).__new__(cls)
                    cls._instance.RATE = 44100
                    cls._instance.CHUNK = int(cls._instance.RATE / 20)  # RATE / number of updates per second
                    p = pyaudio.PyAudio()
                    cls._instance.stream = p.open(
                        format=pyaudio.paInt16,
                        channels=1,
                        rate=cls._instance.RATE,
                        input=True,
                        frames_per_buffer=cls._instance.CHUNK
                    )
                    data = np.fromstring(cls._instance.stream.read(cls._instance.CHUNK), dtype=np.int16)
                    cls._instance.lenght = [0, len(data), -2 ** 16 / 2, 2 ** 16 / 2]
                    cls._instance.fig, cls._instance.ax = plt.subplots()  # fig : figure object, ax : Axes object
                    cls._instance.line = cls._instance.ax.plot(data)[0]
                    cls._instance.ax.grid()
                    cls._instance.ax.axis(cls._instance.lenght)
                    cls._instance.ax.set_yticklabels([])
                    cls._instance.ax.set_xticklabels([])
        return cls._instance


def updatesound():
    audiocontroller = AudioController()
    while (True):
        data = np.fromstring(audiocontroller.stream.read(audiocontroller.CHUNK), dtype=np.int16)
        audiocontroller.line.set_ydata(data)
        #time.wait(0.05)
