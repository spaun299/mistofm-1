from flask_admin.contrib.sqla import ModelView
from flask_admin.form.upload import ImageUploadField
from flask_admin.form.rules import Field
from flask import Markup
import config
from flask import current_app as app


class AdminView(ModelView):
    form_excluded_columns = ['cr_tm', 'stored_on_server']


class StationView(AdminView):
    column_editable_list = ['name']
    column_searchable_list = ['name']
    column_formatters = {'description_html': lambda view, context, model,
                                                    name: Markup(model.description_html)}


class CustomizableField(Field):
    def __init__(self, field_name, render_field='lib.render_field', field_args={}):
        super(CustomizableField, self).__init__(field_name, render_field)
        self.extra_field_args = field_args

    def __call__(self, form, form_opts=None, field_args={}):
        field_args.update(self.extra_field_args)
        return super(CustomizableField, self).__call__(form, form_opts, field_args)


class ImageView(AdminView):
    column_list = ['image_url', 'stored_on_server']
    create_modal = True
    edit_modal = True
    form_extra_fields = {
        'image_data': ImageUploadField("Image", base_path=config.IMAGES_PATH)
    }

    def _image_preview(self, context, model, name):
        markup_string = '<img src="%s" height=100>' % model.image_url
        return Markup(markup_string)

    form_edit_rules = [
        CustomizableField('stations', field_args={
            'readonly': False
        }),
    ]

    form_ajax_refs = {
        'stations': {
            'fields': ['name'],
            'page_size': 10
        }
    }
    column_formatters = {
        "image_url": _image_preview
    }
