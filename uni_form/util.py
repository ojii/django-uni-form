from django.forms.forms import BoundField
from django.template.loader import render_to_string


def render_field(field, form, template="uni_form/field.html", labelclass=None):
    if not isinstance(field, str):
        return field.render(form)

    try:
        field_instance = form.fields[field]
    except KeyError:
        raise Exception("Could not resolve form field '%s'." % field)
    bound_field = BoundField(form, field_instance, field)
    html = render_to_string(template, {'field': bound_field, 'labelclass': labelclass})
    if not hasattr(form, 'rendered_fields'):
        form.rendered_fields = []
    if not field in form.rendered_fields:
        form.rendered_fields.append(field)
    else:
        raise Exception("A field should only be rendered once: %s" % field)
    return html


class BaseInput(object):
    """
        An base Input class to reduce the amount of code in the Input classes.
    """
    
    def __init__(self, name, value):
        self.name = name
        self.value = value
        

class Toggle(object):
    """
        A container for holder toggled items such as fields and buttons.
    """
    
    fields = []
    
    
class FieldRenderer(object):
    def __init__(self, field, form):
        self.field = field
        self.form = form
        
    def render(self):
        return render_field(self.field, self.form)
    
    
class BaseLayoutObject(object):
    @property
    def lower_name(self):
        return self.__class__.__name__.lower()
    
    @property
    def template(self):
        return 'uni_form/helpers/%s' % self.lower_name

    def render(self, form):
        render_fields = []
        for field in self.fields:
            render_fields.append(FieldRenderer(field, form))
        return self.render_template({'fields': render_fields, 'row': self})
        
    def render_template(self, context):
        selfkey = self.lower_name
        if not selfkey in context:
            context[selfkey] = self
        return render_to_string(self.template, context)