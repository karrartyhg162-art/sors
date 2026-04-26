"""جدول قاعدة بيانات لإدارة مشرفي البوت المساعد"""

try:
    from . import BASE, SESSION
except ImportError as e:
    raise AttributeError from e

from sqlalchemy import Column, String, UnicodeText


class BotAdmins(BASE):
    __tablename__ = "bot_admins"
    user_id = Column(String, primary_key=True, nullable=False)
    first_name = Column(UnicodeText)
    username = Column(UnicodeText)
    date = Column(UnicodeText)

    def __init__(self, user_id, first_name, username, date):
        self.user_id = str(user_id)
        self.first_name = first_name
        self.username = username
        self.date = date


BotAdmins.__table__.create(checkfirst=True)


def add_bot_admin(user_id, first_name, username, date):
    """إضافة مشرف جديد للبوت"""
    if SESSION.query(BotAdmins).filter(BotAdmins.user_id == str(user_id)).one_or_none():
        return False  # already exists
    adder = BotAdmins(str(user_id), first_name, username, date)
    SESSION.add(adder)
    SESSION.commit()
    return True


def rem_bot_admin(user_id):
    """إزالة مشرف من البوت"""
    rem = (
        SESSION.query(BotAdmins)
        .filter(BotAdmins.user_id == str(user_id))
        .delete(synchronize_session="fetch")
    )
    if rem:
        SESSION.commit()
        return True
    return False


def get_all_bot_admins():
    """جلب جميع مشرفي البوت"""
    try:
        return SESSION.query(BotAdmins).all()
    except BaseException:
        return []
    finally:
        SESSION.close()


def is_bot_admin(user_id):
    """التحقق إذا كان المستخدم مشرف في البوت"""
    try:
        return (
            SESSION.query(BotAdmins)
            .filter(BotAdmins.user_id == str(user_id))
            .one_or_none()
        )
    except BaseException:
        return None
    finally:
        SESSION.close()
