import cv2
import pickle
import numpy as np
import pandas as pd
import mediapipe as mp
from sklearn import preprocessing
from database_functions import sendtext

cv2.namedWindow("preview")
vc = cv2.VideoCapture(0)

mpHands = mp.solutions.hands
hands = mpHands.Hands()
mpDraw = mp.solutions.drawing_utils

columns = ["wrist_x", "wrist_y", "wrist_z", "thumb_cmc_x", "thumb_cmc_y", "thumb_cmc_z", "thumb_mcp_x", "thumb_mcp_y", "thumb_mcp_z", "thumb_ip_x", "thumb_ip_y", 
           "thumb_ip_z", "thumb_tip_x", "thumb_tip_y", "thumb_tip_z", "index_finger_mcp_x", "index_finger_mcp_y", "index_finger_mcp_z", "index_finger_pip_x", 
           "index_finger_pip_y", "index_finger_pip_z", "index_finger_dip_x", "index_finger_dip_y", "index_finger_dip_z", "index_finger_tip_x", "index_finger_tip_y", 
           "index_finger_tip_z", "middle_finger_mcp_x", "middle_finger_mcp_y", "middle_finger_mcp_z", "middle_finger_pip_x", "middle_finger_pip_y", "middle_finger_pip_z",
           "middle_finger_dip_x", "middle_finger_dip_y", "middle_finger_dip_z", "middle_finger_tip_x", "middle_finger_tip_y", "middle_finger_tip_z", "ring_finger_mcp_x", 
           "ring_finger_mcp_y", "ring_finger_mcp_z", "ring_finger_pip_x", "ring_finger_pip_y", "ring_finger_pip_z", "ring_finger_dip_x", "ring_finger_dip_y", "ring_finger_dip_z",
           "ring_finger_tip_x", "ring_finger_tip_y", "ring_finger_tip_z", "pinky_mcp_x", "pinky_mcp_y", "pinky_mcp_z", "pinky_pip_x", "pinky_pip_y", "pinky_pip_z", "pinky_dip_x", 
           "pinky_dip_y", "pinky_dip_z", "pinky_tip_x", "pinky_tip_y", "pinky_tip_z"]

actual_columns = []
for loc in ["right_", "left_"]:
    for column in columns:
        new_column = loc + column
        actual_columns.append(new_column)

data = pd.DataFrame(columns=actual_columns)
min_max_scaler = preprocessing.StandardScaler()

file_name = 'sign_language.sav'
loaded_model = pickle.load(open(file_name, 'rb'))

words = ["Hello", "to meet", "nice", "everyone"]
last_words = set()
sentence = ""

frame_count = 0
frame_display = "!"

def actual_handedness(hands):
    if (hands == "Right"):
        return "left_"
    return "right_"

while True:
    rval, frame = vc.read()
  
    if frame is not None:
        imgRGB = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = hands.process(imgRGB)

        imLst = []
        row_data = {column: 0 for column in actual_columns}
        if results.multi_hand_landmarks:
            hand_index = 0
            for handlandmark in results.multi_hand_landmarks:
                handedness = results.multi_handedness[hand_index]
                acutal_hand = actual_handedness(handedness.classification[0].label)
                for id, lm in enumerate(handlandmark.landmark):
                    h, w, d = frame.shape
                    cx, cy, cz = int(lm.x * w), int(lm.y * h), int(lm.z * d)
                    if (id * 3 + 1 <= len(columns)):
                        column_x = columns[id * 3]
                        column_y = columns[(id * 3) + 1]
                        column_z = columns[(id * 3) + 2]
                        row_data[acutal_hand + column_x] = cx
                        row_data[acutal_hand + column_y] = cy
                        row_data[acutal_hand + column_z] = cz
                        imLst.append([id, cx, cy])

                hand_index += 1
                mpDraw.draw_landmarks(frame, handlandmark, mpHands.HAND_CONNECTIONS)
    
        if imLst:
            #data = data.append(row_data, ignore_index=True)
            img = pd.DataFrame(row_data, index = [0])
            imgX = img.to_numpy()
            scaled_X = imgX / 1000 #min_max_scaler.fit_transform(imgX)
            probs = loaded_model.predict_proba(scaled_X)
            max_prob = max(probs[0])
            word = words[np.where(probs[0] == max_prob)[0][0]]
            if max_prob >= 0.9 and not word in last_words:
                sentence = sentence + " " + word
                last_words.add(word)

        if sentence != "":
            font = cv2.FONT_HERSHEY_SIMPLEX
            textsize = cv2.getTextSize(sentence, font, 1, 2)[0]
            textX = (frame.shape[1] - textsize[0]) // 2
            textY = (frame.shape[0] + textsize[1]) // 10
            cv2.putText(frame, "Me: " + sentence, (textX, textY), font, 1, (255, 255, 255), 2)

        cv2.imshow("preview", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    if frame_count % 50 == 0  and frame_display == sentence and sentence != "":
        sendtext("hearing_imp", sentence)
        sentence = ""
        last_words = set()
    elif frame_count % 50 == 0  and frame_display != sentence:
        frame_display = sentence

    frame_count += 1

#data.to_csv(r'everyone.csv', index = False, header = True)
