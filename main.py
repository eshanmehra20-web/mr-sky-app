import os
import sys
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.core.window import Window

# सुरक्षा के लिए बैकग्राउंड डार्क सेट करना
Window.clearcolor = (0.05, 0.05, 0.05, 1)

class MrSkyApp(App):
    def build(self):
        self.title = "Mr. Sky Sentinel"
        self.correct_pin = "7860"  # आप चाहें तो अपना सीक्रेट पिन बदल सकते हैं
        
        self.layout = BoxLayout(orientation='vertical', padding=40, spacing=20)
        
        # हेडर टेक्स्ट
        self.header_label = Label(
            text="[b]MR. SKY[/b]\nAuthorized Access Only",
            markup=True,
            font_size='22sp',
            color=(0.9, 0.9, 0.9, 1),
            halign='center'
        )
        self.layout.add_widget(self.header_label)
        
        # पिन इनपुट बॉक्स
        self.pin_input = TextInput(
            hint_text="Enter Secret PIN",
            password=True,
            multiline=False,
            font_size='24sp',
            size_hint_y=None,
            height='50dp',
            halign='center'
        )
        self.layout.add_widget(self.pin_input)
        
        # अनलॉक बटन
        self.login_btn = Button(
            text="Unlock Sentinel",
            font_size='18sp',
            size_hint_y=None,
            height='50dp',
            background_color=(0.1, 0.6, 0.3, 1)
        )
        self.login_btn.bind(on_press=self.verify_pin)
        self.layout.add_widget(self.login_btn)
        
        # स्टेटस या रिजल्ट डिस्प्ले
        self.status_label = Label(
            text="",
            font_size='16sp',
            color=(1, 0.3, 0.3, 1),
            halign='center'
        )
        self.layout.add_widget(self.status_label)
        
        return self.layout

    def verify_pin(self, instance):
        entered_pin = self.pin_input.text.strip()
        if entered_pin == self.correct_pin:
            self.status_label.color = (0.2, 1, 0.2, 1)
            self.status_label.text = "Access Granted: Welcome Master."
        else:
            self.status_label.color = (1, 0.3, 0.3, 1)
            self.status_label.text = "Access Denied: Invalid PIN!"
            self.pin_input.text = ""

if __name__ == '__main__':
    MrSkyApp().run()
