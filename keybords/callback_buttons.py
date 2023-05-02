import math

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder


def edit_message_kb() -> InlineKeyboardMarkup:
    buttons = [
        [
            InlineKeyboardButton(text='Description', callback_data='Description'),
            InlineKeyboardButton(text='Category', callback_data='Category')
        ],
        [
            InlineKeyboardButton(text='Location', callback_data='Location'),
            InlineKeyboardButton(text='Camera', callback_data='Camera')
        ],
        [
            InlineKeyboardButton(text='Artist', callback_data='Artist')
        ],
        [
            InlineKeyboardButton(text='<< Back to post', callback_data='<< Back'),
            InlineKeyboardButton(text='Show message', callback_data='Show')
        ]
    ]

    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard


def ok_edit_kb() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.add(InlineKeyboardButton(text='Ok', callback_data='Ok'))
    builder.add(InlineKeyboardButton(text='Edit', callback_data='Edit'))
    return builder.as_markup()


def category_kb() -> InlineKeyboardMarkup:
    buttons = [
        [
            InlineKeyboardButton(text='What is South Korea for me', callback_data='What is South Korea for me')
        ],
        [
            InlineKeyboardButton(text='The purest feeling in the life',
                                 callback_data='The purest feeling in the life')
        ],
        [
            InlineKeyboardButton(text="Student’s life", callback_data="Student’s life"),
            InlineKeyboardButton(text='Urban', callback_data='Urban')
        ],
        [
            InlineKeyboardButton(text='Model photography', callback_data='Model photography'),
            InlineKeyboardButton(text='People', callback_data='People')
        ],
        [
            InlineKeyboardButton(text='Creativity', callback_data='Creativity'),
            InlineKeyboardButton(text='Nature', callback_data='Nature')
        ],
        [
            InlineKeyboardButton(text='Global citizen', callback_data='Global citizen')
        ]
    ]

    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard


def confirm_kb() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.add(InlineKeyboardButton(text='Confirm selection', callback_data='Confirm'))
    builder.add(InlineKeyboardButton(text='Back', callback_data='Back'))
    builder.adjust(1)
    return builder.as_markup()


def anonymous_kb() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.add(InlineKeyboardButton(text='Anonymous author', callback_data='Anonymous author'))
    return builder.as_markup()


def admin_kb(user_id) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.add(InlineKeyboardButton(text='Approve', callback_data=f'Publish {user_id}'))
    builder.add(InlineKeyboardButton(text='Publish to Collection', callback_data=f'Collection {user_id}'))
    builder.add(InlineKeyboardButton(text='Reject', callback_data='Reject'))
    builder.adjust(1)
    return builder.as_markup()


def yes_back_kb() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.add(InlineKeyboardButton(text='Yes', callback_data='Yes'))
    builder.add(InlineKeyboardButton(text='Back to main menu', callback_data='Main menu'))
    return builder.as_markup()


def change_data_kb() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.add(InlineKeyboardButton(text='Continue', callback_data='Next'))
    builder.add(InlineKeyboardButton(text='Edit', callback_data='Change'))
    return builder.as_markup()


def choose_user_data_kb() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.add(InlineKeyboardButton(text='Name', callback_data='name'))
    builder.add(InlineKeyboardButton(text='Email', callback_data='email'))
    builder.add(InlineKeyboardButton(text='Instagram', callback_data='instagram'))
    builder.add(InlineKeyboardButton(text='Back', callback_data='Back change'))
    builder.adjust(1)
    return builder.as_markup()


def change_url_kb() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.add(InlineKeyboardButton(text='Everything is cool', callback_data='Next url'))
    builder.add(InlineKeyboardButton(text='Edit a link', callback_data='Change url'))
    return builder.as_markup()


def order_photo_album_kb() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.add(InlineKeyboardButton(text='Order the Photo Album', callback_data='album'))
    return builder.as_markup()


def order_book_kb() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.add(InlineKeyboardButton(text='Order the PCS Book', callback_data='book'))
    return builder.as_markup()


def payment_kb() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.add(InlineKeyboardButton(text='💰 In Cash', callback_data='In Cash'))
    builder.add(InlineKeyboardButton(text='💳 Bank Account', callback_data='Bank Account'))
    return builder.as_markup()


def orders_category_kb() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.add(InlineKeyboardButton(text='Photo album', callback_data='admin album'))
    builder.add(InlineKeyboardButton(text='Book', callback_data='admin book'))
    return builder.as_markup()


def open_closed_orders_kb(product) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.add(InlineKeyboardButton(text='Open', callback_data=f'open {product}'))
    builder.add(InlineKeyboardButton(text='Closed', callback_data=f'closed {product}'))
    builder.add(InlineKeyboardButton(text='↩️ Back', callback_data=f'back {product}'))
    builder.adjust(2)
    return builder.as_markup()


def paid_unpaid_orders_kb(product) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.add(InlineKeyboardButton(text='Paid', callback_data=f'paid {product}'))
    builder.add(InlineKeyboardButton(text='Unpaid', callback_data=f'unpaid {product}'))
    builder.add(InlineKeyboardButton(text='↩️ Back', callback_data=f'back open/closed {product}'))
    builder.adjust(2)
    return builder.as_markup()


def closed_orders_kb(product) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.add(InlineKeyboardButton(text='Completed', callback_data=f'completed {product}'))
    builder.add(InlineKeyboardButton(text='Canceled', callback_data=f'canceled {product}'))
    builder.add(InlineKeyboardButton(text='↩️ Back', callback_data=f'back open/closed {product}'))
    builder.adjust(2)
    return builder.as_markup()


def orders_kb(product, orders, count, offset) -> InlineKeyboardMarkup:
    step = offset + 5
    step = count if step > count else step
    pages = math.ceil(count / 5)
    current_page = math.ceil(step / 5)

    buttons, navigation_buttons = [], []
    for order in orders[offset:step]:
        buttons.append([InlineKeyboardButton(text=order[0], callback_data=f'order {order[0]}')])

    if offset > 0:
        navigation_buttons.append(InlineKeyboardButton(text='⬅️ Previous', callback_data='previous page'))
    if pages > 1:
        navigation_buttons.append(InlineKeyboardButton(text=f'Page {current_page}/{pages}', callback_data=f'page'))
    if step < count:
        navigation_buttons.append(InlineKeyboardButton(text='Next ➡️', callback_data='next page'))

    buttons.append(navigation_buttons)
    buttons.append([InlineKeyboardButton(text='↩️ Back', callback_data=f'back paid/unpaid {product}')])
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)

    return keyboard


def unpaid_order_more_kb(order_id) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.add(InlineKeyboardButton(text='✅ Approve the order', callback_data=f'Approve {order_id}'))
    builder.add(InlineKeyboardButton(text='❌ Cancel the order', callback_data=f'Cancel {order_id}'))
    builder.add(InlineKeyboardButton(text='↩️ Back to orders', callback_data='Back to orders'))
    builder.adjust(2)
    return builder.as_markup()


def paid_order_more_kb(order_id) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.add(InlineKeyboardButton(text='✅ Complete the order', callback_data=f'Complete {order_id}'))
    builder.add(InlineKeyboardButton(text='📨 Notify of readiness', callback_data=f'Notify {order_id}'))
    builder.add(InlineKeyboardButton(text='❌ Cancel the order', callback_data=f'Cancel {order_id}'))
    builder.add(InlineKeyboardButton(text='↩️ Back to orders', callback_data='Back to orders'))
    builder.adjust(2, 1)
    return builder.as_markup()


def back_orders() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.add(InlineKeyboardButton(text='↩️ Back to orders', callback_data='Back to orders'))
    return builder.as_markup()
