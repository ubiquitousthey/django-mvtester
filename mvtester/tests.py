from django.test import TestCase
from django.test.client import Client
from models import Experiment, Treatment, Goal, GoalStats
import random

def randomly_select(sel_list):
    index = random.randrange(0,len(list))
    return sel_list[index]

class ExperimentTest(TestCase):
    def setUp(self):
        self.experiment = Experiment.objects.create(
            name='Test',
            slug='test'
        )

        Goal.objects.create(
            name='Test Conversion',
            slug='test-conversion',
            experiment=self.experiment
        )

        self.control = Treatment.objects.create(
            is_control=True,
            experiment=self.experiment,
            slug='test-control',
            name='Test Control'
        )

        Treatment.objects.create(
            experiment=self.experiment,
            slug='test-a',
            name='Test A'
        )

        Treatment.objects.create(
            experiment=self.experiment,
            slug='test-b',
            name='Test B'
        )

    def run_test(self, control_visitor, control_convert, test1_visitor, test1_convert, test2_visitor, test2_convert):
        treatments = self.experiment.treatment_set.filter(is_control=False)

        self.control.treat_visitor('test-conversion', False)
        self.control.visitors_treated = control_visitor
        self.control.save()
        control_result = self.control.goalstats_set.get(goal__slug='test-conversion')
        control_result.value = control_convert
        control_result.calculate_rate()
        control_result.save()

        treatment = treatments[0]
        treatment.treat_visitor('test-conversion', False)
        treatment.visitors_treated = test1_visitor
        treatment.save()
        result = treatment.goalstats_set.get(goal__slug='test-conversion')
        result.value = test1_convert
        result.calculate_rate()
        result.calculate_zscore()
        result.save()

        treatment = treatments[1]
        treatment.treat_visitor('test-conversion', False)
        treatment.visitors_treated = test2_visitor
        treatment.save()
        result = treatment.goalstats_set.get(goal__slug='test-conversion')
        result.value = test2_convert
        result.calculate_rate()
        result.calculate_zscore()
        result.save()

    def test_determine_winner(self):
        treatments = self.experiment.treatment_set.filter(is_control=False)

        self.run_test(182,35,160,45,189,28)
        self.assertEqual(treatments[0], self.experiment.get_winner('test-conversion'))

        self.run_test(182,35,180,12,189,51)
        self.assertEqual(treatments[1], self.experiment.get_winner('test-conversion'))

        self.run_test(182,35,180,45,189,28)
        self.assertEqual(self.control, self.experiment.get_winner('test-conversion'))

class TreatmentTest(TestCase):
    """
    Tests for django-mvtester
    """
    def setUp(self):
        self.experiment = Experiment.objects.create(
            name='Test',
            slug='test'
        )

        Goal.objects.create(
            name='Test Conversion',
            slug='test-conversion',
            experiment=self.experiment
        )

        self.control = Treatment.objects.create(
            is_control=True,
            experiment=self.experiment,
            slug='test-control',
            name='Test Control'
        )

        Treatment.objects.create(
            experiment=self.experiment,
            slug='test-a',
            name='Test A'
        )

        Treatment.objects.create(
            experiment=self.experiment,
            slug='test-b',
            name='Test B'
        )

    def test_treatment(self):
        self.control.treat_visitor('test-conversion',True)
        self.control.treat_visitor('test-conversion',True)
        self.assertEqual(2,self.control.visitors_treated,'Visitor Count')

    def test_treatment_goal(self):
        self.control.treat_visitor('test-conversion', True)
        self.control.treat_visitor('test-conversion', False)
        result = self.control.goalstats_set.get(goal__slug='test-conversion')

        self.assertEqual(1,result.value,'Measurement Value')

    def test_rate(self):
        self.control.treat_visitor('test-conversion', False)
        self.control.visitors_treated = 182
        self.control.save()
        control_result = self.control.goalstats_set.get(goal__slug='test-conversion')
        control_result.value = 35
        control_result.calculate_rate()
        control_result.save()
        self.assertEqual(round(control_result.rate,4), .1923)

    def test_zscore(self):
        treatments = self.experiment.treatment_set.filter(is_control=False)

        self.control.treat_visitor('test-conversion', False)
        self.control.visitors_treated = 182
        self.control.save()
        control_result = self.control.goalstats_set.get(goal__slug='test-conversion')
        control_result.value = 35
        control_result.calculate_rate()
        control_result.save()

        treatment = treatments[0]
        treatment.treat_visitor('test-conversion', False)
        treatment.visitors_treated = 188
        treatment.save()
        result = treatments[0].goalstats_set.get(goal__slug='test-conversion')
        result.value = 61
        result.calculate_rate()
        result.calculate_zscore()
        result.save()

        self.assertEqual(round(result.z_score,2), 2.94)

class RandomizeTemplate(TestCase):
    def test_resolve_template(self):
        pass

    def test_randomize_template(self):
        pass

class TestMiddleware(TestCase):
    def test_middleware_goal(self):
        c = Client('/')
