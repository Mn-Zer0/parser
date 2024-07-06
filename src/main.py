from database import add_job_search_to_db, init_db, check_if_url_exists
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, filters, ConversationHandler, CallbackContext, Application
from parser import get_vacancies
import os
from dotenv import load_dotenv


load_dotenv()
# Определение состояний диалога
CITY, JOB, MIN_SALARY, MAX_SALARY = range(4)
BOT_TOKEN = os.getenv('BOT_TOKEN')
print(BOT_TOKEN)


# Функция для обработки команды /start
async def start(update, context):
    await update.message.reply_text('Привет! В каком городе вы ищете работу?')
    return CITY


# Функция для обработки города
async def city(update, context):
    user_data = context.user_data
    user_data['city'] = update.message.text
    await update.message.reply_text('Какая у вас вакансия?')
    return JOB


# Функция для обработки вакансии
async def job(update, context):
    user_data = context.user_data
    user_data['job'] = update.message.text
    await update.message.reply_text('Какая минимальная оплата?')
    return MIN_SALARY


# Функция для обработки минимальной оплаты
async def min_salary(update, context):
    user_data = context.user_data
    user_data['min_salary'] = update.message.text
    await update.message.reply_text('Какая максимальная оплата?')
    return MAX_SALARY


# Функция для обработки команды /cancel
async def cancel(update, context):
    await update.message.reply_text('Отмена. Для начала поиска введите /start.')
    return ConversationHandler.END


# Функция для обработки максимальной оплаты с добавлением записи в базу данных
async def max_salary(update: Update, context: CallbackContext):
    user_data = context.user_data
    user_data['max_salary'] = update.message.text
    # Добавляем информацию в базу данных
    # add_job_search_to_db(user_data['city'], user_data['job'], user_data['min_salary'], user_data['max_salary'])

    # Получаем вакансии
    vacancies = await get_vacancies(user_data['job'], user_data['city'])

    # Выводим информацию
    await update.message.reply_text(f"Ищем вакансии в городе {user_data['city']} на должность {user_data['job']} "
                              f"с оплатой от {user_data['min_salary']} до {user_data['max_salary']}.")
    await display_vacancies(update, vacancies, user_data['city'], user_data['job'], user_data['min_salary'], user_data['max_salary'])
    return ConversationHandler.END


async def display_vacancies(update: Update, vacancies, city, job_title, min_salary, max_salary):
    for vacancy in vacancies:
        title = vacancy.get('name')
        url = vacancy.get('alternate_url')

        # Проверяем, существует ли уже такая ссылка в базе данных
        if not check_if_url_exists(url):
            # Если ссылка не найдена, добавляем информацию в базу данных
            add_job_search_to_db(city, job_title, min_salary, max_salary, url)
            await update.message.reply_text(f"{title}: {url}")
        else:
            # Если ссылка найдена, пропускаем добавление
            continue

        await update.message.reply_text(f"{title}: {url}")


def main():
    # Создание экземпляра приложения с помощью Application.builder
    application = Application.builder().token(BOT_TOKEN).build()

    # Определение обработчика диалога
    conversation_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            CITY: [MessageHandler(filters.TEXT & ~filters.COMMAND, city)],
            JOB: [MessageHandler(filters.TEXT & ~filters.COMMAND, job)],
            MIN_SALARY: [MessageHandler(filters.TEXT & ~filters.COMMAND, min_salary)],
            MAX_SALARY: [MessageHandler(filters.TEXT & ~filters.COMMAND, max_salary)]
        },
        fallbacks=[CommandHandler('cancel', cancel)]
    )
    # Добавление обработчика диалога в приложение
    application.add_handler(conversation_handler)
    application.run_polling()


if __name__ == '__main__':
    init_db()  # Инициализируем базу данных при запуске бота
    main()
