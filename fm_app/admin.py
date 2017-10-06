from flask_admin.contrib.sqla import ModelView
from wtforms.validators import NumberRange
from flask_admin.form.upload import ImageUploadField
from flask_admin.form.rules import Field
from flask_admin.base import AdminIndexView
from flask_admin.contrib.sqla.ajax import QueryAjaxModelLoader
from flask_admin import expose
from flask import Markup, g, flash, current_app as app, redirect, url_for
from wtforms.fields.simple import PasswordField
import config
from utils import get_db_session, get_database_uri
from .models import Playlist
from flask_user import current_user, login_required


class IndexView(AdminIndexView):
    @expose()
    @login_required
    def index(self):
        return self.render(self._template)


class AdminView(ModelView):
    form_excluded_columns = ['cr_tm', 'stored_on_server']

    @staticmethod
    def _image_preview(obj, context, model, name, img_height=100):
        markup_string = '<img src="{url}" height={height}>'.format(url=model.image_url,
                                                                   height=img_height)
        return Markup(markup_string)

    def is_accessible(self):
        return current_user.is_authenticated and current_user.user_type == 'admin'

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('index.station'))


class StationIcesView(AdminView):
    # form_choices = {'bitrate': [(16, 16), (32, 32), (64, 64), (128, 128), (256, 256)]}

    form_ajax_refs = {'playlists': QueryAjaxModelLoader(
        'playlists', get_db_session(get_database_uri(
            config.DB_HOST, config.DB_USERNAME,
            config.DB_PASSWORD, config.DB_NAME)), Playlist,
        filters=["station_id is NULL"], fields=['name'])}
    form_extra_fields = {
        'password': PasswordField('Password')
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
            model.save()
        except Exception as e:
            flash(e)
            return False
        return model


class PlaylistMusicView(AdminView):
    column_filters = ['playlist.name', 'song.song_name']
    column_searchable_list = ['playlist.name', 'song.song_name']


class MusicView(AdminView):
    column_searchable_list = ['song_name']
    form_excluded_columns = ['playlist_assoc']


class PlaylistView(AdminView):
    form_excluded_columns = ['music_assoc']
    validate_hours = NumberRange(1, 24, "Value should be from 1 to 24")
    form_args = {"play_from_hour": {"validators": [validate_hours, ]},
                 "play_to_hour": {"validators": [validate_hours, ]}}
    column_filters = ['name']
    # def create_model(self, form):
    #     model = self.model(**form.data)
    #     model.save()


class StationView(AdminView):

    column_editable_list = ['name']
    column_searchable_list = ['name']
    column_formatters = {'description_html': lambda view, context, model,
                                                    name: Markup(model.description_html),
                         'images': lambda view, context, model,
                                                    name: AdminView._image_preview(
                             view, context, model, name, 40
                         )}


class CustomizableField(Field):
    def __init__(self, field_name, render_field='lib.render_field', field_args={}):
        super(CustomizableField, self).__init__(field_name, render_field)
        self.extra_field_args = field_args

    def __call__(self, form, form_opts=None, field_args={}):
        field_args.update(self.extra_field_args)
        return super(CustomizableField, self).__call__(form, form_opts, field_args)


class ImageView(AdminView):
    column_list = ['image_url', 'name', 'stored_on_server']
    create_modal = True
    edit_modal = True

    def get_file_name(self, file_data):
        return app.root_path + g.image_url

    form_extra_fields = {
        'image_data': ImageUploadField("Image", base_path=config.IMAGES_PATH,
                                       namegen=get_file_name)
    }

    def create_model(self, form):
        """
            Create model from form.

            :param form:
                Form instance
        """
        try:
            model = self.model()
            uploaded = bool(form.data.get('image_data'))
            model.image_url = form.data.get('image_url')
            model.name = form.data.get('name')
            if not (model.image_url or uploaded):
                flash("Please provide image url or upload it!")
                return False
            elif model.image_url and uploaded:
                flash("Choose one option: provide image url or upload own. "
                      "Url will be used as a picture.")
                uploaded = False
                del form.data['image_data']
            self.session.add(model)
            if uploaded:
                model.image_url = "tmp"
                model.stored_on_server = True
                self.session.flush()
                try:
                    file_ext = form.data['image_data'].filename.split('.')[-1]
                except IndexError:
                    file_ext = 'png'
                model.image_url = model.get_stored_image_url(file_ext)
                g.image_url = model.image_url
                form.data['image_url'] = model.image_url
                form.image_data.populate_obj(model, 'image_data')
                self.session.add(model)
            self._on_model_change(form, model, True)
            self.session.commit()
        except Exception as ex:
            if not self.handle_view_exception(ex):
                pass
            self.session.rollback()
            return False
        else:
            self.after_model_change(form, model, True)
        return model

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
        "image_url": AdminView._image_preview
    }
