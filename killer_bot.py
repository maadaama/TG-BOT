from telegram import Update
from telegram.ext import Updater
from telegram.ext import CommandHandler, ConversationHandler
from telegram.ext import MessageHandler
from telegram.ext import Filters
from telegram.ext import CallbackContext

from key import TOKEN
from connect_to_database import write_to_db, get_user_from_db

GRADES = (
    '8н', '8о', '8п', '8Н', '8О', '8П',
    '9н', '9о', '9п', '9Н', '9О', '9П',
    '10н', '10Н', '10но', '10НО',
    '11н', '11Н', '11о', '11О'
)

WAIT_FOR_CLASS, WAIT_FOR_NAME, WAIT_FOR_PHOTO = range(3)


def main():
    """
    Конфигурирует и запускает бот
    """
    # Updater - объект, который ловит обновления и Телеграм
    updater = Updater(token=TOKEN)

    # Диспетчер будет распределять события по обработчикам
    dispatcher = updater.dispatcher


    # Добавляем обработчик события из Телеграма
    dispatcher.add_handler(CommandHandler('start', do_start))

    dispatcher.add_handler(
        ConversationHandler(
            entry_points=[CommandHandler('register', ask_for_class), ],  # Точки старта диалого
            states={
                WAIT_FOR_CLASS: [MessageHandler(Filters.text, get_class)],
                WAIT_FOR_NAME: [MessageHandler(Filters.text, get_name)],
                WAIT_FOR_PHOTO: [MessageHandler(Filters.text, get_photo)],
            },  # Состояние
            fallbacks=[]  # Отлов ошибок
        )
    )

    dispatcher.add_handler(MessageHandler(Filters.text, do_help))

    # Все обработчики надо добавить До этого места
    # Начать бесконечный опрос телеграма на предмет обновлений
    updater.start_polling()
    print(updater.bot.getMe())
    print('Бот запущен')
    updater.idle()


def do_help(update: Update, context: CallbackContext):
    text = [
        'Привет!',
        'Я помогу тебе зарегистрироваться',
        'Для этого нажми на /register',

    ]
    text = '\n'.join(text)  # собираем строки в текст через разделитель "перевод строки"
    update.message.reply_text(text)


def do_start(update: Update, context: CallbackContext):
    print('Ура! Ко мне обратились!')
    text = [
        'Привет, человек! Тебя приветствует искуственный разум!',
        'Для начала нажми на /register',
    ]
    text = '\n'.join(text)
    update.message.reply_text(text)



def ask_for_class(update: Update, context: CallbackContext):
    user = get_user_from_db(update.message.from_user.id)
    if user:
        lines = [
            f'Ты уже зарегистрирован по именем {user["name"]}',
            f'в классе {user["class"]}',
        ]

        text = '\n'.join(lines)
        update.message.reply_text(text)

        return ConversationHandler.END

    lines = [
        'Введите номер и букву своего класса',
        'Пример: 10н'
    ]
    text = '\n'.join(lines)
    update.message.reply_text(text)

    return WAIT_FOR_CLASS


def ask_for_name(update: Update, context: CallbackContext):
    text = 'Введите своё имя'
    update.message.reply_text(text)
    return WAIT_FOR_NAME


def ask_for_photo(update: Update, context: CallbackContext):
    text = 'Прикрепите свое фото.'
    update.message.reply_text(text)
    return WAIT_FOR_PHOTO


def get_class(update: Update, context: CallbackContext):
    grade = update.message.text
    # можно вывести содержимое переменной grade, чтобы понять, что туда попало
    if grade not in GRADES:
        'В списке участников нет такого класса!'
        lines = [
            f'В списке участников нет такого класса!',
            'Попробуйте еще раз!',
        ]
        text = '\n'.join(lines)
        update.message.reply_text(text)

        return ask_for_class(update, context)
    else:
        context.user_data['class'] = grade
        text = f'Я запомнил Ваш класс: {grade}'
        update.message.reply_text(text)

        return ask_for_name(update, context)


def get_name(update: Update, context: CallbackContext):
    name = update.message.text
    context.user_data['name'] = name
    text = f'Я запомнил Ваше имя: {name}'
    update.message.reply_text(text)

    return ask_for_photo(update, context)


def get_photo(update: Update, context: CallbackContext):
    photo = update.message.text
    context.user_data['photo'] = photo
    text = f'Я загрузил Ваше фото: {photo}'
    update.message.reply_text(text)

    return register_player(update, context)


def register_player(update: Update, context: CallbackContext):
    user_id = update.message.from_user.id
    grade = context.user_data["class"]
    name = context.user_data["name"]
    photo = context.user_data["photo"]

    write_to_db(user_id, grade, name, photo)

    lines = [
        'Вы зарегистрированы!',
        f'Вы учитесь в классе: {context.user_data["class"]}',
        f'Вас зовут: {context.user_data["name"]}',
        f'Ваше фото: {context.user_data["photo"]}'
    ]
    text = '\n'.join(lines)
    update.message.reply_text(text)

    return ConversationHandler.END


if __name__ == '__main__':
    main()