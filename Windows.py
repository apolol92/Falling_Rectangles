import tkinter as tk
import WordRecognizer as wr
import GameThread as gt
import pyaudio
import wave

class MainWindow:

    def __init__(self):
        self.root = tk.Tk()
        self.root.title('Falling Rectangles')

        self.button_start_game = tk.Button(self.root, text="Start Game!", command=self.button_start_game_click, width=25)
        self.button_start_game.pack()
        self.root.mainloop()

    def button_start_game_click(self):
        GameWindow()

class GameWindow:
    GAME_WIDTH = 500
    GAME_HEIGHT = 600

    def __init__(self):
        self.window = tk.Tk()
        self.window.title('Playing Falling Rectangles')
        self.gamescene = tk.Canvas(self.window, width=self.GAME_WIDTH, height=self.GAME_HEIGHT)
        self.gamescene.pack()
        #Prepare WordRecognizer
        self.recognizer = wr.TwoWordRecognizer()
        self.recognizer.loadReferenceWords("reference_words/left.wav","reference_words/right.wav")
        self.recognizer.loadData("left/","right/")
        #Add GameThread
        self.game_thread = gt.GameThread(self.gamescene, self.window)
        self.game_thread.start()
        #Add KeyEvent
        self.window.bind("s",self.speak)
        #Show window
        self.window.mainloop()

    def speak(self,event):
        print("Say something..")
        FORMAT = pyaudio.paInt16
        CHANNELS = 2
        RATE = 44100
        CHUNK = 1024
        RECORD_SECONDS = 1
        WAVE_OUTPUT_FILENAME = "input.wav"

        audio = pyaudio.PyAudio()

        # start Recording
        stream = audio.open(format=FORMAT, channels=CHANNELS,
                        rate=RATE, input=True,
                        frames_per_buffer=CHUNK)
        print("recording...")
        frames = []

        for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
            data = stream.read(CHUNK)
            frames.append(data)
        print("finished recording")

        # stop Recording
        stream.stop_stream()
        stream.close()
        audio.terminate()

        waveFile = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
        waveFile.setnchannels(CHANNELS)
        waveFile.setsampwidth(audio.get_sample_size(FORMAT))
        waveFile.setframerate(RATE)
        waveFile.writeframes(b''.join(frames))
        waveFile.close()
        t = self.recognizer.predict(WAVE_OUTPUT_FILENAME)
        print(t)
        if(t==1):
            #left
            right = False
        elif(t==2):
            right = True

        if(right==False):
            #left
            self.game_thread.player_bat.moveX(-20)
        else:
            #right
            self.game_thread.player_bat.moveX(20)

