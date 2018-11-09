from flask import Flask, render_template, request
from flask_uploads import UploadSet, configure_uploads, IMAGES

app = Flask(__name__)
imageascii = ''

photos = UploadSet('photos', IMAGES)

app.config['UPLOADED_PHOTOS_DEST'] = 'static/img'
configure_uploads(app, photos)

@app.route('/', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST' and 'photo' in request.files:
        filename = photos.save(request.files['photo'])
        runner(request.files['photo'])
        request.files= None
        return render_template('response.html',imageascii=imageascii)
    return render_template('upload.html')


from PIL import Image

ASCII_CHARS = ['.',',',':',';','+','*','?','%','S','#','@']
ASCII_CHARS = ASCII_CHARS[::-1]


def resize(image, new_width=100):
    (old_width, old_height) = image.size
    aspect_ratio = float(old_height)/float(old_width)
    new_height = int(aspect_ratio * new_width)
    new_dim = (new_width, new_height)
    new_image = image.resize(new_dim)
    return new_image

def grayscalify(image):
    return image.convert('L')

def modify(image, buckets=25):
    initial_pixels = list(image.getdata())
    new_pixels = [ASCII_CHARS[pixel_value//buckets] for pixel_value in initial_pixels]
    return ''.join(new_pixels)


def do(image, new_width=100):
    image = resize(image)
    image = grayscalify(image)

    pixels = modify(image)
    len_pixels = len(pixels)

    new_image = [pixels[index:index+new_width] for index in range(0, len_pixels, new_width)]

    return '\n'.join(new_image)

def runner(path):
    global imageascii
    image = None
    try:
        image = Image.open(path)
    except Exception:
        print("Unable to find image in",path)
        #print(e)
        return
    image = do(image)
    imageascii=image

if __name__ == '__main__':
    app.run(debug=True)
