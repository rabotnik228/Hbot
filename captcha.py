import os
import random
import speech_recognition
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from fake_useragent import UserAgent
import speech_recognition as sr
import urllib
import pydub


def delay():
    time.sleep(random.randint(2, 3))


def cor_capt():
    options = webdriver.ChromeOptions()
    ua = UserAgent(browsers=['edge', 'chrome'])
    userAgent = ua.chrome
    print(userAgent)
    options.add_argument(f'user-agent={userAgent}')
    options.add_experimental_option("useAutomationExtension", False)
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_argument('--disable-blink-features=AutomationControlled')
    driver = webdriver.Chrome(os.getcwd() + "\\webdriver\\chromedriver.exe", options=options)
    driver.get("https://www.google.com/recaptcha/api2/demo")
    '''driver.get("https://patrickhlauke.github.io/recaptcha/")'''

    frames = driver.find_elements_by_tag_name("iframe")
    driver.switch_to.frame(frames[0])
    delay()
    driver.find_element_by_class_name("recaptcha-checkbox-border").click()

    driver.switch_to.default_content()
    frames = driver.find_element_by_xpath("/html/body/div[last()]/div[4]").find_elements_by_tag_name("iframe")
    driver.switch_to.frame(frames[-1])
    delay()

    driver.find_element_by_id("recaptcha-audio-button").click()

    driver.switch_to.default_content()
    frames = driver.find_elements_by_tag_name("iframe")
    driver.switch_to.frame(frames[-1])
    delay()

    driver.find_element_by_xpath("/html/body/div/div/div[3]/div/button").click()
    src = driver.find_element_by_id("audio-source").get_attribute("src")
    print("[INFO] Audio src: %s" % src)

    urllib.request.urlretrieve(src, os.getcwd() + "\\sample.mp3")
    sound = pydub.AudioSegment.from_mp3(os.getcwd() + "\\sample.mp3")
    sound.export(os.getcwd() + "\\sample.wav", format="wav")
    sample_audio = sr.AudioFile(os.getcwd() + "\\sample.wav")
    r = speech_recognition.Recognizer()
    with sample_audio as source:
        user_audio = r.record(source)
    key = r.recognize_google(audio_data=user_audio, language='en-US')
    print("[INFO] Recaptcha Passcode: %s" % key)

    driver.find_element_by_id("audio-response").send_keys(key.lower())
    driver.find_element_by_id("audio-response").send_keys(Keys.ENTER)
    driver.switch_to.default_content()
    delay()
    return cor_capt()


cor_capt()
