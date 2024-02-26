import threading
import time
import pygame
import schedule
import datetime
from section_info import SectionInfo
import json
import sys
import pygame
import os

# 0 metro
# 1 hihat
# 2 hihat-open
# 3 hihat-foot
# 4 snare-drum
# 5 snare-stick
# 6 tom1
# 7 tom2
# 8 tom3 
# 9 bass
# 10 crash
# 11 ride
# 12 cup

class DrumPlayer:
    def __init__(self):
        self.sheet = []
        self.current_position = 0
        self.isPlaying = False
        self.isPaused = False
        self.play_Metro = False
        self.modified_speed = 0
        self.thread = None
        pygame.mixer.init()
        self.sound =[]
        if os.name == 'nt' :
            self.sound.append([pygame.mixer.Sound('.\\res\\metro_1.mp3'), pygame.mixer.Sound('.\\res\\metro_2.mp3')]) #节拍器
            self.sound.append(pygame.mixer.Sound('.\\res\\hihat.mp3')) #踩镲 
            self.sound.append(pygame.mixer.Sound('.\\res\\hihat-open.mp3')) #踩镲开
            self.sound.append(pygame.mixer.Sound('.\\res\\hihat-foot.mp3')) #踩镲脚
            self.sound.append(pygame.mixer.Sound('.\\res\\snare-drum.mp3')) #军鼓
            self.sound.append(pygame.mixer.Sound('.\\res\\snare-stick.mp3')) #军鼓边击
            self.sound.append(pygame.mixer.Sound('.\\res\\tom1.mp3')) #tom1
            self.sound.append(pygame.mixer.Sound('.\\res\\tom2.mp3')) #tom2
            self.sound.append(pygame.mixer.Sound('.\\res\\tom3.mp3')) #tom3
            self.sound.append(pygame.mixer.Sound('.\\res\\bass.mp3')) #底鼓
            self.sound.append(pygame.mixer.Sound('.\\res\\crash.mp3'))  #吊镲
            self.sound.append(pygame.mixer.Sound('.\\res\\ride.mp3')) #叮叮镲
            self.sound.append(pygame.mixer.Sound('.\\res\\ride-bell.mp3')) #叮叮镲-帽
        else:
            self.sound.append([pygame.mixer.Sound(
                './res/metro_1.mp3'), pygame.mixer.Sound('./res/metro_2.mp3')])
            self.sound.append(pygame.mixer.Sound('./res/hihat.mp3')) #踩镲 
            self.sound.append(pygame.mixer.Sound('./res/hihat-open.mp3')) #踩镲开
            self.sound.append(pygame.mixer.Sound('./res/hihat-foot.mp3')) #踩镲脚
            self.sound.append(pygame.mixer.Sound('./res/snare-drum.mp3')) #军鼓
            self.sound.append(pygame.mixer.Sound('./res/snare-stick.mp3')) #军鼓边击
            self.sound.append(pygame.mixer.Sound('./res/tom1.mp3')) #tom1
            self.sound.append(pygame.mixer.Sound('./res/tom2.mp3')) #tom2
            self.sound.append(pygame.mixer.Sound('./res/tom3.mp3')) #tom3
            self.sound.append(pygame.mixer.Sound('./res/bass.mp3')) #底鼓
            self.sound.append(pygame.mixer.Sound('./res/crash.mp3'))  #吊镲
            self.sound.append(pygame.mixer.Sound('./res/ride.mp3')) #叮叮镲
            self.sound.append(pygame.mixer.Sound('./res/ride-bell.mp3')) #叮叮镲-帽
    
    def load_sheet(self, file):
        with open(file, 'r') as f:
            json_data = json.load(f)
            for i in range(len(json_data)):
                self.sheet.append(SectionInfo(i,json_data[i]['speed'], json_data[i]['divide_num'], json_data[i]['sound_data']))

    def start_play(self, begin_section=0, end_section=None, repeat_time=1, play_metro=False, modified_speed=0):
        if self.sheet is None or len(self.sheet) == 0:
            raise ValueError("Sheet not loaded")
        
        if begin_section < 0 or begin_section >= len(self.sheet):
            raise ValueError("Invalid start section")
        self.begin_section = begin_section

        if end_section == None:
            end_section = len(self.sheet)
        if end_section < 0 or end_section > len(self.sheet):
            raise ValueError("Invalid end section")
        if end_section < begin_section:
            raise ValueError("End section must be greater than or equal to start section")
        
        self.end_section = end_section
        self.repeat_time = repeat_time
        self.play_Metro = play_metro
        self.isPlaying = True
        self.modified_speed = modified_speed
        self.thread = threading.Thread(target=self.__play_method)
        self.thread.start()

    def pause_resume_play(self):
        if self.isPlaying:
            self.isPaused = not self.isPaused

    def stop_play(self):
        self.isPlaying = False
        self.isPaused = False
        if self.thread:
            self.thread.join()
            self.thread = None
    
    def is_playing(self):
        return self.isPlaying
    
    def is_paused(self):
        return self.isPlaying and self.isPaused
    
    def __stop_play_notice(self):
        event = pygame.event.Event(pygame.USEREVENT, custom_type="STOP_PLAY")
        pygame.event.post(event)

    def __play_sound(self, data):
        for i in range(len(data)):
            tone = data[i]
            if tone < len(self.sound):
                self.sound[tone].play()
            
    def __play_metro(self, is_start=True):
        if self.play_Metro:
            self.sound[0][0 if is_start else 1].play()
   
    def __play_method(self):
        while True:
            if self.play_Metro:
                print("play pre beat tone")
                beat_time = 60 / self.modified_speed if self.modified_speed > 0 else self.sheet[self.begin_section].speed
                for i in range(0, 4):
                    st = time.time()
                    self.__play_metro(i == 0)
                    cost = time.time() - st
                    time.sleep(beat_time - cost)
                    
            for i in range(self.begin_section, self.end_section):
                if self.modified_speed == 0:
                    beat_time = 60 / self.sheet[i].speed
                else:
                    beat_time = 60 / self.modified_speed
                shot_time = beat_time / self.sheet[i].divide_num
                data_len = len(self.sheet[i].sound_data)

                for j in range(data_len):
                    while self.isPaused == True:
                        time.sleep(1)

                    st = time.time()
                    if self.isPlaying == False:
                        return
                    if j % self.sheet[i].divide_num == 0:
                        self.__play_metro(j == 0)
                    self.__play_sound(self.sheet[i].sound_data[j])
                    cost = time.time() - st
                    time.sleep(shot_time - cost)

            self.repeat_time -= 1
            if self.repeat_time == 0:
                self.__stop_play_notice()
                return
