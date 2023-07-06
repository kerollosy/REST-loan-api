from apscheduler.schedulers.background import BackgroundScheduler
from django.core.management import call_command


def process_due_payments():
    call_command('process_payments')


def start_scheduler():
    scheduler = BackgroundScheduler()
    scheduler.add_job(process_due_payments, 'interval', days=1)
    scheduler.start()
