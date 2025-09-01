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

    def create_ui(self):
        input_layout = BoxLayout(size_hint=(1, 0.4))

        self.input_text = TextInput(
            hint_text = 'Enter human text here...',
            size_hint = (0.5, 0.9),
            multiline = True
        )
        self.input_text.bind(text=self.on_text_change)

        self.output_text = TextInput(
            hint_text = 'Duck translation...',
            size_hint = (0.5, 0.9),
            multiline = True,
            readonly = True
        )

        input_layout.add_widget(self.input_text)
        input_layout.add_widget(self.output_text)
        self.add_widget(input_layout)

        self.praise_button = Button(
            text = 'Praise the Great Duck',
            size_hint = (0.8, 0.8),
            pos_hint = {'x':0, 'y':0}
        )
        self.praise_button.bind(on_press=self.praise_duck)
        self.add_widget(self.praise_button)

        self.duck_counter = Label(
            text = 'Ducks arrived: 0',
            size_hint = (0.3, 0.1),
            pos_hint = {'right':1, 'y':0}
        )
        self.add_widget(self.duck_counter)



