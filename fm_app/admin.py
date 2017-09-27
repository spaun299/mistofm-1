from flask_admin.contrib.sqla import ModelView
from flask_admin.form.upload import ImageUploadField
from flask_admin.form.rules import Field
from flask import Markup, g, flash
import config
from werkzeug.utils import secure_filename
from flask import current_app as app
import random


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

    def get_file_name(self, file_data):
        tmp_filename = str(random.getrandbits(128))
        g.tmp_filename = tmp_filename
        return tmp_filename

    form_extra_fields = {
        'image_data': ImageUploadField("Image", base_path=config.IMAGES_PATH, namegen=get_file_name)
    }

    def create_model(self, form):
        """
            Create model from form.

            :param form:
                Form instance
        """
        try:
            model = self.model()
            form.populate_obj(model)
            self.session.add(model)
            self._on_model_change(form, model, True)
            tmp_filename = getattr(g, 'tmp_filename')
            if model.image_url == 'Uploaded' and not tmp_filename:
                flash("Please provide image url or upload it!")
            elif model.image_url != 'Uploaded' and tmp_filename:
                flash("Choose one option: provide image url or upload own. "
                      "Url will be used as picture.")
            if tmp_filename:
                self.session.flush()
                model.rename_filename_to_id(g.tmp_filename)
                model.change_upload_image_url()
                self.session.commit()
                del g.tmp_filename
        except Exception as ex:
            if not self.handle_view_exception(ex):
                pass
            self.session.rollback()
            return False
        else:
            self.after_model_change(form, model, True)
        return model

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
