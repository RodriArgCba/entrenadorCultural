import threading
import cv2
from kivy.graphics.texture import Texture


class CamaraController(object):
    
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            with threading.Lock():
                if cls._instance is None:
                    print('Creating the object')
                    cls._instance = super(CamaraController, cls).__new__(cls)
                    cls._instance.net = cv2.dnn.readNetFromTensorflow("graph_opt.pb")
                    cls._instance.inWidth = 200
                    cls._instance.inHeight = 200
                    cls._instance.thr = 0.2
                    cls._instance.BODY_PARTS = {"Nose": 0, "Neck": 1, "RShoulder": 2, "RElbow": 3, "RWrist": 4,
                                  "LShoulder": 5, "LElbow": 6, "LWrist": 7, "RHip": 8, "RKnee": 9,
                                  "RAnkle": 10, "LHip": 11, "LKnee": 12, "LAnkle": 13, "REye": 14,
                                  "LEye": 15, "REar": 16, "LEar": 17, "Background": 18}

                    cls._instance.POSE_PAIRS = [["Neck", "RShoulder"], ["Neck", "LShoulder"], ["RShoulder", "RElbow"],
                                  ["RElbow", "RWrist"], ["LShoulder", "LElbow"], ["LElbow", "LWrist"],
                                  ["Neck", "RHip"], ["RHip", "RKnee"], ["RKnee", "RAnkle"], ["Neck", "LHip"],
                                  ["LHip", "LKnee"], ["LKnee", "LAnkle"], ["Neck", "Nose"], ["Nose", "REye"],
                                  ["REye", "REar"], ["Nose", "LEye"], ["LEye", "LEar"]]
                    cls._instance.cap = cv2.VideoCapture(2)
                    if not cls._instance.cap.isOpened():
                        cls._instance.cap = cv2.VideoCapture(0)
                    if not cls._instance.cap.isOpened():
                        raise IOError("No se puede acceder a la webcam")
                    cls._instance.cap.set(cv2.CAP_PROP_FPS, 60)
        return cls._instance

    def capturepose(self) -> Texture:
        if hasattr(self,'last_texture'):
            return self.last_texture
        else:
            return False



def updateimage():
    camaracontroller = CamaraController()
    j=0
    while (True):
        j=j+1
        hasFrame, frame = camaracontroller.cap.read()
        if not hasFrame:
            return
        frameWidth = frame.shape[1]
        frameHeight = frame.shape[0]
        camaracontroller.net.setInput(
            cv2.dnn.blobFromImage(frame, 1.0, (camaracontroller.inWidth, camaracontroller.inHeight), (127.5, 127.5, 127.5), swapRB=True, crop=False))
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

        t, _ =camaracontroller.net.getPerfProfile()
        freq = cv2.getTickFrequency() / 1000
        cv2.putText(frame, '%.2fms' % (t / freq), (10, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0))
        buf1 = cv2.flip(frame, 0)
        buf = buf1.tostring()
        camaracontroller.last_texture = buf