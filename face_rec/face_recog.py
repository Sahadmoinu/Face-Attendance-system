import cv2
import numpy as np
import os
import face_recognition as fr
import requests
import time

path = 'images'
my_list = os.listdir(path)

imgs = []
ids = []
classnames = []

for i in my_list:
    imgpath = os.path.join(path, i)
    img1 = cv2.imread(imgpath)
    imgs.append(img1)
    id_part = i.split('_')[0]
    name_part = i.split('_')[1].split('.')[0]
    ids.append(id_part)
    classnames.append(name_part)

print("Names:", classnames)
print("IDs:", ids)

# Encode faces
def faceencodings(images):
    encodelist = []
    for i in images:
        img_rgb = cv2.cvtColor(i, cv2.COLOR_BGR2RGB)
        face_in_frame = fr.face_locations(img_rgb)
        if face_in_frame:
            face_encode = fr.face_encodings(img_rgb, face_in_frame)[0]
            encodelist.append(face_encode)
        else:
            encodelist.append(None)
    return encodelist

encodelist_knownface = faceencodings(imgs)

laravel_api_url = "http://127.0.0.1:8000/recognized-face"

def get_latest_status(user_id):
    try:
        response = requests.get(f"{laravel_api_url}/latest-status/{user_id}")
        if response.status_code == 200:
            data = response.json()
            return data.get('status')
    except Exception as e:
        print(f"Failed to fetch latest status for {user_id}:", e)
    return None

video = cv2.VideoCapture(0)

logged_users = {}  
TIMEOUT = 10 

while True:
    success, img = video.read()
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    face_locations = fr.face_locations(img_rgb)
    face_encodings = fr.face_encodings(img_rgb, face_locations)
    current_frame_users = []
    for enc, loc in zip(face_encodings, face_locations):
        matches = fr.compare_faces(encodelist_knownface, enc)
        face_dist = fr.face_distance(encodelist_knownface, enc)
        match_index = np.argmin(face_dist)
        if matches[match_index]:
            user_id = ids[match_index]
            user_name = classnames[match_index]
            current_frame_users.append(user_id)
            if user_id not in logged_users:
                latest_status = get_latest_status(user_id)
                new_status = 'out' if latest_status == 'in' else 'in'
                try:
                    response = requests.post(
                        laravel_api_url,
                        json={"name": user_name, "id": user_id, "status": new_status}
                    )
                    print(f"Logged {user_name} ({user_id}) as {new_status}, response: {response.status_code}")
                except Exception as e:
                    print(f"Failed to send to Laravel: {e}")
            logged_users[user_id] = time.time()
            y1, x2, y2, x1 = loc
            cv2.rectangle(img, (x1, y1), (x2, y2), (0, 0, 255), 3)
            cv2.putText(img, user_name, (x1, y1 - 10), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 255), 2)
    to_remove = [uid for uid, last_seen in logged_users.items() if time.time() - last_seen > TIMEOUT]
    for uid in to_remove:
        del logged_users[uid]
    cv2.imshow("Frame", img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

video.release()
cv2.destroyAllWindows()