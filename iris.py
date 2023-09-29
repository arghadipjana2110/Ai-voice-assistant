import pyttsx3  # pip install pyttsx3
import speech_recognition as sr  # pip install speechRecognition
import datetime
import wikipedia  # pip install wikipedia
import webbrowser
import os
import smtplib
from selenium import webdriver
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import playsound 
import psutil 
from bs4 import BeautifulSoup
import requests
engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
# print(voices[1].id)
engine.setProperty('voice', voices[1].id)
def speak(audio):
    engine.say(audio)
    engine.runAndWait()
def wishMe():
    hour = int(datetime.datetime.now().hour)
    if 0 <= hour < 12:
        speak("Good Morning!")

    elif 12 <= hour < 18:
        speak("Good Afternoon!")

    else:
        speak("Good Evening!")

    speak("I am Iris. Please tell me how can I help you")
def takeCommand():
    # It takes microphone input from the user and returns string output
    r = sr.Recognizer()
    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source,duration=0.5)
        print("Listening...")
        r.pause_threshold = 1
        audio = r.listen(source)

    try:
        print("Recognizing...")
        query = r.recognize_google(audio, language='en-In')
        # query = r.recognize_google(audio)
        print(f"User said: {query}\n")

    except Exception as e:
        # print(e)    
        print("Say that again please...")
        return "None"
    return query
def sendEmail(to, content):
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.login('souvikkumar.das@tnu.in', 'S7o6u8v8i4k5#')
    server.sendmail('arghadipjana270@gmail.com', to, content)
    server.close()
def get_headlines():
    url = "https://www.bbc.com/news/world/asia/india"  # Replace with the URL of the news website you want to scrape
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    headlines = []
    # Find the HTML elements containing the headlines and extract the text
    # Customize this code based on the structure of the news website you are scraping
    headline_elements = soup.find_all('h3', class_='headline')

    for i, element in enumerate(headline_elements):
        headline = element.text.strip()
        headlines.append(headline)
        
        # Limit to 5 headlines
        if i == 4:
            break

    return headlines
def task():
    wishMe()
    while True:
        # if 1:
        query = takeCommand().lower()
        # Logic for executing tasks based on query
        if 'wikipedia' in query:
            speak('Searching Wikipedia...')
            query = query.replace("wikipedia", "")
            results = wikipedia.summary(query, sentences=2)
            speak("According to Wikipedia")
            print(results)
            speak(results)
        elif 'battery status' in query:
            battery = psutil.sensors_battery()  
            plugged = battery.power_plugged
            if plugged: 
             percent =battery.percent
             if percent <= 80: 
               speak(" Charger Plugged In, To get the better battery life, charge upto 80%")
                
             elif percent ==100:
                speak("Please plugged out the charger. Battery is charged")
                 
            else:  
              percent = battery.percent
              if percent <= 20:  
               speak('Battery Reminder, Your battery is running low. You might want to plug in your PC')
               
      
              elif percent <= 50:  
               speak(f'battery percent is below{percent}')   
              else:  
                 speak(f'Battery percent is {percent}')
        elif 'open facebook' in query:
            usr='rockstarjd942@gmail.com'
            pwd='rockjd942'

            driver = webdriver.Chrome()
            driver.get('https://www.facebook.com/')
            print ("Opened facebook")
            

            username_box = driver.find_element(By.ID,'email')
            username_box.send_keys(usr)
            print ("Email Id entered")
        

            password_box = driver.find_element(By.ID,'pass')
            password_box.send_keys(pwd)
            print ("Password entered")

            login_box = driver.find_element(By.XPATH,'/html/body/div[1]/div[1]/div[1]/div/div/div/div[2]/div/div[1]/form/div[2]/button')
            login_box.click()
            driver.quit   
                    
        elif 'play' in query:
            driver: WebDriver = webdriver.Chrome()
            driver.maximize_window()

            wait = WebDriverWait(driver, 3)
            # presence = EC.presence_of_element_located
            visible = EC.visibility_of_element_located
            video =  query.split("for")[-1]
            # Navigate to url with video being appended to search_query
            driver.get('https://www.youtube.com/results?search_query={}'.format(str(video)))

            # play the video
            wait.until(visible((By.XPATH, '/html/body/ytd-app/div[1]/ytd-page-manager/ytd-search/div[1]/ytd-two-column-search-results-renderer/div/ytd-section-list-renderer/div[2]/ytd-item-section-renderer/div[3]/ytd-video-renderer[1]/div[1]/div/div[1]/div/h3/a')))
            driver.find_element(By.XPATH, '/html/body/ytd-app/div[1]/ytd-page-manager/ytd-search/div[1]/ytd-two-column-search-results-renderer/div/ytd-section-list-renderer/div[2]/ytd-item-section-renderer/div[3]/ytd-video-renderer[1]/div[1]/div/div[1]/div/h3/a').click()
            driver.quit
        # Play the video.
        elif "buzzing" in query or "news" in query or "headlines" in query:
            # headlines = get_headlines()

            # for headline in headlines:
            #    print(headline)
            #    speak(headline)

            try:
              url = 'https://www.bbc.com/news/world/asia/india'
              response = requests.get(url)
  
              soup = BeautifulSoup(response.text, 'html.parser')
              headlines = soup.find('body').find_all('h3')
              unwanted = ['BBC World News TV', 'BBC World Service Radio',
               'News daily newsletter', 'Mobile app', 'Get in touch']
              speak("headlines are")
              for i, x in list(dict.fromkeys(headlines)):
                if x.text.strip() not in unwanted:
                 print(x.text.strip())
                 speak(x.text.strip())
                break
            except Exception as e:
               print(str(e))
        elif 'search' in query:
            #set chromodriver.exe path
           driver = webdriver.Chrome()
           driver.implicitly_wait(0.5)
           search_term = query.split("for")[-1]
           driver.get("https://www.google.com/")
           m = driver.find_element(By.NAME,'q')
           m.send_keys(search_term)
           time.sleep(0.2)
           m.send_keys(Keys.ENTER)
        elif 'open stackoverflow' in query:
           webbrowser.open("stackoverflow.com")

        elif 'play music' in query:
            music_dir = "E:\\music"
            songs = os.listdir(music_dir)
            print(songs)
            os.startfile(os.path.join(music_dir, songs[0]))

        elif 'the time' in query:
            strtime = datetime.datetime.now().strftime("%H:%M:%S")
            speak(f"Sir, the time is {strtime}")

        elif 'open code' in query:
            codepath = "C:\\Users\\Souvik Das\\AppData\\Local\\Programs\\Microsoft VS Code\\Code.exe"
            os.startfile(codepath)

        elif 'email' in query:
            try:
                speak("What should I say?")
                content = query
                to = "arghadipjana270@gmail.com"
                sendEmail(to, content)
                speak("Email has been sent!")
            except Exception as e:
                print(e)
                speak("Sorry my friend sir. I am not able to send this email")
        elif "goodbye" in query:
            speak("see you soon")
            exit()
        elif "power off" in query:
            speak("Do you want to shutdown your laptop")
            while True:
                command = takeCommand()
                if "no" in command:
                    speak("Thank u sir I will not shut down the computer")
                    break
                if "yes" in command:
                    # Shutting down
                    speak("Shutting down the computer")
                    os.system("shutdown /s /t 0")
                    break

        elif "restart" in query:
            speak("Do you want to restart your laptop")
            while True:
                command = takeCommand()
                if "no" in command:
                    speak("Thank u sir I will not shut down the computer")
                    break
                if "yes" in command:
                    # restart
                    speak("restarting the computer")
                    os.system("shutdown /r /t 0")
                    break

      

if __name__ == "__main__":
    while True:
        permission = takeCommand().lower()
        if "hello" in permission:
            playsound.playsound("C:/Users/Souvik Das/Music/achive-sound-132273.mp3")
            speak("welcome back ")
            task()
        
