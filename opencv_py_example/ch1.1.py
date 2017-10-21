import cv2

# print [x for x in dit(cv2) if x.strtswitch('COLOR_')]
print [x for x in dir(cv2) if x.startswith('COLOR_')]