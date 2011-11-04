from optparse import make_option
from django.core.management.base import BaseCommand, CommandError
from mvtester.models import Treatment, Goal

class Command(BaseCommand):
    requires_model_validation = True
    option_list = BaseCommand.option_list + (
        make_option('-t','--treatment',
            dest='treatments',
            type='str',
            action='append',
            nargs=4,
            help='Treatment Load -- TreatmentSlug GoalSlug Count ConvRate'),
        )

    def handle(self, *args, **options):
        treatment_load_strings = options.get('treatments',[])
        if not treatment_load_strings:
            raise CommandError('You must provide some treatment/goals to load')

        for treatment_load_string in treatment_load_strings:
            self.load_treatment_data(treatment_load_string[0],treatment_load_string[1],int(treatment_load_string[2]),int(treatment_load_string[3]))

    def load_treatment_data(self,treatment_slug,goal_slug,treatment_count,conv_rate):
            print('Loading data for {0}:{1}'.format(treatment_slug,goal_slug))
            treatment = Treatment.objects.get(slug=treatment_slug)
            conv_count = treatment_count * conv_rate / 100
            converted = True
            for x in xrange(treatment_count):
                if x == conv_count:
                    converted = False
                treatment.treat_visitor(goal_slug,converted)

