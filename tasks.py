import smtplib
from email.header import Header
from email.mime.text import MIMEText

from celery import Celery
from celery.schedules import crontab
from flask_mail import Mail, Message

from webapp import create_app
import price_parsers
from webapp.config import SENDER, SUBJ_FOR_EMAIL

flask_app = create_app()
celery_app = Celery('tasks', broker='redis://localhost:6379/0')
mail = Mail(flask_app)


@celery_app.on_after_configure.connect
def setup_tasks(sender, **kwargs):
    sender.add_periodic_task(crontab(minute=0, hour='*/5'), update_prices_megafon.s())
    sender.add_periodic_task(crontab(minute=0, hour='*/5'), update_prices_eldorado.s())
    sender.add_periodic_task(crontab(minute=0, hour='*/5'), update_prices_techport.s())
    sender.add_periodic_task(crontab(minute=0, hour='*/5'), update_prices_citilink.s())
    sender.add_periodic_task(crontab(minute=0, hour='*/5'), update_prices_mts.s())


@celery_app.task
def update_prices_megafon():
    with flask_app.app_context():
        price_parsers.MegafonParser().update_db()


@celery_app.task
def update_prices_eldorado():
    with flask_app.app_context():
        price_parsers.EldoradoParser().update_db()


@celery_app.task
def update_prices_techport():
    with flask_app.app_context():
        price_parsers.TechportParser().update_db()


@celery_app.task
def update_prices_citilink():
    with flask_app.app_context():
        price_parsers.CitilinkParser().update_db()


@celery_app.task
def update_prices_mts():
    with flask_app.app_context():
        price_parsers.MtsParser().update_db()


@celery_app.task
def send_mail(email, phone_name):
    with flask_app.app_context():
        msg = Message(subject=SUBJ_FOR_EMAIL, recipients=[email], sender=SENDER)
        msg.body = f'Цена на {phone_name} из Вашего избранного снизилась!'
        mail.send(msg)

