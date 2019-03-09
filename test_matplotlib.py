from __future__ import print_function
from builtins import input

from pygrabber.dshow_graph import FilterGraph
import cv2

# tested with Python 3, works not in Python 2

import threading, time
import matplotlib.pyplot as plt
import numpy as np
from pygrabber.dshow_graph import FilterGraph

# tested and works with Python 3, works not in Python 2

image_done = threading.Event()
image_grabbed = None

def img_cb(image):
    global image_done
    global image_grabbed
    image_grabbed = np.flip(image, 2)
    image_done.set()

graph = FilterGraph()
graph.add_input_device(0)
graph.add_sample_grabber(img_cb)
graph.add_null_render()
graph.prepare()
graph.run()
time.sleep(2)
graph.grab_frame()
image_done.wait(1000)
graph.stop()
plt.imshow(image_grabbed)
plt.show()