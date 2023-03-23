import sqlalchemy as sq
from sqlalchemy.orm import Session
from solbot_db.models import Users, Orders, Blacklist, Admins, create_tables


class BotDB:
    def __init__(self):
        # DSN = f'postgresql://{USER}:{PASSWORD}@localhost:5432/db_name'
        DSN = 'sqlite:///sqlite3.db'
        self.engine = sq.create_engine(DSN, echo=False)

    def user_is_blocked(self, user_id) -> bool:
        with Session(bind=self.engine) as session:
            user = session.query(Users).filter(Users.user_id == user_id).first()

            return True if user else False

    def add_user_to_blacklist(self, user_id, username) -> None:
        with Session(bind=self.engine) as session:
            user = session.query(Users).filter(Users.user_id == user_id).first()
            if not user:
                session.add(Users(user_id=user_id, username=username))
                session.commit()

    def del_user_from_blacklist(self, user_id) -> None:
        with Session(bind=self.engine) as session:
            user = session.query(Users).filter(Users.user_id == user_id).first()
            session.delete(user)
            session.commit()

    def add_user_info(self, user_id, name, surname, email, instagram) -> None:
        with Session(bind=self.engine) as session:
            user = session.query(Users).filter(Users.user_id == user_id).first()
            if not user:
                session.add(Users(user_id=user_id, name=name, surname=surname, email=email, instagram=instagram))
                session.commit()

    def order_exists(self, user_id) -> bool:
        with Session(bind=self.engine) as session:
            order = session.query(Orders.order_id).join(Users).filter(Users.user_id == user_id, Orders.open == True,
                                                                      Orders.paid == False).first()

            return True if order else False

    def create_order(self, user_id, url) -> int:
        with Session(bind=self.engine) as session:
            session.add(Orders(user_id=user_id, url=url))
            session.commit()
            order_id = session.query(Orders.order_id).filter(Orders.user_id == user_id, Orders.url == url,
                                                             Orders.open == True).first()
        return order_id[0]

    def get_user_info(self, user_id) -> Users:
        user_data = {}
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
