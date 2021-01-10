import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    SECRET_KEY = os.environ.get('') or 'LYK'

    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
    'sqlite:///' + os.path.join(basedir, 'LYK_algorithm.db')

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    AVATAR_UPLOAD_DIR = os.path.join(basedir, 'static\\uploaded_AVATAR')
    CODE_UPLOAD_DIR = os.path.join(basedir, 'static\\uploaded_CODE')
