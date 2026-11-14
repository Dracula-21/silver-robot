from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from kivy.clock import Clock
import threading
import asyncio

# ВАШИ ДАННЫЕ
API_ID = 33600401  # <-- ВСТАВЬ СВОЙ API_ID
API_HASH = 'f1ef88aa120c93c9ad95a2c246acaf17' # <-- ВСТАВЬ СВОЙ API_HASH

try:
    from telethon import TelegramClient

    class PhoneCheckerApp(App):
        def build(self):
            layout = BoxLayout(orientation='vertical', padding=20, spacing=10)
            
            self.phone_input = TextInput(hint_text='Введите номер (+998...)', multiline=False, size_hint_y=None, height=50)
            layout.add_widget(self.phone_input)
            
            self.check_btn = Button(text='Проверить', size_hint_y=None, height=50)
            self.check_btn.bind(on_press=self.start_check)
            layout.add_widget(self.check_btn)
            
            self.result_label = Label(text='Введите номер и нажмите Проверить')
            layout.add_widget(self.result_label)
            
            return layout

        def update_label(self, text):
            self.result_label.text = text

        async def _check(self, phone):
            # Приложение найдет файл session.session, который мы загрузили
            client = TelegramClient('session', API_ID, API_HASH)
            await client.connect()
            
            if not await client.is_user_authorized():
                await client.disconnect()
                return "Ошибка: Нет авторизации. Файл session.session не подхватился."
            
            try:
                user = await client.get_entity(phone)
                res = f"✅ Найден:\nИмя: {user.first_name} {user.last_name or ''}\n"
                res += f"Юзернейм: @{user.username if user.username else 'скрыт'}"
            except Exception as e:
                res = f"❌ Не найден или ошибка"
            await client.disconnect()
            return res

        def run_check(self, phone):
            try:
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
                res = loop.run_until_complete(self._check(phone))
                Clock.schedule_once(lambda dt: self.update_label(res), 0)
            except Exception as e:
                Clock.schedule_once(lambda dt: self.update_label(f"Ошибка: {e}"), 0)

        def start_check(self, instance):
            phone = self.phone_input.text
            if not phone:
                self.result_label.text = "Введите номер!"
                return
            self.result_label.text = "Поиск..."
            threading.Thread(target=self.run_check, args=(phone,), daemon=True).start()

    if __name__ == '__main__':
        PhoneCheckerApp().run()

except Exception as e:
    class ErrorApp(App):
        def build(self):
            return Label(text=f"ОШИБКА ЗАПУСКА:\n{e}")
    if __name__ == '__main__':
        ErrorApp().run()
