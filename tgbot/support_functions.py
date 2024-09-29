import logging

from telegram import ReplyKeyboardMarkup

from .db import api_put, check_status, get_data

LOGO = '/data/logo.png'
LOGO_2 = '/data/logo_2.png'


def rename_order(id):
    data = get_data('api_order', id)
    for row in data:
        api_put(
            'api_order',
            id,
            'type',
            'разовый заказ'
        ) if row[3] == 'Мне подходит этот вариант!' else None


def get_address(user):
    data = get_data('api_address', user.id)
    for row in data:
        address = f'г. {row[0]}, {row[1]}. Дополнительно: {row[2]}'
    return address


def get_additionally(user):
    if check_status('api_address', user.id) is True:
        data = get_data('api_address', user.id)
        for row in data:
            additionally = row[2]
    else:
        additionally = 'NULL'
    return additionally


def get_profile(user):
    data = get_data('api_profile', user.id)
    for row in data:
        profile = (
            f'Аромат: {row[0]},\nГлажение: {row[1]},\nВопросы про пятна: '
            f'{row[2]},\nВопросы про происхождение пятен: {row[3]},\n'
            f'Пожелания к стирке: {row[4]},\nПожелания к доставке: {row[5]}'
        )
    return profile


def get_order(user):
    data = get_data('api_order', user.id)
    for row in data:
        order = f'{row[3]}, дата: {row[0]}, время: {row[1]}'
    return order


def finish_message(user):
    rename_order(user.id)
    if check_status('api_profile', user.id) is True:
        return (f'Доброго дня! клиент {user.first_name} {user.last_name} '
                f'(https://t.me/{user.username} / @{user.username} / '
                f'tg://user?id={user.id} )\nоформил заказ: {get_order(user)}\n'
                f'Адрес: {get_address(user)}\nАнкета: {get_profile(user)}')
    else:
        return (f'Доброго дня! клиент {user.first_name} {user.last_name} '
                f'(https://t.me/{user.username} / @{user.username} / '
                f'tg://user?id={user.id} )\nоформил заказ: {get_order(user)}\n'
                f'Адрес: {get_address(user)}\n')


def thanks_message(user):
    return (f'Доброго дня! клиент {user.first_name} {user.last_name} '
            f'(https://t.me/{user.username} / @{user.username} / '
            f'tg://user?id={user.id} )\nзаполнил/изменил анкету:\n'
            f'{get_profile(user)}')


def finish_user(user):
    return (f'Доброго дня! новый клиент {user.first_name} {user.last_name} '
            f'( https://t.me/{user.username} / @{user.username} / '
            f'tg://user?id={user.id}')


def get_image(image):
    logo = 0
    try:
        logo = open(
            image,
            'rb'
        )
    except Exception as error:
        message_error = (f'Failed open image: {error}')
        logging.error(message_error)
    return logo


async def send_message(update, text, buttons):
    await update.message.reply_text(
        text,
        reply_markup=ReplyKeyboardMarkup(
            buttons,
            one_time_keyboard=True,
            resize_keyboard=True,
            input_field_placeholder='Выбрать вариант'
        ),
    )


async def send_text_message(update, text, buttons):
    await update.message.reply_text(
        text,
        reply_markup=ReplyKeyboardMarkup(
            buttons,
            one_time_keyboard=True,
            resize_keyboard=True
        ),
    )
