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
                 extensions=('JPG', 'CR2', 'ORF', 'ARW', 'TIFF', 'DNG'),
                 batch_size=300,
                 encoder = coder_grey
                 ignore=None):

        # Init
        self.extensions = extensions
        self.ignore = ignore
        self.BATCH_SIZE = batch_size
        self.encoder = encoder
        self._indexed = list()
        self._index = 0
        self._delivered = dict()

        if path:
            self.indexing_data


    def next_batch(self):

        batch = list()
        training_batch =  self._indexed[self._index*self.BATCH_SIZE:(slef._index+1)*self.BATCH_SIZE]
        for training in training_batch:
            batch.append(self.encoder(training))
        self._index += 1
        return np.array(batch)

    def indexing_files(self):
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


        for (dirpath, dirnames, filenames) in os.walk(self.path):
            for f in filenames:
                if f.upper().endswith(self.extensions):
                    # source_files.append(os.path.join(dirpath, f))
                    parent = os.path.basename(os.path.normpath(dirpath))
                    self._indexed.append({'dir':dirpath,
                                         'filename':f,
                                         'parent_folder':parent})

        return


# coders

def coder_grey(file_path):
    pixels = 125
    im = Image.open(file_path)
    im = ImageOps.fit(im, (pixels, pixels), Image.ANTIALIAS)
    im = ImageOps.grayscale(im)
    im = np.asarray(im)
    im = (im - 127.5)/127.5

    return im
