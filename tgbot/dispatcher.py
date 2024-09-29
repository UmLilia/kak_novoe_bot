from telegram.ext import (CallbackQueryHandler, CommandHandler,
                          ConversationHandler, MessageHandler, filters)

from .main_functions import (about_us, additionally, address, aroma, basket,
                             care_set, conditions, finish_order, history,
                             ironing, manager, order_agree, order_date, price,
                             spots, start, subscription_order, thanks, time,
                             wake_up, wishes, wishes_delivery,
                             write_additionally)

(MAIN_MENU, PROFILE, IRONING, SPOTS, HISTORY, WISHES, DELIVERY, ADDRESS,
 DONE_ADDRESS) = range(9)


def setup_handlers(application):
    conv_handler = ConversationHandler(
        entry_points=[
            CommandHandler('start', start),
            MessageHandler(filters.Regex('Вернуться в главное меню'), wake_up),
            MessageHandler(filters.TEXT, wake_up)
        ],
        states={
            MAIN_MENU: [
                MessageHandler(
                    filters.Regex('^(Вернуться в главное меню)$'),
                    wake_up
                ),
                CommandHandler('start', start),
                MessageHandler(
                    filters.Regex('^(Мне нужна помощь персонального*)'),
                    manager
                ),
                MessageHandler(
                    filters.Regex('^(Забрать мою корзину 🧺)$'),
                    basket
                ),
                MessageHandler(
                    filters.Regex('^(Назад)$'),
                    basket
                ),
                MessageHandler(
                    filters.Regex('^(Что входит в цикл заботы?)'),
                    conditions
                ),
                CallbackQueryHandler(time),
                MessageHandler(filters.Regex('^(О нас)$'), about_us),
                MessageHandler(filters.Regex('^(Цены)$'), price),
                MessageHandler(filters.Regex(
                    '^(Связь с персональным менеджером 🕘)$'),
                    manager
                ),
                MessageHandler(filters.Regex('^(Набор заботы)$'), care_set),
                MessageHandler(filters.Regex(
                    '^(Отследить мой заказ)$'),
                    manager
                ),
                MessageHandler(filters.Regex('^(Заполнить анкету)$'), aroma),
                MessageHandler(filters.Regex(
                    '^(Пробный цикл заботы ••• 1290 руб.)$'), order_agree),
                MessageHandler(filters.Regex(
                    '^(Абонемент *)'
                ), order_agree),
                MessageHandler(filters.Regex(
                    '^(Получить набор заботы)$'),
                    manager
                ),
                MessageHandler(filters.Regex(
                    '^(Мне подходит этот вариант!)$'),
                    order_agree
                ),
                MessageHandler(filters.Regex(
                    '^(Заказ по абонементу)$'),
                    subscription_order
                ),
                MessageHandler(filters.Regex(
                    '^(Посмотреть абонементы)$'),
                    subscription_order
                ),
                MessageHandler(filters.Regex(
                    '^(Вернуться к выбору даты)$'),
                    order_date
                ),
                MessageHandler(filters.Regex(
                    '^(07.00-*|09.00-*|11.00-*|13.0*|15.0*|17.0*|19.0*|21.0*)'
                ), finish_order),
                MessageHandler(filters.Regex(
                    '^(Санкт-Пет*|Зеленогорск|Сестрорецк|Кронштадт|Всевол*)'
                ), address),
                MessageHandler(filters.Regex(
                    '^(В списке нет моего города)$'),
                    manager
                ),
                MessageHandler(filters.TEXT, wake_up)
            ],
            PROFILE: [
                MessageHandler(filters.Regex(
                    '^(Вернуться в главное меню)$'),
                    wake_up
                ),
                MessageHandler(filters.TEXT, ironing)
            ],
            IRONING: [
                MessageHandler(filters.Regex(
                    '^(Вернуться к предыдущему вопросу)$'
                ), aroma),
                MessageHandler(filters.TEXT, spots)
            ],
            SPOTS: [
                MessageHandler(filters.Regex(
                    '^(Вернуться к предыдущему вопросу)$'),
                    ironing
                ),
                MessageHandler(filters.TEXT, history)
            ],
            HISTORY: [
                MessageHandler(filters.Regex(
                    '^(Вернуться к предыдущему вопросу)$'),
                    spots
                ),
                MessageHandler(filters.TEXT, wishes)
            ],
            WISHES: [
                MessageHandler(filters.Regex(
                    '^(Предыдущий вопрос)$'),
                    history
                ),
                MessageHandler(filters.TEXT, wishes_delivery)
            ],
            DELIVERY: [
                MessageHandler(filters.Regex('^(Предыдущий вопрос)$'), wishes),
                MessageHandler(filters.TEXT, thanks),
            ],
            ADDRESS: [
                MessageHandler(filters.Regex(
                    '^(Предыдущий вопрос)$'),
                    order_agree
                ),
                MessageHandler(filters.TEXT, additionally),
            ],
            DONE_ADDRESS: [
                MessageHandler(filters.Regex(
                    '^(Предыдущий вопрос)$'),
                    address
                ),
                MessageHandler(filters.TEXT, write_additionally),
                CallbackQueryHandler(time),
            ],
        },
        fallbacks=[
            CommandHandler('start', start)
        ],
    )

    application.add_handler(conv_handler)
    return application
