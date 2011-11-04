from django.conf import settings
from models import Goal
from mvtester.models import Experiment, Treatment
from mvtester.utils import randomize_template, get_template

ACTIVE_EXPERIMENTS = 'mvt-experiments'
EXPERIMENT_PREFIX = 'mvt-exp-trt-'

class MVTesterMiddleware(object):
    def process_view( self, request, view_func, args, kwargs ):
        try:
            experiments = request.session.get(ACTIVE_EXPERIMENTS,[])
            for goal in Goal.objects.filter(experiment__id__in=experiments,experiment__url_pattern__isnull=False):
                treatment_slug = request.session[EXPERIMENT_PREFIX+goal.experiment.slug]
                treatment = Treatment.objects.get(slug=treatment_slug)
                if goal.matches(request.path):
                    goal.update(treatment,True)
        except Exception:
            if settings.DEBUG:
                raise

    def process_template_response(self, request, response):
        try:
            for exp in Experiment.objects.filter(is_active=True,url_pattern__isnull=False):
                if exp.matches(request.path):
                    treatment = exp.treatment_set.get_random()
                    treatment.treat_visitor()
                    response.template_name = treatment.template_name
                    request.session[EXPERIMENT_PREFIX+treatment.experiment.slug] = treatment.slug
                    if ACTIVE_EXPERIMENTS not in request.session:
                        request.session[ACTIVE_EXPERIMENTS] = []

                    request.session[ACTIVE_EXPERIMENTS].append(treatment.experiment.id)
                    return response

            return response
        except Exception:
            if settings.DEBUG:
                raise
