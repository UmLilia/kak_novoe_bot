import os
from datetime import date

from telegram import ReplyKeyboardMarkup, Update
from telegram.ext import ContextTypes

from . import telegramcalendar
from .buttons import (ABOUT_US_BUTTONS, AROMA_BUTTONS, BASKET_BUTTONS,
                      CARE_SET_BUTTONS, CITIES_BUTTONS, IRONING_BUTTONS,
                      MAIN_BUTTONS, PREV_BUTTONS, PREV_NEXT_BUTTONS,
                      PRICES_BUTTONS, RETURN_MENU_BUTTONS,
                      SUBSCRIPTIONS_BUTTONS, TIME_BUTTONS, YES_NO_BUTTONS)
from .db import api_put, check_status, check_user, write_data
from .manager import send_manager_message
from .messanges import (ABOUT_TEXT, ADDRESS_TEXT, AGREE_DATA_TEXT, AROMA_TEXT,
                        BASKET_TEXT, CARE_SET_TEXT, FINISH_ORDER_TEXT,
                        GREETING_TEXT, HISTORY_TEXT, IRONING_TEXT,
                        MANAGER_CARE_SET_TEXT, MANAGER_STATUS_TEXT,
                        MANAGER_TEXT, ORDER_AGREE_TEXT, ORDER_TEXT,
                        PRICES_TEXT, SOME_TEXT, SPOTS_TEXT, THANKS_TEXT,
                        TIME_TEXT, WISHES_DELIVERY_TEXT, WISHES_TEXT,
                        MANAGER_REPLY_TEXT)
from .support_functions import (LOGO, LOGO_2, finish_message, finish_user,
                                get_additionally, get_image, send_message,
                                send_text_message, thanks_message)

TOKEN = os.environ['TOKEN']

ID_MANAGER = os.environ['ID_MANAGER']

(MAIN_MENU, PROFILE, IRONING, SPOTS, HISTORY, WISHES, DELIVERY, ADDRESS,
 DONE_ADDRESS) = range(9)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_photo(photo=get_image(LOGO))
    await send_message(update, GREETING_TEXT, MAIN_BUTTONS)
    return MAIN_MENU


async def wake_up(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await send_message(update, SOME_TEXT, MAIN_BUTTONS)
    return MAIN_MENU


async def basket(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await send_message(
        update,
        BASKET_TEXT,
        BASKET_BUTTONS
    )
    return MAIN_MENU


async def about_us(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_photo(photo=get_image(LOGO_2))
    await send_message(update, ABOUT_TEXT, ABOUT_US_BUTTONS)
    return MAIN_MENU


async def price(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await send_message(update, PRICES_TEXT, PRICES_BUTTONS)
    return MAIN_MENU


async def manager(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = update.message
    user = message.from_user
    text = message.text
    await context.bot.send_message(
            chat_id=ID_MANAGER,
            text=(f'{user.first_name} {user.last_name} (https://t.me/'
                  f'{user.username}/ @{user.username} / tg://user?id={user.id}'
                  f' : {text}')
        )
    if 'В списке нет моего города' == text:
        await send_message(
            update,
            ('Сейчас что-нибудь придумаем! Ваш персональный менеджер уже '
             'пишет вам в чате @knovoe. Ждем вас там 🌱'),
            RETURN_MENU_BUTTONS
        )
        await send_manager_message(
            user,
            (f'Здравствуйте, {user.first_name}!\n\nНа связи Лиза, ваш '
             'персональный менеджер.\n\nНапишите, пожалуйста, ваш адрес '
             '(включая город) и мы подумаем, как организовать приезд курьера к'
             ' вам.')
        )
    elif 'Отследить мой заказ' == text:
        await send_message(
            update,
            ('Ваш персональный менеджер уже актуализирует статус вашего '
             'заказа. Он скоро напишет вам в чате @knovoe 🌱'),
            RETURN_MENU_BUTTONS
        )
        await send_manager_message(
            user,
            f'Здравствуйте, {user.first_name}!\n\n{MANAGER_STATUS_TEXT}'
        )
    elif 'Получить набор заботы' == text:
        await send_message(
            update,
            MANAGER_REPLY_TEXT,
            RETURN_MENU_BUTTONS
        )
        await send_manager_message(
            user,
            f'Здравствуйте, {user.first_name}!\n\n{MANAGER_CARE_SET_TEXT}'
        )
    elif 'Мне нужна помощь персонального менеджера' == text:
        await send_message(
            update,
            ('Ваш персональный менеджер уже пишет вам в чате @knovoe. '
             'Ждем вас там 🌱'),
            RETURN_MENU_BUTTONS
        )
        await send_manager_message(
            user,
            (f'Здравствуйте, {user.first_name}!\n\nНа связи Лиза, ваш '
             'персональный менеджер.\n\nЯ с радостью помогу вам '
             'разобраться в нашем сервисе 🧼\n\nПросто напишите 🌱')
        )
    else:
        await send_message(
            update,
            ('Ваш персональный менеджер уже пишет вам в чате @knovoe. '
             'Ждем вас там 🌱'),
            RETURN_MENU_BUTTONS
        )
        await send_manager_message(
            user,
            f'Здравствуйте, {user.first_name}! {MANAGER_TEXT}'
        )
    return MAIN_MENU


async def care_set(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_photo(photo=get_image(LOGO_2))
    await send_message(update, CARE_SET_TEXT, CARE_SET_BUTTONS)
    return MAIN_MENU


async def aroma(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user = update.message.from_user
    if check_status('api_users', user.id) is not True:
        await send_message(update, AGREE_DATA_TEXT, AROMA_BUTTONS)
        check_user(user)
        text = finish_user(user)
        await context.bot.send_message(
            chat_id=ID_MANAGER,
            text=text
        )
    await send_message(update, AROMA_TEXT, AROMA_BUTTONS)
    return PROFILE


async def ironing(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user = update.message.from_user
    write_data('api_profile', user.id, 'aroma', update.message.text)
    await send_message(update, IRONING_TEXT, IRONING_BUTTONS)
    return IRONING


async def spots(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user = update.message.from_user
    api_put('api_profile', user.id, 'ironing', update.message.text)
    await send_message(update, SPOTS_TEXT, YES_NO_BUTTONS)
    return SPOTS


async def history(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user = update.message.from_user
    api_put('api_profile', user.id, 'spots', update.message.text)
    await send_message(update, HISTORY_TEXT, YES_NO_BUTTONS)
    return HISTORY


async def wishes(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user = update.message.from_user
    api_put('api_profile', user.id, 'history', update.message.text)
    await send_text_message(update, WISHES_TEXT, PREV_NEXT_BUTTONS)
    return WISHES


async def wishes_delivery(
        update: Update,
        context: ContextTypes.DEFAULT_TYPE) -> int:
    user = update.message.from_user
    api_put('api_profile', user.id, 'wishes', update.message.text)
    await send_text_message(update, WISHES_DELIVERY_TEXT, PREV_NEXT_BUTTONS)
    return DELIVERY


async def thanks(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user = update.message.from_user
    api_put('api_profile', user.id, 'delivery', update.message.text)
    await send_message(update, THANKS_TEXT, RETURN_MENU_BUTTONS)
    await context.bot.send_message(
            chat_id=ID_MANAGER,
            text=thanks_message(user)
        )
    return MAIN_MENU


async def conditions(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await send_message(
        update,
        ORDER_TEXT,
        PREV_BUTTONS
    )
    return MAIN_MENU


async def order_agree(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = update.message.text
    user = update.message.from_user
    address = get_additionally(user)
    check_user(user)
    write_data('api_order', user.id, 'type', message)
    if check_status('api_address', user.id) is True and address is not None:
        await order_date(update, context)
    else:
        await send_message(update, ORDER_AGREE_TEXT, CITIES_BUTTONS)
        return MAIN_MENU


async def address(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.message.from_user
    write_data('api_address', user.id, 'city', update.message.text)
    await context.bot.send_message(
            chat_id=ID_MANAGER,
            text=finish_user(user)
        )
    await send_text_message(update, ADDRESS_TEXT, PREV_NEXT_BUTTONS)
    return ADDRESS


async def additionally(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.message.from_user
    api_put('api_address', user.id, 'address', update.message.text)
    await send_text_message(
        update,
        ('Хотите ли вы что-то добавить, '
         'чтобы курьер быстрее нашел вас?'),
        PREV_NEXT_BUTTONS
    )
    return DONE_ADDRESS


async def write_additionally(
        update: Update,
        context: ContextTypes.DEFAULT_TYPE):
    user = update.message.from_user
    api_put('api_address', user.id, 'additionally', update.message.text)
    await order_date(update, context)


async def subscription_order(
        update: Update,
        context: ContextTypes.DEFAULT_TYPE):
    await send_message(
        update,
        'Выберите, пожалуйста, подходящий вам абонемент',
        SUBSCRIPTIONS_BUTTONS
    )
    return MAIN_MENU


async def order_date(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await send_message(
        update,
        SOME_TEXT,
        PREV_BUTTONS
    )
    await update.message.reply_text(
        'В какой день вам удобно было бы встретить курьера?',
        reply_markup=telegramcalendar.create_calendar()
    )
    return MAIN_MENU


async def time(update: Update, context: ContextTypes.DEFAULT_TYPE):
    selected, my_date = await telegramcalendar.process_calendar_selection(
        update,
        context
    )
    if selected and my_date.date() >= date.today():
        api_put(
            'api_order',
            update.effective_chat.id,
            'date',
            my_date.strftime("%d/%m/%Y")
        )
        await context.bot.send_message(
            chat_id=update.callback_query.from_user.id,
            text=f'Вы выбрали {my_date.strftime("%d/%m/%Y")}',
            reply_markup=ReplyKeyboardMarkup(
                TIME_BUTTONS, one_time_keyboard=True, resize_keyboard=True
            )
        )
        await context.bot.send_message(
            chat_id=update.callback_query.from_user.id,
            text=TIME_TEXT,
            reply_markup=ReplyKeyboardMarkup(
                TIME_BUTTONS, one_time_keyboard=True, resize_keyboard=True
            )
        )
        return MAIN_MENU
    elif my_date.date() < date.today():
        await context.bot.send_message(
            chat_id=update.callback_query.from_user.id,
            text='Пожалуйста, выберите дату не ранее сегодняшнего дня',
            reply_markup=telegramcalendar.create_calendar()
        )
        return MAIN_MENU


async def finish_order(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.message.from_user
    api_put('api_order', user.id, 'time', update.message.text)
    text = f'Отлично, {user.first_name}! {FINISH_ORDER_TEXT}'
    await send_message(update, text, RETURN_MENU_BUTTONS)
    await context.bot.send_message(
            chat_id=ID_MANAGER,
            text=finish_message(user)
        )
    return MAIN_MENU
