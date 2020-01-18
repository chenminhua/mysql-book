import tensorflow as tf
import random


def convert2int(image):
    # transfer from [-1,1] to [0,255]
    return tf.image.convert_image_dtype((image + 1.0) / 2.0, tf.uint8)


def convert2float(image):
    # transfer from [0,255] to [-1,1]
    image = tf.image.convert_image_dtype(image, dtype=tf.float32)
    return (image / 127.5) - 1.0


def batch_convert2int(images):
    # Args images: 4D float tensor (batch_size, image_size, image_size, depth)
    return tf.map_fn(convert2int, images, dtype=tf.uint8)


def batch_convert2float(images):
    # Args images: 4D float tensor (batch_size, image_size, image_size, depth)
    return tf.map_fn(convert2float, images, dtype=tf.float32)


class ImagePool:
    """history of generated images"""
    def __init__(self, pool_size):
        self.pool_size = pool_size
        self.images = []

    def query(self, image):
        if self.pool_size == 0:
            return image

        if len(self.images) < self.pool_size:
            self.images.append(image)
            return image
        else:
            # if hit the pool capacity, replace an old image in 0.5 probability
            p = random.random()
            if p > 0.5:
                random_id = random.randrange(0, self.pool_size)
                tmp = self.images[random_id].copy()
                self.images[random_id] = image.copy()
                return tmp
            else:
                return image

