import cv2
import numpy as np
from skimage.segmentation import chan_vese
from skimage import morphology
from scipy import ndimage
from scipy.ndimage import grey_dilation, generate_binary_structure
from skimage.morphology import disk

def bison_mask(bison, window, chan_mu=0.1):
    gray = cv2.cvtColor(bison, cv2.COLOR_RGB2GRAY)
    binary = chan_vese(gray[window[0]:window[1], window[2]:window[3]], mu=chan_mu)
    mask = np.zeros_like(gray).astype('bool')
    mask[window[0]:window[1], window[2]:window[3]] = binary
    structuring_element = disk(5)
    mask = cv2.morphologyEx(mask.astype(np.uint8), cv2.MORPH_CLOSE, structuring_element)
    mask = ndimage.binary_fill_holes(mask)

    return mask


def morphological_reconstruction(marker, mask, connectivity=1):
    """Perform morphological reconstruction of the marker into the mask.
    
    See the Matlab image processing toolbox documentation for details:
    http://www.mathworks.com/help/toolbox/images/f18-16264.html
    """
    sel = generate_binary_structure(marker.ndim, connectivity)
    diff = True
    while diff:
        markernew = grey_dilation(marker, footprint=sel)
        markernew = np.minimum(markernew, mask)
        diff = (markernew - marker).max() > 0
        marker = markernew

    return marker


def hminima(a, thresh):
    """Suppress all minima that are shallower than thresh.

    Parameters
    ----------
    a : array
        The input array on which to perform hminima.
    thresh : float
        Any local minima shallower than this will be flattened.

    Returns
    -------
    out : array
        A copy of the input array with shallow minima suppressed.
    """
    maxval = a.max()
    ainv = maxval - a
    
    return maxval - morphological_reconstruction(ainv-thresh, ainv)