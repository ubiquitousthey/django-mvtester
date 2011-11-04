import random
from django.conf import settings
import os
from django.template import loader
from django.template.base import TemplateDoesNotExist

def resolve_template_path(template):
    if isinstance(template, (list, tuple)):
        for tmp in template:
            try:
                return resolve_template_path(tmp)
            except TemplateDoesNotExist:
                continue
    elif isinstance(template, basestring):
        src, origin = loader.find_template(template)
        return origin.name
    else:
        return template

def randomize_template(template):
    template = resolve_template_path(template)
    template_dir = os.path.dirname(template)
    template_fname = os.path.basename(template)
    template_pattern = template_fname.split(os.extsep)[0]
    templates = []
    for template_option in os.listdir(os.path.dirname(template)):
        to_fname = os.path.basename(template_option)
        if to_fname.startswith(template_pattern):
            templates.append(os.path.join(template_dir,template_option))

    index = random.randrange(0,len(templates))
    template = templates[index]
    return template

def get_template(request, template):
    session_key = 'treatment-template'
    load_session_default = True

    #Debug will allow template to change
    if settings.DEBUG and request.method != 'POST':
        load_session_default = False

    #Use the session assigned template if it exists
    session_template = request.session.get(session_key)
    if session_template and load_session_default:
        return session_template

    template = randomize_template(template)
    request.session[session_key] = template

    return template

def count_chars(string):
    chars = [c for c in string]
    count = 0
    prev_c = None
    for c in chars.sort():
        if c != prev_c:
            c = prev_c
            count = 1
            print '{0}, {1}'.format(c, count)
