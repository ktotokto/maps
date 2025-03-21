from pygame import image

def pil_image_to_surface(img):
    mode, size = img.mode, img.size
    data = img.tobytes("raw", mode)
    return image.fromstring(data, size, mode)