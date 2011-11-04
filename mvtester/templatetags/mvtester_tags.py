from django.template.base import Node

class Treat(Node):
    def __init__(self, measurement):
        self.measurement = measurement
    def render(self, context):
        return '<!--Measuring {0}-->'.format(self.measurement)