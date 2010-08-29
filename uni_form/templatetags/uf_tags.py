from classytags import core, arguments
from django import template
from django.forms.forms import BoundField
from django.template.loader import render_to_string

register = template.Library()


class Form(core.Tag):
    name = 'uf_form'
    
    options = core.Options(
        arguments.Argument('form'),
        arguments.Argument('action'),
        arguments.Argument('method', required=False, default='post'),
        'classes',
        arguments.MultiValueArgument('classes', required=False),
        'multipart',
        arguments.Flag('multipart', true_values=['true', 'on', 'yes', '1'], default=False),
        blocks=['uf_end_form'],
    )
    
    def render_tag(self, context, form, action, method, classes, multipart, uf_end_form):
        context.push()
        context['form'] = form
        context['action'] = action
        context['method'] = method
        context['multipart'] = multipart
        inner = uf_end_form.render(context)
        context['inner'] = inner
        output = render_to_string('uni_form/uf_tags/form.html', context)
        context.pop()
        return output
register.tag(Form)


class BaseInputTag(core.Tag):
    options = core.Options(
        arguments.Argument('name'),
        arguments.Argument('value'),
        'classes',
        arguments.MultiValueArgument('classes', required=False),
    )

    input_type = 'button'
    field_classes = ['button']
    
    def render_tag(self, context, name, value, classes):
        context.push()
        context['name'] = name
        context['value'] = value
        context['classes'] = classes + self.field_classes
        context['type'] = self.input_type
        output = render_to_string('uni_form/uf_tags/input.html', context)
        context.pop()
        return output


class Submit(BaseInputTag):
    name = 'uf_submit'
    input_type = 'submit'
    field_classes = ['submit', 'submitButton']
register.tag(Submit)


class Button(BaseInputTag):
    name = 'uf_button'
    input_type = 'button'
    field_classes = 'button'
register.tag(Button)


class Hidden(BaseInputTag):
    name = 'uf_hidden'
    input_type = 'hidden'
    field_classes = ['hidden']
register.tag(Hidden)


class Reset(BaseInputTag):
    name = 'uf_reset'
    input_type = 'reset'
    field_classes = ['reset', 'resetButton']
register.tag(Reset)


class Fieldset(core.Tag):
    name = 'uf_fieldset'
    options = core.Options(
        arguments.Argument('legend', required=False, default=""),
        'classes',
        arguments.MultiValueArgument('classes', required=False),
        blocks=['uf_end_fieldset']
    )
    
    def render_tag(self, context, legend, classes, uf_end_fieldset):
        context.push()
        context['legend'] = legend
        context['classes'] = classes
        inner = uf_end_fieldset.render(context)
        context['inner'] = inner
        output = render_to_string('uni_form/uf_tags/fieldset.html', context)
        context.pop()
        return output
register.tag(Fieldset)


class Field(core.Tag):
    name = 'uf_field'
    options = core.Options(
        arguments.Argument('name'),
        'classes',
        arguments.MultiValueArgument('classes', required=False),
    )

    def render_tag(self, context, name, classes):
        context.push()
        context['name'] = name
        context['classes'] = classes
        form = context['form']
        context['field'] = BoundField(form, form.fields[name], name)
        output = render_to_string('uni_form/uf_tags/field.html', context)
        context.pop()
        return output
register.tag(Field)


class Row(core.Tag):
    name = 'uf_row'
    options = core.Options(
        'classes',
        arguments.MultiValueArgument('classes', required=False),
        blocks=['uf_end_row']
    )
    
    def render_tag(self, context, classes, uf_end_row):
        context.push()
        context['classes'] = classes
        inner = uf_end_row.render(context)
        context['inner'] = inner
        output = render_to_string('uni_form/uf_tags/row.html', context)
        context.pop()
        return output
register.tag(Row)


class Column(core.Tag):
    name = 'uf_column'
    options = core.Options(
        'classes',
        arguments.MultiValueArgument('classes', required=False),
        blocks=['uf_end_column']
    )
    
    def render_tag(self, context, classes, uf_end_column):
        context.push()
        context['classes'] = classes
        inner = uf_end_column.render(context)
        context['inner'] = inner
        output = render_to_string('uni_form/uf_tags/column.html', context)
        context.pop()
        return output
register.tag(Column)