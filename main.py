from kivy.app import App
from kivy.uix.label import Label

class PhoneCheckerApp(App):
    def build(self):
        return Label(text="Приложение работает!")

if __name__ == '__main__':
    PhoneCheckerApp().run()
