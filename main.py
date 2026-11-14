from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.clock import Clock
import threading
import traceback
import asyncio

# ВАШИ ДАННЫЕ (ОБЯЗАТЕЛЬНО ЗАМЕНИ)
API_ID = 33600401  
API_HASH = 'f1ef88aa120c93c9ad95a2c246acaf17' 

try:
    from telethon import TelegramClient

    class PhoneCheckerApp(App):
        def build(self):
            self.layout = BoxLayout(orientation='vertical', padding=20, spacing=10)
            
            self.phone_input = TextInput(hint_text='Введите номер (+998...)', multiline=False, size_hint_y=None, height=50)
            self.layout.add_widget(self.phone_input)
            
            self.check_btn = Button(text='Проверить', size_hint_y=None, height=50)
            self.check_btn.bind(on_press=self.start_check)
            self.layout.add_widget(self.check_btn)
            
            self.scroll = ScrollView()
            self.result_label = Label(text='Введите номер и нажмите Проверить', size_hint_y=None, halign='center')
            self.result_label.bind(texture_size=self.result_label.setter('size'))
            self.scroll.add_widget(self.result_label)
            self.layout.add_widget(self.scroll)
            
            return self.layout

        def update_label(self, text):
            # Обновляем текст безопасно из другого потока
            self.result_label.text = text

        async def _check(self, phone):
            # Создаем клиент. Он сам создаст файл session.session при первом запуске.
            client = TelegramClient('session', API_ID, API_HASH)
            await client.connect()
            
            if not await client.is_user_authorized():
                await client.disconnect()
                return "Ошибка: Нет авторизации. Сначала зайдите в Telegram."
            
            try:
                user = await client.get_entity(phone)
                res = f"✅ Найден:\nИмя: {user.first_name} {user.last_name or ''}\n"
                res += f"Юзернейм: @{user.username if user.username else 'скрыт'}\n"
                res += f"ID: {user.id}"
            except Exception as e:
                res = f"❌ Не найден или ошибка:\n{str(e)}"
            await client.disconnect()
            return res

        def run_telegram_check(self, phone):
            try:
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
                res = loop.run_until_complete(self._check(phone))
                Clock.schedule_once(lambda dt: self.update_label(res), 0)
            except Exception as e:
                error_msg = f"Ошибка потока: {e}"
                Clock.schedule_once(lambda dt: self.update_label(error_msg), 0)

        def start_check(self, instance):
            phone = self.phone_input.text
            if not phone:
                self.result_label.text = "Введите номер!"
                return
            
            self.result_label.text = "Поиск в Telegram (ожидайте)..."
            # Запускаем проверку в отдельном потоке, чтобы не было черного экрана
            threading.Thread(target=self.run_telegram_check, args=(phone,), daemon=True).start()

    if __name__ == '__main__':
        PhoneCheckerApp().run()

except Exception as e:
    # Экран на случай, если библиотека не загрузится
    error_text = traceback.format_exc()
    class ErrorApp(App):
        def build(self):
            layout = BoxLayout(orientation='vertical', padding=20)
            lbl = Label(text=f"ОШИБКА ЗАПУСКА:\n\n{str(e)}", halign='center', valign='middle')
            lbl.bind(size=lbl.setter('text_size'))
            layout.add_widget(lbl)
            return layout
    if __name__ == '__main__':
        ErrorApp().run()
