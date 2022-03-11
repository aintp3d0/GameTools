import os

import cv2
import numpy

# from helper import show_image


class UserCredentials:

  def __init__(self, image_path: str):
    self.image_path = image_path

  def crop_user_creds(self, image: numpy.ndarray) -> numpy.ndarray:
    y1 = 230
    y2 = y1 + 80
    x1 = 725
    x2 = x1 + 980
    image = image[y1:y2, x1:x2]
    return image

  def get_user_name(self, image: numpy.ndarray) -> numpy.ndarray:
    """Cropping the user name by contours
    """
    # SEE: https://medium.com/analytics-vidhya/how-to-detect-tables-in-images-using-opencv-and-python-6a0f15e560c3
    image = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
    _, thresh_value = cv2.threshold(image, 180, 255, cv2.THRESH_BINARY_INV)
    contours, hierarchy = cv2.findContours(
      thresh_value,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE
    )
    xs = {}

    for cnt in contours:
      x, y, w, h = cv2.boundingRect(cnt)
      xs[x] = (x, y, w, h)

    prev_word = None
    word_distance = 30

    for i in sorted(xs.keys()):
      if prev_word is None:
        prev_word = i
        continue

      new_word = (i - prev_word)
      if new_word > word_distance:
        break

      prev_word = i

    x, _, w, _ = xs.get(prev_word)
    x2 = (x + w) + word_distance
    image = image[:, :x2]
    return image

  def get(self) -> numpy.ndarray:
    """Getting the user credentials from the given image
    """
    image = cv2.imread(self.image_path)
    image = self.crop_user_creds(image)

    image = self.get_user_name(image)
    return image

  def save(self, image_path: str):
    image = self.get()
    cv2.imwrite(image_path, image)


def main():
  image_path = os.path.join('user', 'static', 'test.jpg')
  uc = UserCredentials(image_path)
  image = uc.get()
  show_image(image)


if __name__ == '__main__':
  main()
