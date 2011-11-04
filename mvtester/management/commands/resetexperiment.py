from optparse import make_option
from django.core.management.base import BaseCommand, CommandError
from mvtester.models import Treatment, Goal, Experiment, GoalStats

class Command(BaseCommand):
    requires_model_validation = True
    args = 'experiment'

    def handle(self, *args, **options):
        e = Experiment.objects.get(slug=args[0])
        for t in Treatment.objects.filter(experiment=e):
            t.visitors_treated = 0
            t.save()
            t.goalstats_set.all().delete()