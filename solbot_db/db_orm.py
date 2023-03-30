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

    def order_exists(self, user_id) -> bool:
        with Session(bind=self.engine) as session:
            order = session.query(Orders.order_id).filter(Orders.user_id == user_id, Orders.open == True,
                                                          Orders.paid == False).first()

            return True if order else False

    def create_order(self, user_id, url) -> int:
        while True:
            with Session(bind=self.engine) as session:
                try:
                    hash_id = get_hash()
                    session.add(Orders(order_id=hash_id, user_id=user_id, url=url))
                    session.commit()
                    order_id = session.query(Orders.order_id).filter(Orders.user_id == user_id, Orders.url == url,
                                                                     Orders.open == True).first()
                    return order_id[0]
                except sqlalchemy.exc.IntegrityError:
                    continue

    def cancel_order(self, user_id) -> int:
        with Session(bind=self.engine) as session:
            order = session.query(Orders).filter(Orders.user_id == user_id, Orders.open == True).first()
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

    def change_user_data(self, user_id, name=None, email=None, instagram=None) -> None:
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

    def order_message_for_admin(self, order_id) -> str:
        with Session(bind=self.engine) as session:
            users_order = session.query(Orders.created_at, Users.name).join(Users).filter(Orders.order_id ==
                                                                                          order_id).first()
            name = users_order.name
            date = users_order.created_at.strftime('%H:%M %d.%m.%Y')

            text = f'\n<b>Order</b>: {order_id}' \
                   f'\n<b>Name</b>: {name}' \
                   f'\n<b>Created at</b>: {date}'
            return text

