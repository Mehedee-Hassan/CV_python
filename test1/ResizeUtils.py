import numpy # Hint to PyInstaller
from CVForwardCompat import cv2


def cvResizeAspectFill(src, maxSize,
                       upInterpolation=cv2.INTER_LANCZOS4,
                       downInterpolation=cv2.INTER_AREA):
    h, w = src.shape[:2]
    if w > h:
        if w > maxSize:
            interpolation=downInterpolation
        else:
            interpolation=upInterpolation
        h = int(maxSize * h / float(w))
        w = maxSize
    else:
        if h > maxSize:
            interpolation=downInterpolation
        else:
            interpolation=upInterpolation
        w = int(maxSize * w / float(h))
        h = maxSize
    dst = cv2.resize(src, (w, h), interpolation=interpolation)
    return dst

def cvResizeCapture(capture, preferredSize):
    # Try to set the requested dimensions.
    w, h = preferredSize
    successW = capture.set(cv2.cv.CV_CAP_PROP_FRAME_WIDTH, w)
    successH = capture.set(cv2.cv.CV_CAP_PROP_FRAME_HEIGHT, h)
    if successW and successH:
        # The requested dimensions were successfully set.
        # Return the requested dimensions.
        return preferredSize
    # The requested dimensions might not have been set.
    # Return the actual dimensions.
    w = capture.get(cv2.cv.CV_CAP_PROP_FRAME_WIDTH)
    h = capture.get(cv2.cv.CV_CAP_PROP_FRAME_HEIGHT)
    return (w, h)
