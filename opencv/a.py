import os.path as path

import cv2

img_file_path = path.abspath(path.join(path.dirname(__file__), 'gopher.png'))
img = cv2.imread(img_file_path, 0)

cv2.imshow('image', img)
k = cv2.waitKey(0)

if k == ord('s'):
    cv2.imwrite('new-gopher.png', img)

cv2.destroyAllWindows()
