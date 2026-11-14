from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
import traceback

# Твои данные
API_ID = 33600401  # <--- ВСТАВЬ СВОЙ API_ID
API_HASH = 'f1ef88aa120c93c9ad95a2c246acaf17' # <--- ВСТАВЬ СВОЙ API_HASH

try:
    # Пытаемся загрузить Telethon
    import ctypes, sys
    ctypes.pythonapi = ctypes.PyDLL("libpython%d.%d.so" % sys.version_info[:2])
    from telethon import TelegramClient
    import asyncio
    
    class PhoneCheckerApp(App):
        def build(self):
            self.layout = BoxLayout(orientation='vertical', padding=20, spacing=10)
            self.phone_input = TextInput(hint_text='Введите номер (+998...)', multiline=False, size_hint_y=None, height=50)
            self.layout.add_widget(self.phone_input)
            self.check_btn = Button(text='Проверить', size_hint_y=None, height=50)
            self.check_btn.bind(on_press=self.check_number)
            self.layout.add_widget(self.check_btn)
            self.scroll = ScrollView()
            self.result_label = Label(text='Готов к работе', size_hint_y=None, halign='center')
            self.result_label.bind(texture_size=self.result_label.setter('size'))
            self.scroll.add_widget(self.result_label)
            self.layout.add_widget(self.scroll)
            return self.layout

        def check_number(self, instance):
            self.result_label.text = "Поиск... (ожидайте)"
            # Заглушка, чтобы проверить работу без падений
            self.result_label.text = "Кнопка работает!"

    if __name__ == '__main__':
        PhoneCheckerApp().run()

except Exception as e:
    # ЕСЛИ ПРОИЗОШЛА ОШИБКА, ПОКАЗЫВАЕМ ЕЕ НА ЭКРАНЕ
    error_text = traceback.format_exc()
    
    class ErrorApp(App):
        def build(self):
            layout = BoxLayout(orientation='vertical', padding=20)
            lbl = Label(text=f"ОШИБКА ЗАПУСКА:\n\n{str(e)}\n\nПроверьте логи.", halign='center', valign='middle')
            lbl.bind(size=lbl.setter('text_size'))
            layout.add_widget(lbl)
            return layout

    if __name__ == '__main__':
        ErrorApp().run()
