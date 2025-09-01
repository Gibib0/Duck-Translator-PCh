from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.popup import Popup
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.core.audio import SoundLoader
from kivy.graphics import Color, Rectangle
import random
import os

class DuckTranslator(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.duck_counter = 0
        self.background_sound = None
        self.current_sound = None

        self.load_assets()
        self.create_ui()
        self.show_warning()

        Clock.schedule_interval(self.imcrement_duck_count, 1)

        self.play_background_music()

    def load_assests(self):
        self.sound = {
            'background': SoundLoader.load('assets/sounds/background_sound.wav'),
            'duck': SoundLoader.load('assets/sounds/duck_sound.wav'),
            'iloveyou': SoundLoader.load('assets/sounds/ILoveU_sound.wav'),
            'screamer': SoundLoader.load('assets/sounds/screamer_sound.wav'),
            'holy': SoundLoader.load('assets/sounds/holy_sound.wav')
        }

        for sound in self.sounds.values():
            if sound: sound.volume = 0.7



