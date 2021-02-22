from datetime import timedelta

from django.db.models import Q
from django.utils import timezone

from django_cron import CronJobBase, Schedule
from products.models import Cart


class CleanCards(CronJobBase):
    RUN_EVERY_MINS = 24 * 60
    schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
    code = 'CleanCards'

    def do(self):
        some_day_last_week = timezone.now().date() - timedelta(days=7)
        qs = Cart.objects.filter(Q(created_at__lte=some_day_last_week) & Q(user=None))
        qs.delete()
