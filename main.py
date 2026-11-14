from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label

class PhoneCheckerApp(App):
    def build(self):
        layout = BoxLayout(orientation='vertical', padding=20, spacing=10)
        
        self.check_btn = Button(text='Проверить', size_hint_y=None, height=50)
        self.check_btn.bind(on_press=self.check_number)
        layout.add_widget(self.check_btn)
        
        self.result_label = Label(text='Приложение работает!')
        layout.add_widget(self.result_label)
        
        return layout

    def check_number(self, instance):
        self.result_label.text = "Кнопка нажата! Kivy работает."

if __name__ == '__main__':
    PhoneCheckerApp().run()
