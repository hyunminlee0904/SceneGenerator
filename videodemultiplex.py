import glob
import os
import shutil
import numpy as np
import subprocess

try:
    import cPickle as pickle
except:
    import pickle


from keras.preprocessing.image import img_to_array, load_img


def process_image(image, target_shape):
    """Given an image, process it and return the array."""
    # Load the image.
    h, w, _ = target_shape
    image = load_img(image, target_size=(h, w))

    # Turn it into numpy, normalize and return.
    img_arr = img_to_array(image)
    x = (img_arr / 255.).astype(np.float32)

    return x

def serialize_frames(folder):
    frames = glob.glob(folder+'_jpg/*.jpg')
    for f in frames:
        x = process_image(f, target_shape=[640,480, 3])
        pickle.dump(x, open(f.replace('jpg','pkl'), 'wb'))
    pass

def generate_frames(episode):
    # 1/1 one frame per sec 24/1 24 frames per second
    com = "ffmpeg -i {0}.mkv -r 24/1 ./{0}_jpg/frame_%0d.jpg -n -v 0".format(episode)
    subprocess.call(com, shell=True)

def get_audio(episode):

    com = "ffmpeg -i {0}.mkv -ab 160k -ac 2 -ar 44100 -vn ./{0}_wav/audio.wav -n".format(episode)
    subprocess.call(com.split(), shell=True)

episodes = glob.glob('*.mkv')

for e in episodes:
    ename = e.rstrip('.mkv').split()[0]
    if not os.path.isfile(ename+'.mkv'):
        shutil.move(e, ename+'.mkv')
    #make folder
    #for info in ['_jpg', '_pkl', '_wav']:
    for info in ['_jpg', '_wav']:
        if not os.path.isdir(ename+info):
            os.mkdir(ename+info)


    generate_frames(ename)
    # Pre serilizatrion of frames
    # serialize_frames(ename)
    # strip audio future usage
    get_audio(ename)
