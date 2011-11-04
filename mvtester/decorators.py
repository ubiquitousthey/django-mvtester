from django.core.exceptions import ImproperlyConfigured
from mvtester.models import GoalStats, Treatment
from mvtester.utils import get_template

def has_template_experiements(cls):
    """
    Overrides the get_template_names method to return a randomly selected template based on the
    pattern returned by the original get_template_names method.
    """
    orig_get_template_names = cls.get_template_names
    def _get_template_names(self):
        """
        Returns a list containing a randomly selected template that follows the naming pattern
        of the original template.
        """
        if not hasattr(self.request, 'session'):
            raise ImproperlyConfigured(
                'The has_template_experiments decorator requires this project to be'
                'configured to use sessions.'
            )

        template_names = orig_get_template_names(self)
        if template_names is None:
            raise ImproperlyConfigured(
                "TemplateResponseMixin requires either a definition of "
                "'template_name' or an implementation of 'get_template_names()'")

        template = get_template(self.request,template_names)
        return [template]
    cls.get_template_names = _get_template_names

    orig_formvalid = cls.form_valid
    def _form_valid(self, form):
        """
        Calls the original formvalid then registers the treatment with mvtester
        """
        return_val = orig_formvalid(self, form)
        qd = self.request.POST
        goal_keys = qd.getlist('mvtester-goal-key')
        for goal_key in goal_keys:
            experiment_slug, treatment_slug, goal_slug = goal_key.split(':')
            treatment = Treatment.objects.get(experiment__slug=experiment_slug,slug=treatment_slug)
            converted = qd[goal_key][0].lower() in 'ty'
            treatment.treat_visitor(goal_slug,converted)

        return return_val
    cls.form_valid = _form_valid
    return cls
