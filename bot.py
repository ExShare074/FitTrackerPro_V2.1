import logging
from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

from main.modules.utils.workout_generator import get_today_workout
from main.modules.utils.training_cycle import start_new_cycle, check_active_cycle


API_TOKEN = '7272100287:AAHs4MtOusnAKO6QhgFOqZ0CmSZVx4zxsQ8'

logging.basicConfig(level=logging.INFO)
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

# Кнопки
start_cycle_btn = KeyboardButton('Старт нового цикла')
today_workout_btn = KeyboardButton('Сегодняшняя тренировка')
menu = ReplyKeyboardMarkup(resize_keyboard=True).add(start_cycle_btn, today_workout_btn)

@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    await message.answer("Привет! Я бот FitTrackerPro 💪\nЧто хочешь сделать?", reply_markup=menu)

@dp.message_handler(lambda message: message.text == 'Старт нового цикла')
async def handle_start_cycle(message: types.Message):
    start_new_cycle()
    await message.answer("✅ Новый тренировочный цикл запущен!")

@dp.message_handler(lambda message: message.text == 'Сегодняшняя тренировка')
async def handle_today_workout(message: types.Message):
    if not check_active_cycle():
        await message.answer("⛔ Нет активного цикла. Сначала запусти его.")
        return
    workout = get_today_workout()
    formatted = "\n".join(f"{w['name']} — {w['sets']}×{w['reps']}" for w in workout)
    await message.answer(f"📅 Сегодняшняя тренировка:\n\n{formatted}")

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
