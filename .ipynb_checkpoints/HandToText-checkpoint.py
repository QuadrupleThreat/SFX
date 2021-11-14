import cv2
import pickle
import pandas as pd
import mediapipe as mp

cv2.namedWindow("preview")
vc = cv2.VideoCapture(0)

mpHands = mp.solutions.hands
hands = mpHands.Hands()
mpDraw = mp.solutions.drawing_utils

columns = ["wrist_x", "wrist_y", "thumb_cmc_x", "thumb_cmc_y", "thumb_mcp_x", "thumb_mcp_y", "thumb_ip_x", "thumb_ip_y", 
           "thumb_tip_x", "thumb_tip_y", "index_finger_mcp_x", "index_finger_mcp_y", "index_finger_pip_x", "index_finger_pip_y",
           "index_finger_dip_x", "index_finger_dip_y", "index_finger_tip_x", "index_finger_tip_y", "middle_finger_mcp_x", "middle_finger_mcp_y",
           "middle_finger_pip_x", "middle_finger_pip_y", "middle_finger_dip_x", "middle_finger_dip_y", "middle_finger_tip_x", "middle_finger_tip_y",
           "ring_finger_mcp_x", "ring_finger_mcp_y", "ring_finger_pip_x", "ring_finger_pip_y", "ring_finger_dip_x", "ring_finger_dip_y",
           "ring_finger_tip_x", "ring_finger_tip_y", "pinky_mcp_x", "pinky_mcp_y", "pinky_pip_x", "pinky_pip_y", "pinky_dip_x", "pinky_dip_y",
           "pinky_tip_x", "pinky_tip_y"]

actual_columns = []
for loc in ["right_", "left_"]:
    for column in columns:
        new_column = loc + column
        actual_columns.append(new_column)

data = pd.DataFrame(columns=actual_columns)

file_name = 'sign_language.sav'
loaded_model = pickle.load(open(file_name, 'rb'))

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
                    h, w, _ = frame.shape
                    cx, cy = int(lm.x * w), int(lm.y * h)

                    if (id * 2 + 1 <= len(columns)):
                        column_x = columns[id * 2]
                        column_y = columns[(id * 2) + 1]
                        row_data[acutal_hand + column_x] = cx
                        row_data[acutal_hand + column_y] = cy
                        imLst.append([id, cx, cy])

                hand_index += 1
                mpDraw.draw_landmarks(frame, handlandmark, mpHands.HAND_CONNECTIONS)

#            if imLst:
#                x1, y1 = imLst[4][1], imLst[4][2]
#                x2, y2 = imLst[8][1], imLst[8][2]
#
#                cv2.circle(frame, (x1, y1), 4, (255, 0, 0), cv2.FILLED)
#                cv2.circle(frame, (x2, y2), 4, (255, 0, 0), cv2.FILLED)
#                cv2.line(frame, (x1, y1), (x2, y2), (255, 0, 0), 3)
    
        if imLst:
            #data = data.append(row_data, ignore_index=True)
            img = pd.DataFrame(row_data, index = [0])
            print(loaded_model.predict(img))
        print("")
        cv2.imshow("preview", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

#data.to_csv(r'you.csv', index = False, header = True)
