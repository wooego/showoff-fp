#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Showoff - Webbased photo album software

Copyright (c) 2010-2014 by Jochem Kossen <jochem@jkossen.nl>

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are
met:

   1. Redistributions of source code must retain the above copyright
   notice, this list of conditions and the following disclaimer.
   2. Redistributions in binary form must reproduce the above
   copyright notice, this list of conditions and the following
   disclaimer in the documentation and/or other materials provided
   with the distribution.

THIS SOFTWARE IS PROVIDED BY THE AUTHOR AND CONTRIBUTORS ``AS IS'' AND
ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR
PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE AUTHOR OR CONTRIBUTORS
BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR
BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY,
WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE
OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN
IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

"""

from flask import Blueprint, current_app, render_template, \
    send_from_directory, url_for, redirect, jsonify, request, \
    session
from werkzeug.utils import secure_filename
from pypinyin import lazy_pinyin
from showoff.lib import Show, Image, CacheManager, ExifManager
from showoff.admin.lib import ImageModifier
from showoff.admin.lib.page import _paginated_overview

import os
import re
import datetime

admin = Blueprint('admin', __name__, template_folder='templates')


def render_themed(template, **options):
    template_path = os.path.join(current_app.config['ADMIN_THEME'], template)
    return render_template(template_path, **options)

def allowed_file(filename):
    ALLOWED_EXTENSIONS = set(['mp4','bmp','png', 'jpg', 'jpeg', 'gif'])
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


@admin.route('/static_files/<path:filename>')
def static_files(filename):
    """Send static files such as style sheets, JavaScript, etc."""
    static_path = os.path.join(admin.root_path,
                               'templates',
                               current_app.config['ADMIN_THEME'],
                               'static')
    return send_from_directory(static_path, filename)


@admin.route('/<album>/image/<filename>/<int:size>/')
def show_image(album, filename, size=None):
    image = Image(album, filename, current_app.config)
    cache = CacheManager(image, current_app.config)
    return send_from_directory(*cache.get(size))


@admin.route('/<album>/image/<filename>/full/')
def show_image_full(album, filename):
    return show_image(album, filename, 'full')


@admin.route('/<album>/show/<filename>')
def image_page(album, filename):
    show = Show(album, current_app.config, session)
    image = Image(album, filename, current_app.config)
    exif_manager = ExifManager(image)
    exif_array = exif_manager.get_exif()
    if exif_array is None:
        exif_array = {}
    return render_themed('image.html', album=album, filename=filename,
                         exif=exif_array, show=show)


@admin.route('/<album>/rotate_exif/')
def rotate_url():
    # dummy
    pass


@admin.route('/new_album', methods=['GET','POST'])
def new_album():
    album_name = request.args.get('album_name','unkown',type=unicode)
    try:
        os.mkdir(os.path.join(current_app.config['ALBUMS_DIR'],album_name))
    except OSError:
        pass
    return redirect(url_for('.show_index'))


@admin.route('/<album>/list/<template>/<int:page>/')
@admin.route('/<album>/list/<int:page>/')
def list_album(album, page, template='grid'):
    show = Show(album, current_app.config, session)
    ext = re.compile(".(jpg|png|gif|bmp)$", re.IGNORECASE)

    album_dir = os.path.join(current_app.config['ALBUMS_DIR'], album)
    all_files = [f for f in os.listdir(album_dir) if ext.search(f)]
    all_files.sort()

    if show.get_setting('reverse') == 'yes':
        all_files.reverse()

    paginator = _paginated_overview(album, page, 'admin.list_album', template)
    return render_themed(template + '.html',
                         album=album,
                         show=show,
                         files=paginator.entries,
                         paginator=paginator,
                         page=page,
                         all_files=all_files)


@admin.route('/<album>/')
def show_album(album):
    return list_album(album, 1)


@admin.route('/<album>/upload', methods=['GET','POST'])
def upload(album):
    if request.method == 'POST':
        files = request.files.getlist('uploads')
        for f in files:
            if f and allowed_file(f.filename):
                filename = secure_filename(f.filename)
                if filename.startswith('.') or '.' not in filename:
                    name = f.filename.split('.')[0]
                    ext = f.filename.split('.')[1]
                    filename = '_'.join(lazy_pinyin(name)) + '.' + ext
                current_app.logger.info('save file "{}" to album "{}"'.format(filename,album))
                f.save(os.path.join(current_app.config['ALBUMS_DIR'], album,"{}-{}".format(str(datetime.date.today()), filename)))
    return redirect(url_for('.show_album',album=album))


@admin.route('/')
def show_index():
    dir_list = os.listdir(current_app.config['ALBUMS_DIR'])
    album_list = [os.path.basename(album) for album in dir_list]
    album_list.sort(reverse=True)
    return render_themed('index.html', albums=album_list)


@admin.route('/<album>/<filename>/rotate/<int:steps>/')
def image_rotate(album, filename, steps=1):
    image = Image(album, filename, current_app.config)
    image_modifier = ImageModifier(image,config=current_app.config)
    image_modifier.rotate(steps)
    return jsonify(result='OK')


@admin.route('/<album>/rotate_exif/<filename>/')
def exif_rotate_image(album, filename):
    image = Image(album, filename, current_app.config)
    image_modifier = ImageModifier(image,config=current_app.config)
    image_modifier.rotate_exif()
    return jsonify(result='OK')


@admin.route('/<album>/<filename>/toggle_publish/')
def toggle_publish_image(album, filename):
    """Toggle publish image"""
    show = Show(album, current_app.config, session)
    try:
        show.toggle_image(filename).save()
    except:
        return jsonify(result='Failed')

    return jsonify(result='OK')

@admin.route('/<album>/add_image_to_show/<filename>/')
def add_image_to_show(album, filename):
    """Add an image to the show"""
    show = Show(album, current_app.config, session)
    try:
        show.add_image(filename).save()
    except:
        return jsonify(result='Failed')

    return jsonify(result='OK')


@admin.route('/<album>/remove_image_from_show/<filename>/')
def remove_image_from_show(album, filename):
    """Remove an image from the show"""
    show = Show(album, current_app.config, session)

    try:
        show.remove_image(filename).save()
    except:
        return jsonify(result='Failed')

    return jsonify(result='OK')

@admin.route('/<album>/sort_by_exifdate/')
def sort_show_by_exifdate(album):
    """Sort the show by exif datetime """
    show = Show(album, current_app.config, session)
    show.sort_by_exif_datetime().save()
    return goback(True)

@admin.route('/<album>/sort_by_filename/')
def sort_show_by_filename(album):
    """Sort the show by filename """
    show = Show(album, current_app.config, session)
    show.sort_by_filename().save()
    return goback(True)

@admin.route('/<album>/edit_users/')
def show_edit_users(album):
    show = Show(album, current_app.config, session)
    users = show.data['users']
    return render_themed('edit_users.html',
                         album=album,
                         show=show,
                         users=users)


@admin.route('/<album>/add_all/')
def add_all_images_to_show(album):
    show = Show(album, current_app.config, session)
    show.add_all_images().save()
    return goback(True)


@admin.route('/<album>/set/<setting>/<value>/')
def show_change_setting(album, setting, value):
    show = Show(album, current_app.config, session)
    try:
        show.change_setting(setting, value).save()
    except:
        return jsonify(result='Failed')
    return jsonify(result='OK')

@admin.route('/<album>/change_password/', methods=['POST'])
def show_change_password(album):
    if request.method == 'POST':
        show = Show(album, current_app.config, session)
        username = request.form['username']
        password = request.form['password']
        show.set_user(username, current_app.config['SECRET_KEY'], password).save()
        return goback(True)


@admin.route('/<album>/remove_user/<username>/')
def show_remove_user(album, username):
    show = Show(album, current_app.config, session)
    show.remove_user(username).save()
    return jsonify(result='OK')

def goback(is_ok):
    if is_ok:
        return redirect(request.referrer or url_for('.index'))
    else:
        return jsonify(result='Failed')
