from .models import MC_User


def get_user_by_image_hash(image_hash: str):
  return MC_User.query.filter_by(image_hash=image_hash).first()
