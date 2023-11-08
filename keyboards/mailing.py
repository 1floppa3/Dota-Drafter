from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

ikb_mailing_add_next_quit = InlineKeyboardMarkup(row_width=1).add(
    InlineKeyboardButton(text='Добавить фотографию', callback_data='add_photo'),
    InlineKeyboardButton(text='Далее', callback_data='next_step_mailing'),
    InlineKeyboardButton(text='Отменить', callback_data='quit_mailing')
)

ikb_mailing_next_quit = InlineKeyboardMarkup(row_width=1).add(
    InlineKeyboardButton(text='Далее', callback_data='next_step_mailing'),
    InlineKeyboardButton(text='Отменить', callback_data='quit_mailing')
)

ikb_mailing_quit = InlineKeyboardMarkup(row_width=1).add(
    InlineKeyboardButton(text='Отменить', callback_data='quit_mailing')
)
