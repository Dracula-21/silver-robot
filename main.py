from kivy.core.window import Window
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from kivy.clock import Clock
from kivy.graphics import Color, Rectangle
import threading
import asyncio
import traceback

# Темный фон, чтобы не было черного экрана
Window.clearcolor = (0.1, 0.1, 0.1, 1)

# ВАШИ ДАННЫЕ (ВСТАВЬ СВОИ)
API_ID = 33600401  
API_HASH = 'f1ef88aa120c93c9ad95a2c246acaf17' 

try:
    from telethon import TelegramClient

    class PhoneCheckerApp(App):
        def build(self):
            # Главный контейнер
            self.layout = BoxLayout(orientation='vertical', padding=30, spacing=20)
            
            # Заголовок
            title = Label(text="Проверка номеров", font_size='24sp', size_hint_y=None, height=50)
            self.layout.add_widget(title)
            
            # Поле ввода
            self.phone_input = TextInput(
                hint_text='+998901234567', 
                multiline=False, 
                size_hint_y=None, 
                height=60,
                font_size='18sp'
            )
            self.layout.add_widget(self.phone_input)
            
            # Кнопка
            self.check_btn = Button(
                text='ПРОВЕРИТЬ', 
                size_hint_y=None, 
                height=60, 
                background_color=(0.2, 0.6, 0.8, 1)
            )
            self.check_btn.bind(on_press=self.start_check)
            self.layout.add_widget(self.check_btn)
            
            # Результат
            self.result_label = Label(
                text='Введите номер и нажмите кнопку', 
                font_size='16sp',
                halign='center',
                valign='middle'
            )
            # Чтобы текст переносился на новую строку
            self.result_label.bind(size=self.result_label.setter('text_size'))
            self.layout.add_widget(self.result_label)
            
            return self.layout

        def update_label(self, text):
            self.result_label.text = text
            self.check_btn.disabled = False # Включаем кнопку обратно

        async def _check(self, phone):
            client = TelegramClient('session', API_ID, API_HASH)
            await client.connect()
            
            if not await client.is_user_authorized():
                await client.disconnect()
                return "❌ Ошибка: Нет авторизации.\nФайл session.session не подхватился."
            
            try:
                user = await client.get_entity(phone)
                res = f"✅ Найден!\n\nИмя: {user.first_name} {user.last_name or ''}\n"
                res += f"Юзернейм: @{user.username if user.username else 'скрыт'}"
            except Exception as err:
                res = f"❌ Не найден или ошибка доступа."
            finally:
                await client.disconnect()
            return res

        def run_check(self, phone):
            # Запускаем асинхронный цикл в отдельном потоке
            try:
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
                res = loop.run_until_complete(self._check(phone))
                # Передаем строку в главный поток
                Clock.schedule_once(lambda dt: self.update_label(res), 0)
            except Exception as e:
                # Сохраняем текст ошибки в строку ДО вызова лямбды
                err_str = str(e) 
                Clock.schedule_once(lambda dt: self.update_label(f"Ошибка сети:\n{err_str}"), 0)

        def start_check(self, instance):
            phone = self.phone_input.text.strip()
            if not phone:
                self.result_label.text = "Вы не ввели номер!"
                return
            
            self.result_label.text = "Поиск в Telegram..."
            self.check_btn.disabled = True # Отключаем кнопку, чтобы не спамили
            # Запускаем поток
            threading.Thread(target=self.run_check, args=(phone,), daemon=True).start()

    if __name__ == '__main__':
        PhoneCheckerApp().run()

except Exception as e:
    # Если что-то упадет при импорте
    err_str = traceback.format_exc()
    class ErrorApp(App):
        def build(self):
            return Label(text=f"ОШИБКА ЗАПУСКА:\n{err_str}")
    if __name__ == '__main__':
        ErrorApp().run()
