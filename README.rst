django-mvtester
=================
Django-mvtester is an app to facilitate multivariate testing or a/b testing.

Installation
----------------
Right now you have to get it from github

Add the middleware like this::

MIDDLEWARE_CLASSES = (

    'mvtester.middleware.MVTesterMiddleware'
)

Make sure it is after the session middleware because mvtester uses sessions to track which treatments
are active for running experiments.

Add mvtester to your installed apps like this::

INSTALLED_APPS = (

    'mvtester'
)

Example
---------------
In the example directory, there is an example of how to use each approach described below.  It example pages that should
work to record conversions.  You can also use the "loadtestdata" management command to load data for testing.

The database is all setup, so you can just run ./manage.py runserver and hit http://localhost:8000 for a demonstration.
You can login to http://localhost:8000/admin to see how to edit the Experiments, Treatment, and Goals models.  Click
on Goals to see what treatment is winning for each goal in the experiment.

Usage
----------------
There are three ways to use mvtester.  One is to use it with the middlware and url goal detection.  The advantage to
using the middleware is that you don't have to make any code changes whatsoever.  The second is to use the
has_template_experiments decorator.  You put this atop your form class-based views, and it will take care of varying
the template.  You then need to add some special variables to your form to have the decorator detect a conversion.  The
advantage is that you can have multiple goals per experiment this way.  You can use it to test form engagement as well
as conversion.  Lastly, you can use the models and their methods to do your testing.

Template Variations
~~~~~~~~~~~~~~~~~~~~~
Templates are automatically randomized using either the decorator or the middlware.  Just create similarly named
templates in the same directory.  For example:
\templates
    \myapp
       home.html
       home_experiment_1.html
       home_exp2.html
       home_tryagain.html

Using the Middlware
~~~~~~~~~~~~~~~~~~~~~~
To Use the middleware, you have to setup up your experiments and goals with url patterns so that mvtester can record
treatments and conversions.  You can setup multiple goals with different url patters to do funnel analysis for each
treatment.


Using the Decorator
~~~~~~~~~~~~~~~~~~~~~
To use the decorator place @has_template_experiments on your class-based form view.  In each template for each treatment
you must follow the pattern below to record conversions::
        <input type="hidden" name="mvtester-goal-key" value="experimentslug:treatmentslug:goalslug"/>
        <input type="hidden" name="experimentslug:treatmentslug:goalslug" value="True"/>

You can use multiple sets of these to track user engagement on the form itself using javascript to set the flag for
conversion.

