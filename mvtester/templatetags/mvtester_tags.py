from django.template.base import Node, TemplateSyntaxError
from mvtester.models import Treatment
from django import template
register = template.Library()

GOAL_KEY_TAG = '<input type="hidden" name="mvtester-goal-key" value="{0}:{1}:{2}"/>'
GOAL_VALUE_TAG = '<input type="hidden" name="{0}:{1}:{2}" value="{3}"/>'


class TreatmentNode(Node):
    def __init__(self, experiment, treatment, goal, default_conversion_status):
        self.goal = goal
        self.experiment = experiment
        self.treatment = treatment
        self.default_conversion_status = default_conversion_status
    def render(self, context):
        treatment = Treatment.objects.get(slug=self.treatment)
        treatment.treat_visitor()
        goal_key_tag = GOAL_KEY_TAG.format(self.experiment,self.treatment,self.goal)
        goal_value_tag = GOAL_VALUE_TAG.format(self.experiment,self.treatment,self.goal,self.default_conversion_status)
        return goal_key_tag + goal_value_tag


def treat_visitor(parser, token):
    try:
        bits = token.split_contents()
        exp = bits[1]
        trt = bits[2]
        goal = bits[3]
        conv = bits[4]
    except ValueError:
        raise TemplateSyntaxError('The treat_visitor tag takes four arguments.')
    return TreatmentNode(exp,trt,goal,conv)
    
register.tag('treat_visitor',treat_visitor)