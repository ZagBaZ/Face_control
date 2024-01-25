import sqlite3
import datetime
import face_recognition
import cv2
import numpy as np
import telebot
import schedule
import os
from dotenv import load_dotenv

load_dotenv()

#Токены
TOKEN = os.getenv("TOKEN")
USER_BOT = os.getenv("USER_BOT")
bot = telebot.TeleBot(TOKEN)

HOUR_MAX = 10
TIME_SEND_MESSAGE = "12:00"


video_capture = cv2.VideoCapture(0, cv2.CAP_DSHOW)

jinping_image = face_recognition.load_image_file("./foto/jinping.jpeg")
jinping_face_encoding = face_recognition.face_encodings(jinping_image)[0]

biden_image = face_recognition.load_image_file("./foto/biden.jpg")
biden_face_encoding = face_recognition.face_encodings(biden_image)[0]

putin_image = face_recognition.load_image_file("./foto/putin.jpg")
putin_face_encoding = face_recognition.face_encodings(putin_image)[0]


known_face_encodings = [
    jinping_face_encoding,
    biden_face_encoding,
    putin_face_encoding
]
known_face_names = [
    "Xi Jinping",
    "Biden",
    'Putin'
]

def job():
    dt = datetime.datetime.today()
    connection = sqlite3.connect('my_database.db')
    cursor = connection.cursor()

    cursor.execute('SELECT surname, hour, minute FROM Employee WHERE day = ? AND hour < ? ORDER BY hour', (dt.day, HOUR_MAX))
    results = cursor.fetchall()
    
    message_bot = ("На ", str(dt.day), '.', str(dt.month), ':', '\n')
    
    for row in results:
        print(row)
        message_row = ('Сотрудник ',  row[0],  ' пришел в ', str(row[1]).zfill(2), ':', str(row[2]).zfill(2), '\n')
        message_bot = message_bot + message_row
    message_bot = ''.join(message_bot)
    bot.send_message(USER_BOT, message_bot)
        
    connection.close()
    
schedule.every().day.at(TIME_SEND_MESSAGE).do(job)

while True:
    ret, frame = video_capture.read()
    rgb_frame = frame[:, :, ::-1]
    face_locations = face_recognition.face_locations(rgb_frame)
    face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)
    
    for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
        matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
        name = "Unknown"
        face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
        best_match_index = np.argmin(face_distances)
        if matches[best_match_index]:
            name = known_face_names[best_match_index]
            dt = datetime.datetime.today()
            connection = sqlite3.connect('my_database.db')
            cursor = connection.cursor()

            cursor.execute('''
            CREATE TABLE IF NOT EXISTS Employee (
            id INTEGER PRIMARY KEY,
            day INTEGER NOT NULL,
            month INTEGER NOT NULL,
            hour INTEGER NOT NULL,
            minute INTEGER NOT NULL,
            surname TEXT NOT NULL
            )
            ''')

            cursor.execute('SELECT day, month, surname FROM Employee WHERE surname = ? AND day = ?', (name, dt.day))
            results = cursor.fetchall()          
            if not results:
                cursor.execute('INSERT INTO Employee (day, month, hour, minute, surname) VALUES (?, ?, ?, ?, ?)', (
                dt.day, dt.month, dt.hour, dt.minute, name)
                        )         
            connection.commit()
            connection.close()

        cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)
        font = cv2.FONT_HERSHEY_DUPLEX
        cv2.putText(frame, name, (left + 6, bottom + 16), font, 1.0, (255, 255, 255), 1)
    
    cv2.imshow('Video', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    schedule.run_pending()

video_capture.release()
cv2.destroyAllWindows()
