import os
import argparse
import shutil
import hashlib
import string
import random
import re
import glob
import numpy as np
from collections import defaultdict
from PIL import Image, ImageOps


class Data_Supplier(object):
    """Data Supplier. We want data, and we want it now and in order

    Class to index and supply frames in a consisten maner. The frames must be
    supplied in order. This class will allow us to get that data in a flexible
    manner

    """

    def __init__(self,
                 path=None,
                 batch_size=300,
                 encoder=None):

        # Init
        self.BATCH_SIZE = batch_size
        self.batches = 0
        self.encoder = encoder
        self._training_dataset = list()
        self._index = 0

        if path:
            self.indexing_data(path)

    def next_batch(self, sequence = 24, step=1):
        """Return next batch of training data.

        Default return a batch all 24 frames in 1 second of animation
        125 X 125 X sequence
        sequence  : int
            Number of animations we want to fetch
        step : int
            Skip frames

        Returns
        -------

        """
        if self.encoder:
            next_batch = list()
            group = list()
            training_batch = self._training_dataset[self._index *
                                                    self.BATCH_SIZE *
                                                    sequence *
                                                    step:(self._index + 1) *
                                                    self.BATCH_SIZE *
                                                    sequence *
                                                    step]

            for training in range(training_batch, step):
                if len(group) < sequence:
                    group.append(self.encoder(training))
                    self._index += step
                else:
                    next_batch.append(np.array(group))
                    group = list()

                # redimension
            next_batch = np.array(next_batch)
            return next_batch.reshape((next_batch.shape[0], 1) + next_batch.shape[1:])



    def indexing_data(self, path):
        """Walk the source folder and index frames.
        Parameters
        ----------
        source_path : str
            Source path
        Returns
        -------
        """
        # combinedignored = re.compile('|'.join('(?:{0})'.format(x) for x in ignore))
        # use endswith , ignore must be a tuple then
        # if ignore and dirpath.endswith(ignore):
        # for duplication, at the end cll the same funciton
        buffer_temp = defaultdict(list)
        for (dirpath, dirnames, filenames) in os.walk(path):
            for f in filenames:
                if f.upper().endswith('JPG'):
                    # source_files.append(os.path.join(dirpath, f))
                    # ({'dir':dirpath,
                    #'filename':f,
                    #'parent_folder':parent})
                    f = os.path.join(dirpath, f)
                    # parent directoy is the episode code
                    parent = os.path.basename(os.path.normpath(dirpath))
                    episode = parent.replace('_jpg','')
                    frame = int(f.replace('frame_','').replace('.jpg',''))

                    buffer_temp[episode].append({'frame':frame,'file':f})

        # Sort data
        for epis in buffer_temp:
            sorted_epis = [ x['file'] for x in sorted(epis, key=lambda k: k['frame'])]
            self._training_dataset.extend(sorted_epis)

        self.batches = int(len(self._training_dataset) / self.batch_size)

        return

    def shuffle(self):

        random.shuffle(self._training_dataset)

    def reset(self):
        self._index = 0


# coders

def coder_grey(file_path, pixels = 128):

    im = Image.open(file_path)
    im = ImageOps.fit(im, (pixels, pixels), Image.ANTIALIAS)
    im = ImageOps.grayscale(im)
    im = np.asarray(im)
    im = (im - 127.5) / 127.5

    return im
