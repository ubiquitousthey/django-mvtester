from django.db.models.manager import Manager
import os
import random
from django.db import models
import math
import re

class Experiment(models.Model):
    """
    Expirment between a control and other possible treatments of a subject
    One Treatment for this experiment must be marked as the control
    """
    is_active = models.BooleanField(default=False)
    name = models.CharField(max_length=50)
    slug = models.SlugField(max_length=50)
    url_pattern = models.CharField(max_length=255,null=True,blank=True)

    def matches(self,url):
        if self.url_pattern:
            return re.match(self.url_pattern,url)
        return False

    def get_winner(self, goal_slug):
        goal = self.goal_set.get(slug=goal_slug)
        return goal.get_winner()

    def __unicode__(self):
        return self.slug

class TreatmentManager(Manager):
    def get_random(self):
        treatments = self.get_query_set()
        index = random.randrange(0,len(treatments))
        return treatments[index]

class Treatment(models.Model):
    """
    Unique treatment of a subject
    is_control must be set to true
    """
    is_control = models.BooleanField(default=False)
    name = models.CharField(max_length=50)
    slug = models.SlugField(max_length=50)
    experiment = models.ForeignKey(Experiment)
    visitors_treated = models.PositiveIntegerField(default=0)
    #Use exp.url_pattern / template_name for middleware method
    template_name = models.CharField(max_length=255,null=True,blank=True)
    objects = TreatmentManager()

    def treat_visitor(self, goal_slug=None, converted=False):
        self.visitors_treated += 1
        self.save()
        for goal in self.experiment.goal_set.all():
            gconverted = converted and goal_slug and goal.slug == goal_slug
            goal.update(self,gconverted)

    def __unicode__(self):
        return '{0}:{1}'.format(unicode(self.experiment), self.slug)

class Goal(models.Model):
    """
    Represents one aspect that is being tested in the expirment.  For example, one may test both the conversion rate
    and the engagement rate to compare two possibilities along multiple axes
    """
    name = models.CharField(max_length=50)
    slug = models.SlugField(max_length=50)
    url_pattern = models.CharField(max_length=255,null=True,blank=True)
    experiment = models.ForeignKey(Experiment)

    def matches(self,url):
        return re.match(self.url_pattern,url)

    def update(self,treatment,converted):
        goalstats,created = treatment.goalstats_set.get_or_create(goal=self)
        goalstats.update(converted)

    def get_winner(self):
        current_winner = self.experiment.treatment_set.get(is_control=True).goalstats_set.get(goal=self)
        for result in self.goalstats_set.all():
            if result.rate > current_winner.rate and result.z_score > 1.65:
                current_winner = result

        return current_winner.treatment

    def __unicode__(self):
        return '{0}:{1}'.format(unicode(self.experiment), self.slug)

class GoalStats(models.Model):
    """
    The actual values for a goal-treatment combo
    """
    goal = models.ForeignKey(Goal)
    treatment = models.ForeignKey(Treatment)
    value = models.PositiveIntegerField(default=0)
    z_score = models.FloatField(default=0)
    rate = models.FloatField(default=0)

    class Meta:
        ordering = ('treatment','goal','-z_score','-rate')

    def update(self,converted):
        if converted:
            self.value += 1
        self.calculate_rate()
        if not self.treatment.is_control:
            self.calculate_zscore()
        self.save()

    @property
    def phi(self):
        # constants
        a1 =  0.254829592
        a2 = -0.284496736
        a3 =  1.421413741
        a4 = -1.453152027
        a5 =  1.061405429
        p  =  0.3275911

        # Save the sign of x
        sign = 1
        if self.z_score < 0:
            sign = -1
        x = abs(self.z_score)/math.sqrt(2.0)

        # A&S formula 7.1.26
        t = 1.0/(1.0 + p*x)
        y = 1.0 - (((((a5*t + a4)*t) + a3)*t + a2)*t + a1)*t*math.exp(-x*x)

        return 0.5*(1.0 + sign*y)

    def __unicode__(self):
        return '{0}:{1}'.format(self.treatment.slug,self.goal.slug)

    def calculate_rate(self):
        """
        Calculate the "conversion rate" for this goal-treatment combo
        """
        self.rate = float(self.value) / self.treatment.visitors_treated

    def calculate_zscore(self):
        """
        Calculate the Z-score for this measurment-treatment combo to determine the
        statistical significance of the measurment result
        """
        control = self.treatment.experiment.treatment_set.get(is_control=True)
        control_result, created = control.goalstats_set.get_or_create(goal=self.goal)
        if control.visitors_treated and self.treatment.visitors_treated:
            X = float(self.rate - control_result.rate)
            treatment_variance = float(self.rate * (1-self.rate))/self.treatment.visitors_treated
            control_variance = float(control_result.rate * (1-control_result.rate)) / control.visitors_treated
            if treatment_variance + control_variance > 0:
                self.z_score =  X / math.sqrt(treatment_variance + control_variance)
