import logging
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackQueryHandler
from telegram import Update
from telegram.ext import (
    ApplicationBuilder, CommandHandler, ContextTypes,
    ConversationHandler
)

# Настройка логирования
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# Хранилище пользовательского состояния
user_states = {}

# Команда /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    user_states[user.id] = {"stage": "start"}
    await update.message.reply_text(
        f"Привет, {user.first_name}! 👋 Добро пожаловать в FitTracker Pro (Telegram Edition)!\n"
        "Для начала работы напиши /help или выбери тренировку."
    )

# Команда /help
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🧠 Доступные команды:\n"
        "/start — Перезапуск\n"
        "/help — Справка\n"
        "Скоро здесь появится выбор программы, просмотр прогресса и упражнения с GIF 💪"
    )
# Команда /program
async def choose_program(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [
            InlineKeyboardButton("🏁 8 недель", callback_data="program_8"),
            InlineKeyboardButton("🏁 10 недель", callback_data="program_10"),
            InlineKeyboardButton("🏁 12 недель", callback_data="program_12")
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("Выбери продолжительность программы:", reply_markup=reply_markup)

# Обработка выбора программы
async def program_selected(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    weeks = int(query.data.split("_")[1])
    user_id = query.from_user.id
    user_states[user_id]["program_weeks"] = weeks
    user_states[user_id]["current_week"] = 1
    user_states[user_id]["progress"] = 0

    await query.edit_message_text(f"✅ Программа на {weeks} недель выбрана. Начинаем с недели 1!")

# Заглушка: упражнения на 1 день
daily_workout = {
    "Push-ups": "https://media.giphy.com/media/XE7Wfij2a7gQbnk16T/giphy.gif",
    "Squats": "https://media.giphy.com/media/l41YxQs5NqvZTmWLu/giphy.gif",
    "Plank": "https://media.giphy.com/media/l0MYB8Ory7Hqefo9a/giphy.gif"
}

# Команда /today — показать текущий день
async def show_today(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if user_id not in user_states or "program_weeks" not in user_states[user_id]:
        await update.message.reply_text("❗️Сначала выбери программу через /program.")
        return

    keyboard = [[InlineKeyboardButton(name, callback_data=f"exercise_{name}")] for name in daily_workout.keys()]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("📅 Упражнения на сегодня:", reply_markup=reply_markup)

# Обработка выбора упражнения — отправка GIF
async def send_exercise_gif(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    exercise_name = query.data.split("_", 1)[1]
    gif_url = daily_workout.get(exercise_name)

    if gif_url:
        await context.bot.send_animation(chat_id=query.message.chat.id, animation=gif_url, caption=f"🏋️‍♂️ {exercise_name}")
    else:
        await context.bot.send_message(chat_id=query.message.chat.id, text="GIF для этого упражнения пока нет.")

# Запуск бота
def main():

    application = ApplicationBuilder().token("7272100287:AAHs4MtOusnAKO6QhgFOqZ0CmSZVx4zxsQ8").build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("program", choose_program))
    application.add_handler(CommandHandler("today", show_today))

    application.add_handler(CallbackQueryHandler(program_selected, pattern=r"^program_\d+$"))
    application.add_handler(CallbackQueryHandler(send_exercise_gif, pattern=r"^exercise_"))

    application.run_polling()

if __name__ == "__main__":
    main()
