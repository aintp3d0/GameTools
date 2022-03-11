import os
import hashlib
import functools

from flask import (
  Blueprint, render_template,
  request, session,
  redirect, url_for
)
from werkzeug.utils import secure_filename

from ..src.user.login import UserCredentials

from .models import MC_User
from .query import get_user_by_image_hash
from .forms import MC_User_Form


monster_castle = Blueprint(
  'monster_castle', __name__,
  template_folder='templates/monster_castle',
  static_folder='static/monster_castle'
)


MC_USER_LOGIN_FLAG = 'MC_USER'
MC_USER_IMAGE_FOLDER = os.path.join(
  monster_castle.static_folder,
  'images', 'users'
)

if not os.path.isdir(MC_USER_IMAGE_FOLDER):
  os.makedirs(MC_USER_IMAGE_FOLDER)


def login_required(func):
  @functools.wraps
  def wrapper(*args, **kwargs):
    image_hash = session.get(MC_USER_LOGIN_FLAG)

    if all((image_hash is not None,
            isinstance(image_hash, str),
            get_user_by_image_hash(image_hash) is not None)):
      return func(*args, **kwargs)

    return redirect(url_for('monster_castle.login'))

  return wrapper


def get_image_hash(image_path: str):
  # SEE: https://www.adamsmith.haus/python/answers/how-to-generate-an-md5-hash-for-large-files-in-python
  md5 = hashlib.md5()
  block_size = 128 * md5.block_size

  file = open(image_path, 'rb')
  chunk = file.read(block_size)

  while chunk:
    md5.update(chunk)
    chunk = file.read(block_size)

  return md5.hexdigest()


@monster_castle.route('/login', methods=['GET', 'POST'])
def login():
  """Simple login page with mc_user image
  """
  form = MC_User_Form(meta={'csrf': False})

  if form.validate_on_submit():
    file = form.image.data
    file_path = os.path.join(MC_USER_IMAGE_FOLDER, secure_filename(file.filename))
    file.save(file_path)

    # changed image with the same name
    uc = UserCredentials(file_path)
    uc.save(file_path)

    # hash for the changed image
    file_hash = get_image_hash(file_path)
    new_file_path = os.path.join(os.path.dirname(file_path), file_hash)

    os.rename(file_path, new_file_path)

    session[MC_USER_LOGIN_FLAG] = file_hash

    return redirect(url_for('monster_castle.index'))

  return render_template('login.html', form=form)


# @login_required
@monster_castle.route('/')
def index():
  """
  Registered Users    (accounts)
  Registered Guilds   ()
  """
  return render_template('index.html')


# @login_required
@monster_castle.route('/guild')
def guild():
  return f"guild:: {MC_User.object.query.all()}"
