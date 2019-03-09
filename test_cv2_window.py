from __future__ import print_function

from pygrabber.dshow_graph import FilterGraph
import cv2

# tested  and works with Python 3, works not in Python 2

def show_image(image):
	cv2.imshow("Image", image)

graph = FilterGraph()
cv2.namedWindow('Image', cv2.WINDOW_NORMAL)
graph.add_input_device(0)
graph.add_sample_grabber(show_image)
graph.add_null_render()
graph.prepare()
graph.run()
print("Press 'q' or 'ESC' to exit")
k = cv2.waitKey(1)
while k not in [27, ord('q')]:
    graph.grab_frame()
    k = cv2.waitKey(1)
graph.stop()
cv2.destroyAllWindows()
print("Done")