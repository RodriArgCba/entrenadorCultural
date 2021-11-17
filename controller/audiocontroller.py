import threading
import pyaudio
import numpy as np
import matplotlib.pyplot as plt
import speech_recognition as sr
import logging
import time
import audioop


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
                    cls._instance.duracionacumulada = 0
                    cls._instance.killthread = True
        return cls._instance

    def resetearcuenta(self):
        self.nrocaptura = 0
        self.acumulado = 0
        self.duracionacumulada = 0


def contarpalabras():
    contador = ContadorDePalabras()
    with contador.microphone as source:
        while not contador.killthread:
            ti = time.time()
            audio = contador.recognizer.listen(source)
            duracion = time.time() - ti
            try:
                texto = contador.recognizer.recognize_google(audio, language='es')
                contador.nrocaptura = contador.nrocaptura + 1
                contador.acumulado = contador.acumulado + len(texto.split(" "))
                contador.duracionacumulada = contador.duracionacumulada + duracion
                logging.info(texto)
                logging.info("tiempo: " + str(duracion))
                logging.info(len(texto.split(" ")) / duracion)
                logging.info("Volumen: " + str(AudioController._instance.volumenpromedio))
                from controller.controladorprincipal import ControladorPrincipal
                ControladorPrincipal().printtochatbox(texto)

            except sr.UnknownValueError:
                print("No pasa nada")


class AudioController(object):
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            with threading.Lock():
                if cls._instance is None:
                    print('Creating the object')
                    cls._instance = super(AudioController, cls).__new__(cls)
                    cls._instance.reset = False
                    cls._instance.volumenacumulado = 0.0
                    cls._instance.volumenpromedio = 0.0
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
                    cls._instance.killthread = True
        return cls._instance


def updatesound():
    audiocontroller = AudioController()
    i = 0
    while not audiocontroller.killthread:
        if audiocontroller.reset:
            i = 0
            audiocontroller.volumenacumulado = 0.0
            audiocontroller.volumenpromedio = 0.0
            audiocontroller.reset = False
        rawdata = audiocontroller.stream.read(audiocontroller.CHUNK)
        volumen = 10 * np.log10(pow(audioop.rms(rawdata, 2), 2) / pow(20, 2))
        if volumen > 20:
            i = i + 1
            audiocontroller.volumenacumulado = audiocontroller.volumenacumulado + volumen
            audiocontroller.volumenpromedio = audiocontroller.volumenacumulado / i
        data = np.fromstring(rawdata, dtype=np.int16)
        audiocontroller.line.set_ydata(data)
