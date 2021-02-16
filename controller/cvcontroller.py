import threading
import time
import math
import cv2
import face_recognition
import numpy as np
from kivy.graphics.texture import Texture
from keras.models import load_model

from model.posicionbrazos import PosicionBrazos
from model.rostro import Rostro
from customlibs.segmentsdistance import distanciaentrelineas

class CamaraController(object):
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            with threading.Lock():
                if cls._instance is None:
                    print('Creating the object')
                    cls._instance = super(CamaraController, cls).__new__(cls)
                    cls._instance.net = cv2.dnn.readNetFromTensorflow("assets/graph_opt.pb")
                    cls._instance.facemodel = load_model("./assets/model_v6_23.hdf5")
                    cls._instance.inWidth = 250
                    cls._instance.inHeight = 250
                    cls._instance.thr = 0.2
                    cls._instance.BODY_PARTS = {"Nose": 0, "Neck": 1, "RShoulder": 2, "RElbow": 3, "RWrist": 4,
                                                "LShoulder": 5, "LElbow": 6, "LWrist": 7, "RHip": 8, "RKnee": 9,
                                                "RAnkle": 10, "LHip": 11, "LKnee": 12, "LAnkle": 13, "REye": 14,
                                                "LEye": 15, "REar": 16, "LEar": 17, "Background": 18}

                    cls._instance.POSE_PAIRS = [["Neck", "RShoulder"], ["Neck", "LShoulder"], ["RShoulder", "RElbow"],
                                                ["RElbow", "RWrist"], ["LShoulder", "LElbow"], ["LElbow", "LWrist"],
                                                ["Neck", "RHip"], ["RHip", "RKnee"], ["RKnee", "RAnkle"],
                                                ["Neck", "LHip"],
                                                ["LHip", "LKnee"], ["LKnee", "LAnkle"], ["Neck", "Nose"],
                                                ["Nose", "REye"],
                                                ["REye", "REar"], ["Nose", "LEye"], ["LEye", "LEar"]]
                    cls._instance.gesture = Rostro.NOAPLICA
                    cls._instance.pose = PosicionBrazos.NOAPLICA
                    cls._instance.cap = cv2.VideoCapture(2)
                    if not cls._instance.cap.isOpened():
                        cls._instance.cap = cv2.VideoCapture(0)
                    if not cls._instance.cap.isOpened():
                        raise IOError("No se puede acceder a la webcam")
                    cls._instance.cap.set(cv2.CAP_PROP_FPS, 60)
        return cls._instance

    def captureposeimage(self) -> Texture:
        if hasattr(self, 'last_texture'):
            return self.last_texture
        else:
            return False

    def capturegesture(self):
        if hasattr(self, 'gesture'):
            return self.gesture
        else:
            return False

    def capturepose(self):
        if hasattr(self, 'pose'):
            return self.pose
        else:
            return False


def updategesture():
    camaracontroller = CamaraController()
    emotion_dict = {0: Rostro.IRRITADO, 5: Rostro.PREOCUPADO, 4: Rostro.SERIO, 1: Rostro.IRRITADO, 6: Rostro.SONRIENDO, 2: Rostro.PREOCUPADO, 3: Rostro.SONRIENDO}
    while (True):
        hasFrame, frame = camaracontroller.cap.read()
        if not hasFrame:
            return
        face_locations = face_recognition.face_locations(frame)
        if len(face_locations) > 0:
            top, right, bottom, left = face_locations[0]
            face_image = frame[top:bottom, left:right]
            face_image = cv2.resize(face_image, (48, 48))
            face_image = cv2.cvtColor(face_image, cv2.COLOR_BGR2GRAY)
            face_image = np.reshape(face_image, [1, face_image.shape[0], face_image.shape[1], 1])
            prediction = camaracontroller.facemodel.predict(face_image)
            predicted_class = np.argmax(prediction)
            label_map = dict((v, k) for v, k in emotion_dict.items())
            predicted_label = label_map[predicted_class]
            camaracontroller.gesture = predicted_label
            print(predicted_label)
        time.sleep(5)


def updateimage():
    camaracontroller = CamaraController()
    ti = time.time()
    while (True):
        hasFrame, frame = camaracontroller.cap.read()
        if not hasFrame:
            return
        frameWidth = frame.shape[1]
        frameHeight = frame.shape[0]
        camaracontroller.net.setInput(
            cv2.dnn.blobFromImage(frame, 1.0, (camaracontroller.inWidth, camaracontroller.inHeight),
                                  (127.5, 127.5, 127.5), swapRB=True, crop=False))
        out = camaracontroller.net.forward()
        out = out[:, :19, :, :]  # MobileNet output [1, 57, -1, -1], we only need the first 19 elements

        assert (len(camaracontroller.BODY_PARTS) == out.shape[1])

        points = []
        for i in range(len(camaracontroller.BODY_PARTS)):
            # Slice heatmap of corresponging body's part.
            heatMap = out[0, i, :, :]

            # Originally, we try to find all the local maximums. To simplify a sample
            # we just find a global one. However only a single pose at the same time
            # could be detected this way.
            _, conf, _, point = cv2.minMaxLoc(heatMap)
            x = (frameWidth * point[0]) / out.shape[3]
            y = (frameHeight * point[1]) / out.shape[2]
            # Add a point if it's confidence is higher than threshold.
            points.append((int(x), int(y)) if conf > camaracontroller.thr else None)

        #Aquí va el código para determinar la posición del cuerpo
        munecaderecha = points[camaracontroller.BODY_PARTS['RWrist']]
        munecaizquierda = points[camaracontroller.BODY_PARTS['LWrist']]
        cododerecho = points[camaracontroller.BODY_PARTS['RElbow']]
        codoizquierdo = points[camaracontroller.BODY_PARTS['LElbow']]
        hombroderecho = points[camaracontroller.BODY_PARTS['RShoulder']]
        cuello = points[camaracontroller.BODY_PARTS['Neck']]
        if ((munecaderecha is None) or (munecaizquierda is None) or
            (cododerecho is None) or (codoizquierdo is None) or
            (hombroderecho is None) or (cuello is None)):
                if (time.time() - ti) > 15:
                    camaracontroller.pose = PosicionBrazos.TRASLAESPALDA
                    ti = time.time()
        else:
            distanciabrazos = distanciaentrelineas(munecaderecha, cododerecho, munecaizquierda, codoizquierdo)
            distanciahombrocuello = math.sqrt((cuello[0]-hombroderecho[0])**2+(cuello[1]-hombroderecho[1])**2)
            ratio = (distanciabrazos / distanciahombrocuello)
            if ratio > 3.5:
                camaracontroller.pose = PosicionBrazos.EXTENDIDOS
                ti = time.time()
            elif ratio < 2:
                camaracontroller.pose = PosicionBrazos.CRUZADOS
                ti = time.time()
            else:
                camaracontroller.pose = PosicionBrazos.NEUTRALES
                ti = time.time()
            print("Distancia entre brazos:")
            print(distanciabrazos)
            print("Distancia hombro cuello:")
            print(distanciahombrocuello)
        #Aquí comienza el código para dibujar los puntos y lineas en la imàgen
        for pair in camaracontroller.POSE_PAIRS:
            partFrom = pair[0]
            partTo = pair[1]
            assert (partFrom in camaracontroller.BODY_PARTS)
            assert (partTo in camaracontroller.BODY_PARTS)

            idFrom = camaracontroller.BODY_PARTS[partFrom]
            idTo = camaracontroller.BODY_PARTS[partTo]

            if points[idFrom] and points[idTo]:
                cv2.line(frame, points[idFrom], points[idTo], (0, 255, 0), 3)
                cv2.ellipse(frame, points[idFrom], (3, 3), 0, 0, 360, (0, 0, 255), cv2.FILLED)
                cv2.ellipse(frame, points[idTo], (3, 3), 0, 0, 360, (0, 0, 255), cv2.FILLED)

        t, _ = camaracontroller.net.getPerfProfile()
        freq = cv2.getTickFrequency() / 1000
        cv2.putText(frame, '%.2fms' % (t / freq), (10, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0))
        buf1 = cv2.flip(frame, 0)
        buf = buf1.tostring()
        camaracontroller.last_texture = buf
