import calendar
import datetime

from telegram import (InlineKeyboardButton, InlineKeyboardMarkup)

MONTHS = {
    'January': 'Январь',
    'February': 'Февраль',
    'March': 'Март',
    'April': 'Апрель',
    'May': 'Май',
    'June': 'Июнь',
    'July': 'Июль',
    'August': 'Август',
    'September': 'Сентябрь',
    'October': 'Октябрь',
    'November': 'Ноябрь',
    'December': 'Декабрь'
}


def create_callback_data(action, year, month, day):
    """ Create the callback data associated to each button"""
    return ";".join([action, str(year), str(month), str(day)])


def separate_callback_data(data):
    print(data)
    """ Separate the callback data"""
    return data.split(";")


def create_calendar(year=None, month=None, day=None):
    """
    Create an inline keyboard with the provided year and month
    :param int year: Year to use in the calendar, if None the current year is
    used.
    :param int month: Month to use in the calendar, if None the current month
    is used.
    :return: Returns the InlineKeyboardMarkup object with the calendar.
    """
    now = datetime.datetime.now()
    if year is None:
        year = now.year
    if month is None:
        month = now.month
    if day is None:
        day = now.day
    data_ignore = create_callback_data("IGNORE", year, month, day)
    keyboard = []
    # First row - Month and Year
    row = []
    row.append(InlineKeyboardButton(
        MONTHS[calendar.month_name[month]]+" "+str(year),
        callback_data=data_ignore)
    )
    keyboard.append(row)
    # Second row - Week Days
    row = []
    for day in ["Пн", "Вт", "Ср", "Чт", "Пт", "Сб", "Вс"]:
        row.append(InlineKeyboardButton(day, callback_data=data_ignore))
    keyboard.append(row)

    my_calendar = calendar.monthcalendar(year, month)
    for week in my_calendar:
        row = []
        for day in week:
            if (day == 0):
                row.append(InlineKeyboardButton(
                    " ",
                    callback_data=data_ignore
                ))
            elif month == now.month and (day < now.day):
                row.append(InlineKeyboardButton(
                    " ",
                    callback_data=data_ignore
                ))
            else:
                row.append(InlineKeyboardButton(
                    str(day),
                    callback_data=create_callback_data("DAY", year, month, day)
                ))
        keyboard.append(row)
    # Last row - Buttons
    row = []
    if year <= now.year and month == now.month:
        row.append(InlineKeyboardButton(" ", callback_data=data_ignore))
    else:
        row.append(InlineKeyboardButton(
            "<",
            callback_data=create_callback_data("PREV-MONTH", year, month, day)
        ))
    row.append(InlineKeyboardButton(" ", callback_data=data_ignore))
    row.append(InlineKeyboardButton(
        ">",
        callback_data=create_callback_data("NEXT-MONTH", year, month, day)
    ))
    keyboard.append(row)

    return InlineKeyboardMarkup(keyboard)


async def process_calendar_selection(bot, update):
    """
    Process the callback_query. This method generates a new calendar if
    forward or backward is pressed. This method should be called inside
    a CallbackQueryHandler.
    :param telegram.Bot bot: The bot, as provided by the CallbackQueryHandler
    :param telegram.Update update: The update, as provided by the
    CallbackQueryHandler
    :return: Returns a tuple (Boolean,datetime.datetime), indicating if a date
    is selected
                and returning the date if so.
    """
    ret_data = (False, None)
    query = bot.callback_query
    print(query.data)
    (action, year, month, day) = separate_callback_data(query.data)
    curr = datetime.datetime(int(year), int(month), 1)
    if action == "IGNORE":
        return
    elif action == "DAY":
        print("changing day")
        await query.message.edit_text(query.message.text)
        ret_data = True, datetime.datetime(int(year), int(month), int(day))
    elif action == "PREV-MONTH":
        pre = curr - datetime.timedelta(days=1)
        await query.message.edit_text(
            query.message.text,
            reply_markup=create_calendar(int(pre.year), int(pre.month))
        )
    elif action == "NEXT-MONTH":
        ne = curr + datetime.timedelta(days=31)
        await query.message.edit_text(
            query.message.text,
            reply_markup=create_calendar(int(ne.year), int(ne.month))
        )
    else:
        print("else")
        return
    return ret_data
