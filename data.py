import os
import argparse
import shutil
import hashlib
import string
import random
import re
import glob
import numpy as np
from PIL import Image, ImageOps


class Data_Supplier(object):
    """docstring forSupplier."""

    def __init__(self,
                 path=None,
                 extensions=('JPG'),
                 batch_size=300,
                 encoder=None,
                 ignore=None):

        # Init
        self.extensions = extensions
        self.ignore = ignore
        self.BATCH_SIZE = batch_size
        self.batches = 0

        self.encoder = encoder
        self._training_dataset = list()
        self._index = 0

        if path:
            self.indexing_data(path)

    def next_batch(self):
        """Return next batch of training data.


        Returns
        -------

        """
        if self.encoder:
            next_batch = list()
            training_batch = self._training_dataset[self._index *
                                                    self.BATCH_SIZE:(self._index + 1) * 
                                                    self.BATCH_SIZE]
            for training in training_batch:
                next_batch.append(self.encoder(training))
            self._index += 1
            # redimension
            next_batch = np.array(next_batch)
            return next_batch.reshape((next_batch.shape[0], 1) + next_batch.shape[1:])

    def indexing_data(self, path):
        """Walk the source folder and select potential photos by extension.
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

        for (dirpath, dirnames, filenames) in os.walk(path):
            for f in filenames:
                if f.upper().endswith(self.extensions):
                    # source_files.append(os.path.join(dirpath, f))
                    # ({'dir':dirpath,
                    #'filename':f,
                    #'parent_folder':parent})
                    f = os.path.join(dirpath, f)
                    # parent = os.path.basename(os.path.normpath(dirpath))
                    self._training_dataset.append(f)

        self.batches = int(len(self._training_dataset) / self.batch_size)

        return


# coders

def coder_grey(file_path):
    pixels = 125
    im = Image.open(file_path)
    im = ImageOps.fit(im, (pixels, pixels), Image.ANTIALIAS)
    im = ImageOps.grayscale(im)
    im = np.asarray(im)
    im = (im - 127.5) / 127.5

    return im
