from datetime import datetime

import sqlalchemy as sq
import sqlalchemy.exc
from sqlalchemy.orm import Session
from solbot_db.models import Users, Orders, Blacklist, Admins, create_tables
from utils import get_hash


class BotDB:
    def __init__(self):
        # DSN = f'postgresql://{USER}:{PASSWORD}@localhost:5432/db_name'
        DSN = 'sqlite:///sqlite3.db'
        self.engine = sq.create_engine(DSN, echo=False)

    # def user_is_blocked(self, user_id) -> bool:
    #     with Session(bind=self.engine) as session:
    #         user = session.query(Users).filter(Users.user_id == user_id).first()
    #
    #         return True if user else False

    # def add_user_to_blacklist(self, user_id, username) -> None:
    #     with Session(bind=self.engine) as session:
    #         user = session.query(Users).filter(Users.user_id == user_id).first()
    #         if not user:
    #             session.add(Users(user_id=user_id, username=username))
    #             session.commit()

    # def del_user_from_blacklist(self, user_id) -> None:
    #     with Session(bind=self.engine) as session:
    #         user = session.query(Users).filter(Users.user_id == user_id).first()
    #         session.delete(user)
    #         session.commit()

    # def add_user_info(self, user_id, name, surname, email, instagram) -> None:
    #     with Session(bind=self.engine) as session:
    #         user = session.query(Users).filter(Users.user_id == user_id).first()
    #         if not user:
    #             session.add(Users(user_id=user_id, name=name, surname=surname, email=email, instagram=instagram))
    #             session.commit()

    def order_exists(self, user_id, product) -> bool:
        with Session(bind=self.engine) as session:
            order = session.query(Orders.order_id).filter(Orders.user_id == user_id, Orders.product == product,
                                                          Orders.open == True,
                                                          Orders.paid == False).first()

            return True if order else False

    def create_order(self, user_id, product, **kwargs) -> int:
        while True:
            with Session(bind=self.engine) as session:
                try:
                    hash_id = get_hash()
                    session.add(Orders(order_id=hash_id, user_id=user_id, product=product, **kwargs))
                    session.commit()
                    return hash_id
                except sqlalchemy.exc.IntegrityError:
                    continue

    def cancel_order(self, user_id, product) -> int:
        with Session(bind=self.engine) as session:
            order = session.query(Orders).filter(Orders.user_id == user_id, Orders.product == product,
                                                 Orders.open == True).first()
            order_id = order.order_id
            order.open = False
            order.canceled = True
            session.commit()
        return order_id

    def get_user_info(self, user_id) -> Users:
        with Session(bind=self.engine) as session:
            user = session.query(Users).filter(Users.user_id == user_id).first()
            return user

    def user_exists(self, user_id) -> bool:
        with Session(bind=self.engine) as session:
            user = session.query(Users).filter(Users.user_id == user_id).first()
            return True if user else False

    def update_user(self, user_id, name=None, email=None, instagram=None) -> None:
        with Session(bind=self.engine) as session:
            user = session.query(Users).filter(Users.user_id == user_id).first()
            if name:
                user.name = name
            if email:
                user.email = email
            if instagram:
                user.instagram = instagram

            session.commit()

    def create_user(self, user_id, name, username, email, instagram) -> None:
        with Session(bind=self.engine) as session:
            session.add(Users(user_id=user_id, name=name, username=username, email=email, instagram=instagram))
            session.commit()

    def order_message_for_admin(self, order_id, product) -> str:
        with Session(bind=self.engine) as session:
            users_order = session.query(Orders.url, Orders.created_at, Users.name).join(Users).filter(Orders.order_id ==
                                                                                                      order_id).first()

            text = f'\n<b>Order</b>: {order_id}' \
                   f'\n<b>Product</b>: {product}' \
                   f'\n<b>Name</b>: {users_order.name}' \
                   f'\n<b>URL</b>: {users_order.url}' \
                   f'\n<b>Created at</b>: {users_order.created_at.strftime("%H:%M %d.%m.%Y")}'
            return text

    def get_orders(self, product, open, paid, canceled) -> list:
        with Session(bind=self.engine) as session:
            orders = session.query(Orders.order_id).filter(Orders.product == product,
                                                           Orders.open == open, Orders.paid == paid,
                                                           Orders.canceled == canceled).all()

        return orders

    def get_order_more(self, order_id) -> str:
        with Session(bind=self.engine) as session:
            order = session.query(Orders.order_id, Users.name, Users.username, Users.email, Users.instagram,
                                  Orders.created_at, Orders.url).join(Users).filter(Orders.order_id == order_id).first()

            text = f'<b>Order number</b>: {order.order_id}' \
                   f'\n<b>Name</b>: {order.name}' \
                   f'\n<b>Username</b>: {order.username}' \
                   f'\n<b>Email</b>: {order.email}' \
                   f'\n<b>Instagram</b>: {order.instagram}' \
                   f'\n<b>URL</b>: {order.url}' \
                   f'\n<b>Created at</b>: {order.created_at.strftime("%H:%M %d.%m.%Y")}'

            return text

    def get_closed_orders(self, product, canceled, paid=None) -> str:
        with Session(bind=self.engine) as session:
            if paid:
                orders = session.query(Orders.order_id, Users.name, Users.username, Users.email, Users.instagram,
                                       Orders.created_at, Orders.url).join(Users).filter(Orders.product == product,
                                                                                         Orders.open == False,
                                                                                         Orders.paid == paid,
                                                                                         Orders.canceled == canceled).all()
            else:
                orders = session.query(Orders.order_id, Users.name, Users.username, Users.email, Users.instagram,
                                       Orders.created_at, Orders.url).join(Users).filter(Orders.product == product,
                                                                                         Orders.open == False,
                                                                                         Orders.canceled == canceled).all()
            result = []
            if orders:
                for order in orders:
                    text = f'<b>Order number</b>: {order.order_id}' \
                           f'\n<b>Name</b>: {order.name}' \
                           f'\n<b>Username</b>: {order.username}' \
                           f'\n<b>Email</b>: {order.email}' \
                           f'\n<b>Instagram</b>: {order.instagram}' \
                           f'\n<b>URL</b>: {order.url}' \
                           f'\n<b>Created at</b>: {order.created_at.strftime("%H:%M %d.%m.%Y")}'
                    result.append(text)
            return result

    def cancel_the_order(self, order_id) -> int:
        with Session(bind=self.engine) as session:
            order = session.query(Orders).filter(Orders.order_id == order_id).first()
            order.canceled = True
            order.open = False
            user_id = order.user_id
            session.commit()

            return user_id

    def approve_the_order(self, order_id) -> int:
        with Session(bind=self.engine) as session:
            order = session.query(Orders).filter(Orders.order_id == order_id).first()
            order.paid = True
            user_id = order.user_id
            session.commit()

            return user_id

    def complete_the_order(self, order_id) -> None:
        with Session(bind=self.engine) as session:
            order = session.query(Orders).filter(Orders.order_id == order_id).first()
            order.open = False
            session.commit()

    def get_order_user(self, order_id) -> int:
        with Session(bind=self.engine) as session:
            user_id = session.query(Orders.user_id).filter(Orders.order_id == order_id).first()
            return user_id[0]
