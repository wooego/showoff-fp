#coding:utf-8
from os import environ as env

DEBUG = True
FRONTEND_TITLE = env.get('GALLERY_TITLE') or u'我的家庭相册'
FRONTEND_HOST = '0.0.0.0' #not used in production
FRONTEND_PORT = 5050 #not used in production
FRONTEND_BASEURL = 'http://photo' #not used in production
FRONTEND_PREFIX = '/gallery'
FRONTEND_FCGI_SOCKET = '/home/fp862/workspaces/showoff/frontend.sock' #not used in production
ADMIN_TITLE = u'管理家庭相册'
ADMIN_HOST = '0.0.0.0' #not used in production
ADMIN_PORT = 5051   #not used in production
ADMIN_BASEURL = 'http://photo' #not used in production
ADMIN_PREFIX = '/admin'
ADMIN_FCGI_SOCKET = '/home/fp862/workspaces/showoff/admin.sock' #not used in production
ADMIN_LOGFILE=u'/mnt/acer_data/showoff_config/showoff.log'
THUMBNAIL_SIZE = 400
GRID_SIZE = 200
ADMIN_THUMBNAIL_SIZE = 400
THUMBNAILS_PER_PAGE = 20
THUMBNAILS_PER_SMALL_LIST = 8
ADMIN_THUMBNAILS_PER_PAGE = 12
ADMIN_GRID_ITEMS_PER_PAGE = 50
FRONTEND_GRID_ITEMS_PER_PAGE = 50
IMAGE_SIZE = 800
ALLOWED_SIZES = [75, 200, 400, 500, 640, 800, 1024, 1600, 'full']
THEME = 'v2'
ADMIN_THEME = 'v2'
CACHE_DIR = u'/mnt/acer_data/showoff_config/cache'
EDITS_DIR = u'/mnt/acer_data/showoff_config/edits'
SHOWS_DIR = u'/mnt/acer_data/showoff_config/shows'
ALBUMS_DIR = env.get('ALBUMS_DIR') or u'/mnt/acer_data/pictures'
SECRET_KEY = env.get('SECRET_KEY') or 'secret_key'
FRONTEND_LIST_TEMPLATES = ['list', 'list_small', 'grid', 'galleria']
