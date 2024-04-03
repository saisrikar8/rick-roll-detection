import keras
import tensorflow as tf
from tensorflow.keras import Sequential
from tensorflow.keras.layers import Dense
from tensorflow.keras.losses import BinaryCrossentropy
from tensorflow.keras.optimizers import Adam
import numpy as np
from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By
import time
import pandas as pd
import pytube
from Audio import get_audio_from_link

# Deep Learning Model to Analyze the Video
class VideoAnalyzer:
    def __init__(self):
        self.model = Sequential([
            Dense(units=64, activation='sigmoid'),
            Dense(units=32, activation='sigmoid'),
            Dense(units=16, activation='sigmoid'),
            Dense(units=8, activation='sigmoid'),
            Dense(units=8, activation='sigmoid'),
            Dense(units=2, activation='sigmoid'),
            Dense(units=1, activation='sigmoid')
        ])
        self.model.compile(
            loss = BinaryCrossentropy(),
            optimizer = Adam(
                learning_rate = 0.12
            )
        )
        self.training_data_x = None
        self.training_data_y = None
        self.get_training_data()


    def get_training_data(self):
        links = list()
        driver = Chrome()
        driver.get('https://www.youtube.com/results?search_query=disguised+rick+roll+video')
        time.sleep(2)
        driver.find_elements(By.XPATH, '//yt-chip-cloud-chip-renderer[@class="style-scope yt-chip-cloud-renderer"]')[1].click()

        maxlen = 0
        # Fetches 500 testcases from youtube
        while (len(links) <= 10):
            time.sleep(2)
            new_links = driver.find_elements(By.XPATH, '//a[@id="video-title"]')
            for new_link in new_links:
                links.append(new_link.get_attribute('href'))
            driver.execute_script('window.scrollBy(0, 1000000)')
            time.sleep(2)

        driver.close()
        # Fetch the links with rick roll and store in a list
        test_data = [[],[]]
        for link in links:
            try:
                audio = get_audio_from_link(link, True)
            except pytube.exceptions.AgeRestrictedError:
                print('This material is age restricted, so it is not being added to the data set')
                continue
            if len(audio[0]) > maxlen:
                maxlen = len(audio[0])
            test_data[0].append(audio[0] + audio[1])
            test_data[1].append(audio[2])
        print('Converting data into compatible formats...')
        self.training_data_x = tf.keras.preprocessing.sequence.pad_sequences(test_data[0])
        self.training_data_y = np.array(test_data[1])
        test_data.clear()
        links.clear()
        time.sleep(10)
        self.model.fit(x=self.training_data_x, y=self.training_data_y)
        self.training_data_x = None
        self.training_data_y = None
        driver = Chrome()
        driver.get('https://www.youtube.com/results?search_query=interesting')
        time.sleep(2)
        driver.find_elements(By.XPATH, '//yt-chip-cloud-chip-renderer[@class="style-scope yt-chip-cloud-renderer"]')[1].click()

        # Fetches 500 testcases from youtube
        while (len(links) <= 10):
            time.sleep(2)
            new_links = driver.find_elements(By.XPATH, '//a[@id="video-title"]')
            for new_link in new_links:
                links.append(new_link.get_attribute('href'))
            driver.execute_script('window.scrollBy(0, 1000000)')
            time.sleep(2)
        driver.close()
        maxlen = 0
        for link in links:
            try:
                audio = get_audio_from_link(link, False)
                time.sleep(3)
            except pytube.exceptions.AgeRestrictedError:
                continue
            if (len(audio[0]) > maxlen):
                maxlen = len(audio[0])
            test_data[0].append(audio[0] + audio[1])
            test_data[1].append(audio[2])

        #Storing all testcases into a ragged tensor
        self.training_data_x = tf.keras.preprocessing.sequence.pad_sequences(test_data[0], maxlen=maxlen)
        self.training_data_y = np.array(test_data[1])
        self.model.fit(x=self.training_data_x, y=np.array(self.training_data_y))
        self.training_data_x = None
        self.training_data_y = None