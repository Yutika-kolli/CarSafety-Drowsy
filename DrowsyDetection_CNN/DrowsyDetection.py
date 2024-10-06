import cv2
from keras.models import load_model
import numpy as np
from pygame import mixer
import time
import sys
import os
import dlib
import glob
import cv2

def drowsy_detection():
    try:
        mixer.init()
        sound = mixer.Sound('alarm.wav')

        face = cv2.CascadeClassifier('haar cascade files\haarcascade_frontalface_alt.xml')
        leye = cv2.CascadeClassifier('haar cascade files\haarcascade_lefteye_2splits.xml')
        reye = cv2.CascadeClassifier('haar cascade files\haarcascade_righteye_2splits.xml')
        model2 = load_model('../DrowsyDetection_CNN/models/cnn_yawning.h5')
        predictor_path = "shape_predictor_68_face_landmarks.dat"
        detector = dlib.get_frontal_face_detector()
        predictor = dlib.shape_predictor(predictor_path)

        model = load_model('models/cnn_eyes.h5')
        path = os.getcwd()
        cap = cv2.VideoCapture(0)
        font = cv2.FONT_HERSHEY_COMPLEX_SMALL
        count = 0
        score = 0
        score2 = 0
        thicc = 2
        rpred = [99]
        lpred = [99]

        while (True):
            ret, frame = cap.read()
            img = frame
            height, width = frame.shape[:2]

            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            faces = face.detectMultiScale(gray, minNeighbors=5, scaleFactor=1.1, minSize=(25, 25))
            left_eye = leye.detectMultiScale(gray)
            right_eye = reye.detectMultiScale(gray)

            # cv2.rectangle(frame, (0,height-50) , (500,height) , (0,0,0) , thickness=cv2.FILLED )

            for (x, y, w, h) in faces:
                cv2.rectangle(frame, (x, y), (x + w, y + h), (100, 100, 100), 1)

            for (x, y, w, h) in right_eye:
                r_eye = frame[y:y + h, x:x + w]
                count = count + 1
                r_eye = cv2.cvtColor(r_eye, cv2.COLOR_BGR2GRAY)
                r_eye = cv2.resize(r_eye, (24, 24))
                r_eye = r_eye / 255
                r_eye = r_eye.reshape(24, 24, -1)
                r_eye = np.expand_dims(r_eye, axis=0)
                rpred = model.predict_classes(r_eye)

            for (x, y, w, h) in left_eye:
                l_eye = frame[y:y + h, x:x + w]
                count = count + 1
                l_eye = cv2.cvtColor(l_eye, cv2.COLOR_BGR2GRAY)
                l_eye = cv2.resize(l_eye, (24, 24))
                l_eye = l_eye / 255
                l_eye = l_eye.reshape(24, 24, -1)
                l_eye = np.expand_dims(l_eye, axis=0)
                lpred = model.predict_classes(l_eye)

            dets = detector(img, 1)
            print("Number of faces detected: {}".format(len(dets)))
            for k, d in enumerate(dets):
                print("Detection {}: Left: {} Top: {} Right: {} Bottom: {}".format(
                    k, d.left(), d.top(), d.right(), d.bottom()))
                # Get the landmarks/parts for the face in box d.
                shape = predictor(img, d)

                # The next lines of code just get the coordinates for the mouth
                # and crop the mouth from the image.This part can probably be optimised
                # by taking only the outer most points.
                xmouthpoints = [shape.part(x).x for x in range(48, 67)]
                ymouthpoints = [shape.part(x).y for x in range(48, 67)]
                maxx = max(xmouthpoints)
                minx = min(xmouthpoints)
                maxy = max(ymouthpoints)
                miny = min(ymouthpoints)

                # to show the mouth properly pad both sides
                pad = 10
                # basename gets the name of the file with it's extension
                # splitext splits the extension and the filename
                # This does not consider the condition when there are multiple faces in each image.
                # if there are then it just overwrites each image and show only the last image.
                # filename = os.path.splitext(os.path.basename(f))[0]

                crop_image = img[miny - pad:maxy + pad, minx - pad:maxx + pad]
                cv2.imwrite('mouth.jpg', crop_image)
                mouth = cv2.imread("mouth.jpg")
                mouth = cv2.cvtColor(mouth, cv2.COLOR_BGR2GRAY)
                mouth = cv2.resize(mouth, (24, 24))
                mouth = mouth / 255
                mouth = mouth.reshape(24, 24, -1)
                mouth = np.expand_dims(mouth, axis=0)
                mpred = model2.predict_classes(mouth)
                print(mpred)
                if (mpred[0] == 1):
                    sts = 'Yawning'
                if (mpred[0] == 0):
                    sts = 'NO-Yawning'
                print(sts)
                print("right=", rpred[0])
                print("left=", lpred[0])

            if (rpred[0] == 0 and lpred[0] == 0):
                score = score + 1
                cv2.putText(frame, "eye_closed", (10, height - 20), font, 1, (255, 255, 255), 1, cv2.LINE_AA)

            else:
                score = score - 1
                cv2.putText(frame, "eye_open", (10, height - 20), font, 1, (255, 255, 255), 1, cv2.LINE_AA)

            if (score < 0):
                score = 0
            cv2.putText(frame, 'Score:' + str(score), (150, height - 20), font, 1, (255, 255, 255), 1, cv2.LINE_AA)

            # Yawning
            if mpred[0] == 1:
                score2 = score2 + 1
                cv2.putText(frame, "Yawning", (320, height - 20), font, 1, (255, 255, 255), 1, cv2.LINE_AA)
            else:
                score2 = score2 - 1
                cv2.putText(frame, "No_Yawning", (320, height - 20), font, 1, (255, 255, 255), 1, cv2.LINE_AA)

            if (score2 < 0):
                score2 = 0
            cv2.putText(frame, 'Score:' + str(score2), (500, height - 20), font, 1, (255, 255, 255), 1, cv2.LINE_AA)

            if (score > 15 or score2 > 15):
                # person is feeling sleepy so we beep the alarm
                cv2.imwrite(os.path.join(path, 'image.jpg'), frame)
                try:
                    sound.play()
                    cv2.putText(frame, "DROWSINESS ALERT..!", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

                except:  # isplaying = False
                    pass
                if (thicc < 16):
                    thicc = thicc + 2
                else:
                    thicc = thicc - 2
                    if (thicc < 2):
                        thicc = 2
                cv2.rectangle(frame, (0, 0), (width, height), (0, 0, 255), thicc)
            cv2.imshow('frame', frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        cap.release()
        cv2.destroyAllWindows()
    except  Exception as e:
        print(e)

#drowsy_detection()