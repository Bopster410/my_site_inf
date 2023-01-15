from project import app
from PIL import Image
import secrets, os

def save_image(form_image, path):
    # Generating a new name image_fn
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_image.filename)
    image_fn = random_hex + f_ext
    # Resizing and saving an image in profile_pics
    image_path = os.path.join(app.root_path, f'static/{path}', image_fn)
    output_size = (250, 250) 
    i = Image.open(form_image)
    i.thumbnail(output_size)
    i.save(image_path)
    return image_fn
