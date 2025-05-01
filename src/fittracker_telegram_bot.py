import os
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, ContextTypes, filters
from bot_config import BOT_TOKEN
from database import Database
from workout_plan import WorkoutPlan
from datetime import datetime, timedelta

# Настройка логирования
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO,
    filename=os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "fittracker.log")
)
logger = logging.getLogger(__name__)

# Локализация
TRANSLATIONS = {
    'ru': {
        'welcome': 'Привет, {}! 👋 Добро пожаловать в FitTracker Pro! 💪 Выбери действие:',
        'select_action': 'Выбери действие:',
        'add_user': 'Добавить пользователя 🧑',
        'start_cycle': 'Начать цикл 🔄',
        'current_workout': 'Текущая тренировка 📋',
        'complete_workout': 'Завершить тренировку 🏋️‍♂️',
        'view_history': 'Посмотреть историю 📅',
        'change_language': 'Смена языка 🌐',
        'user_added': 'Пользователь {} добавлен! 🧑',
        'cycle_started': 'Цикл ({}-дневный сплит) начат! 🔄',
        'workout_completed': 'Тренировка завершена! 💪',
        'history_empty': 'История пуста.',
        'select_cycle': 'Выбери тип цикла:',
        'language_changed': 'Язык изменен на {}.',
        'enter_user_name': 'Введите имя нового пользователя:',
        'no_user': 'Сначала зарегистрируйся с помощью /start.'
    },
    'en': {
        'welcome': 'Hello, {}! 👋 Welcome to FitTracker Pro! 💪 Choose an action:',
        'select_action': 'Choose an action:',
        'add_user': 'Add user 🧑',
        'start_cycle': 'Start cycle 🔄',
        'current_workout': 'Current workout 📋',
        'complete_workout': 'Complete workout 🏋️‍♂️',
        'view_history': 'View history 📅',
        'change_language': 'Change language 🌐',
        'user_added': 'User {} added! 🧑',
        'cycle_started': 'Cycle ({} split) started! 🔄',
        'workout_completed': 'Workout completed! 💪',
        'history_empty': 'History is empty.',
        'select_cycle': 'Choose cycle type:',
        'language_changed': 'Language changed to {}.',
        'enter_user_name': 'Enter the new user name:',
        'no_user': 'Register first using /start.'
    }
}

def get_text(key, lang='ru'):
    return TRANSLATIONS.get(lang, TRANSLATIONS['ru']).get(key, key)

# Инициализация базы данных
db_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "data", "workouts.db")
db = Database(db_path)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.message.from_user
    name = user.first_name
    telegram_id = user.id
    try:
        db.add_user(name, telegram_id)
        context.user_data['language'] = 'ru'
        keyboard = [
            [InlineKeyboardButton(get_text('add_user', 'ru'), callback_data='add_user')],
            [InlineKeyboardButton(get_text('start_cycle', 'ru'), callback_data='start_cycle')],
            [InlineKeyboardButton(get_text('complete_workout', 'ru'), callback_data='complete_workout')],
            [InlineKeyboardButton(get_text('view_history', 'ru'), callback_data='view_history')],
            [InlineKeyboardButton(get_text('current_workout', 'ru'), callback_data='current_workout')],
            [InlineKeyboardButton(get_text('change_language', 'ru'), callback_data='change_language')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await update.message.reply_text(
            get_text('welcome', 'ru').format(name),
            reply_markup=reply_markup,
            parse_mode='Markdown'
        )
    except Exception as e:
        logger.error(f"Error in start: {e}")
        await update.message.reply_text("Произошла ошибка. Пожалуйста, попробуйте еще раз.")

async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    user_id = db.get_user_id(query.from_user.id)
    lang = context.user_data.get('language', 'ru')

    if not user_id:
        await query.message.reply_text(get_text('no_user', lang), parse_mode='Markdown')
        return

    try:
        if query.data == 'add_user':
            await query.message.reply_text(get_text('enter_user_name', lang), parse_mode='Markdown')
            context.user_data['awaiting_user_name'] = True
        elif query.data == 'start_cycle':
            keyboard = [
                [InlineKeyboardButton("5-дневный сплит" if lang == 'ru' else "5-day split", callback_data='cycle_5')],
                [InlineKeyboardButton("3-дневный сплит" if lang == 'ru' else "3-day split", callback_data='cycle_3')]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            await query.message.reply_text(get_text('select_cycle', lang), reply_markup=reply_markup, parse_mode='Markdown')
        elif query.data == 'complete_workout':
            plan = WorkoutPlan(8, 1, 5)  # По умолчанию 8 недель, 5-дневный сплит
            plan.complete_workout(db, user_id)
            await query.message.reply_text(get_text('workout_completed', lang), parse_mode='Markdown')
        elif query.data == 'view_history':
            workouts = db.get_workouts(user_id)
            if workouts:
                history = "\n".join(
                    [f"📅 {w['date']}: *{w['exercise']}* - {w['sets']} подходов, {w['reps']}, {w['weight']} кг"
                     for w in workouts])
                await query.message.reply_text(history, parse_mode='Markdown')
            else:
                await query.message.reply_text(get_text('history_empty', lang), parse_mode='Markdown')
        elif query.data == 'current_workout':
            plan = WorkoutPlan(8, 1, 5)
            workouts = plan.get_workouts(user_id, db)
            table = f"*📋 {get_text('current_workout', lang)}*:\n" + "\n".join(
                [f"🏋️ *{w['exercise']}*: {w['sets']} подходов, {w['reps']}, {w['suggested_weight']} кг"
                 for w in workouts]
            )
            # Добавляем кнопку для Web App (заглушка, требует хостинга)
            keyboard = [[InlineKeyboardButton("Открыть таблицу 📊", web_app=WebAppInfo(url="https://your-web-app-url"))]]
            reply_markup = InlineKeyboardMarkup(keyboard)
            await query.message.reply_text(table, reply_markup=reply_markup, parse_mode='Markdown')
        elif query.data == 'change_language':
            keyboard = [
                [InlineKeyboardButton("Русский 🇷🇺", callback_data='lang_ru')],
                [InlineKeyboardButton("English 🇬🇧", callback_data='lang_en')]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            await query.message.reply_text("Выберите язык / Choose language:", reply_markup=reply_markup,
                                           parse_mode='Markdown')
        elif query.data.startswith('cycle_'):
            days = 5 if query.data == 'cycle_5' else 3
            plan = WorkoutPlan(8, 1, days)
            plan.start_cycle(db, user_id)
            await query.message.reply_text(
                get_text('cycle_started', lang).format(f"{days}-дневный сплит" if lang == 'ru' else f"{days}-day split"),
                parse_mode='Markdown')
        elif query.data.startswith('lang_'):
            lang = query.data.split('_')[1]
            context.user_data['language'] = lang
            await query.message.reply_text(
                get_text('language_changed', lang).format('Русский' if lang == 'ru' else 'English'), parse_mode='Markdown')
    except Exception as e:
        logger.error(f"Error in button_callback: {e}")
        await query.message.reply_text("Произошла ошибка. Пожалуйста, попробуйте еще раз.")

async def message_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if context.user_data.get('awaiting_user_name'):
        name = update.message.text.strip()
        telegram_id = update.effective_user.id
        try:
            db.add_user(name, telegram_id)
            context.user_data['awaiting_user_name'] = False
            lang = context.user_data.get('language', 'ru')
            await update.message.reply_text(get_text('user_added', lang).format(name), parse_mode='Markdown')
        except Exception as e:
            logger.error(f"Error in message_handler: {e}")
            await update.message.reply_text("Произошла ошибка. Пожалуйста, попробуйте еще раз.")
    else:
        await update.message.reply_text("Используйте /start для начала.", parse_mode='Markdown')

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    lang = context.user_data.get('language', 'ru')
    await update.message.reply_text(
        f"🧠 *{get_text('select_action', lang)}*:\n"
        "/start — Начать\n"
        "/help — Справка\n"
        "Выберите действие через кнопки ниже:",
        parse_mode='Markdown'
    )

async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    logger.error(f"Update {update} caused error {context.error}")
    if update and update.message:
        await update.message.reply_text("Произошла ошибка. Пожалуйста, попробуйте еще раз.")

def main():
    application = Application.builder().token(BOT_TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CallbackQueryHandler(button_callback))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, message_handler))
    application.add_error_handler(error_handler)
    application.run_polling()

if __name__ == "__main__":
    main()