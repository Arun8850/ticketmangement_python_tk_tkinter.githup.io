import pyttsx3
import datetime
import speech_recognition as sr
import os
import random
import smtplib
from fpdf import FPDF
from tkinter import *
from tkinter import messagebox
from twilio.rest import Client
from ttkthemes import themed_tk as tk
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders

import smtplib
import pymysql

c = 0

engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voices', voices[0].id)


# print(voices[0].id)= man voices
def speak(audio):
    engine.say(audio)
    engine.runAndWait()


def wishme():
    hour = int(datetime.datetime.now().hour)
    if hour > 0 and hour < 12:
        speak("Good Morning")
    elif hour >= 12 and hour < 18:
        speak("Good After Non")
    else:
        speak("Good Evening")
    speak("i am jarvis sir. please tell me how can i help you")


def takeCommand():
    # It takes microphone input from the user and returns string output

    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1
        audio = r.listen(source, timeout=1, phrase_time_limit=50)
    try:

        print("Recognizing...")
        query = r.recognize_google(audio, language='en-in')  # Using google for voice recognition.
        print(f"User said: {query}\n")  # User query will be printed.
    except Exception as e:
        speak("Say that again please...")  # Say that again will be printed in case of improper voice
        return "None"  # None string will be returned
    return query


def sendEmail(to, content):
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()

    server.login('babakijaiho866@gmail.com', 'Pass@1234')
    server.sendmail('babakijaiho866@gmail.com', to, content)
    server.close()


def registration():
    c = 0
    speak("please tell your name")
    con = pymysql.connect(host="localhost", user="root", password="Root", database="login")
    cur = con.cursor()
    name = takeCommand().lower()
    speak("please tell your emailid")
    emailid = takeCommand().lower()
    speak("please tell your password")
    pw = takeCommand().lower()
    speak("please confirm your password")
    cpw = takeCommand().lower()
    speak("please tell your contact number")
    cn = takeCommand().lower()
    speak("please tell your full name")
    fn = takeCommand().lower()
    if (pw != cpw):
        speak("your password is not same as your confirm password please try again.....")
        c = c + 1
        return c

    else:
        cur.execute("INSERT INTO register VALUES (%s,%s,%s,%s,%s,%s)", (name, emailid, pw, cpw, cn, fn))
        con.commit()
        con.close()
        speak("regestration is successfull")
        c += 1
        return c


def login():
    con = pymysql.connect(host="localhost", user="root", password="Root", database="login")
    cur = con.cursor()
    speak("kindly tell your user name")
    name = takeCommand().lower()
    speak("kindly tell your password")
    p_id = takeCommand().lower()
    cur.execute("select * from register where username= %s and password=%s", (name, p_id))
    row = cur.fetchall()
    name1 = row[0][0]
    pas = row[0][2]
    if (name1 == name and pas == p_id):
        speak("login is successful")
    else:
        speak("invalid password or user name,please try again")

    con.commit()
    con.close()


if __name__ == "__main__":

    # speak("Code With Harry")
    # speak("please tell your name")
    wishme()
    takeCommand()
    while True:
        query = takeCommand().lower()
        if "open notepad" in query:
            npath = "C:\\Windows\\system32\\notepad.exe"
            os.startfile(npath)
        elif 'email to company' in query:

            try:
                speak("What should I say?")
                content = takeCommand()
                to = "arun.pandey@slrtce.in"
                sendEmail(to, content)
                speak("Email has been sent!")
            except Exception as e:
                print(e)
                speak("Sorry my friend "
                      ". I am not able to send this email")
        elif "open registration" in query:
            registration()
            if (c == 1):
                speak("kindly login")
            login()
        elif "open login" in query:
            login()

        elif "open userprofile" in query:
            speak("kindly tell your Full name")
            name = takeCommand().lower()
            speak("kindly tell your skill")
            sk = takeCommand().lower()
            speak("kindly tell your email_id")
            email = takeCommand().lower()
            speak("kindly tell your branch")
            br = takeCommand().lower()
            speak("kindly tell your project link")
            p_l = takeCommand().lower()
            # print("arrra")

            try:
                ##print("aaaa")

                my_pdf = FPDF()
                my_pdf.add_page()
                my_pdf.set_font("Arial", size=16)
                my_pdf.cell(200, 10, txt="My Resume", ln=1, align="C")
                text = (
                        "Respected Sir/Madam,\n I am " + name)
                my_pdf.cell(200, 10, txt=text, ln=2, align="C")
                text = (" \nI have learned the following " + sk)
                my_pdf.cell(200, 10, txt=text, ln=3, align="C")
                text = (" thourly \ni have done my graduation in " + br)
                my_pdf.cell(200, 10, txt=text, ln=4, align="C")
                text = (" i have made following projects " + p_l)
                my_pdf.cell(200, 10, txt=text, ln=5, align="C")
                text = ("\n  Yours Faithfully\n " + name)
                my_pdf.cell(200, 10, txt=text, ln=6, align="C")
                my_pdf.output("myPDF.pdf")
                '''


                l_user = 'babakijaiho866@gmail.com'
                email_password = 'Pass@1234'
                email_send = email

                subject = 'Your Resume'

                msg = MIMEMultipart()
                msg['From'] = l_user
                msg['To'] = email_send
                msg['Subject'] = subject


                body = 'Hi here, is your resume'
                msg.attach(MIMEText(body, 'plain'))


                filename = 'myPDF.pdf'
                attachment = open(filename, 'rb')

                part = MIMEBase('application', 'octet-stream')
                part.set_payload((attachment).read())
                encoders.encode_base64(part)
                part.add_header('Content-Disposition', "attachment; filename= " + filename)

                msg.attach(part)
                text = msg.as_string()
                server = smtplib.SMTP('smtp.gmail.com', 587)
                server.starttls()
                server.login(l_user, email_password)

                server.sendmail(l_user, email_send, text)
                server.quit()
                speak("resume is been send successfull")
                '''


            except Exception as es:
                messagebox.showerror("Error", f"Error due to:(str(es))")

        # cur.execute("INSERT INTO resume VALUES (%s,%s,%s,%s,%s,%s)", (name, sk, e_id, br,p_l))
        # con.commit()











