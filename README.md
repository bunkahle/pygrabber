# pygrabber
===========

Python tool to capture photo from camera and for doing simple image processing using DirectShow and OpenCV

See https://www.codeproject.com/Articles/1274094/%2FArticles%2F1274094%2FCapturing-images-from-camera-using-Python-and-Dire
and the original repository at:
https://github.com/andreaschiavinato/python_grabber

Modifications made to work under Python 2 and 3.

Introduction
============

Using OpenCV in Python is a very good solution to prototype vision applications, it allows you to quickly draft and test algorithms. It’s very easy to process images read from files, not so easy if you want to process images captured from a camera. OpenCV provides some basic methods to access the camera linked to the PC (through the object VideoCapture), but most of the time, they aren’t enough even for a simply prototype. For instance, it’s not possible to list all the cameras linked to the PC and there isn’t a quick way to tune the parameters of the camera. Alternatively, you can use PyGame or the SDK provided by the camera manufacturer, if available.

In Windows to interact with the cameras, DirectShow is often used. Its main strengths are:

- Almost any camera provides a driver that allows it to be used from DirectShow.
- It’s a technology well established and widely used.
- It’s based on the COM framework, so it is designed to be used from different programming languages.

Conversely, it’s quite an old technology that is being replaced by the Windows Media Foundation and Microsoft is not developing it anymore. But it’s not a big deal because it has all the features needed and it’s used in so many applications that (in my opinion), Microsoft will keep it available for a long time.

Here, I want to propose a simple application written entirely in Python that allows you to capture images from a camera using DirectShow, display them on screen and perform simple processing on them using OpenCV. The application is based on a class that exposes some of the functionalities of DirectShow and that can be reused in other applications. The code is designed to be easy to change and to expand.

You can find the code of the application also on https://github.com/andreaschiavinato/python_grabber .
Background

To understand this article, you need basic knowledge of Python and of the Windows application development.
Using the Application

1. Make sure the following Python packages are installed: numpy, matplotlib, opencv-python, comtypes.
2. Run main.py.
3. Once the application is started, the dialog Select a video device is shown. Select a camera, then press Ok.
4. A screen that allows you to select the camera resolution will be shown. Select the desired resolution or leave the default values and press Ok.
5. The camera live stream is shown on the left part of the screen.
6. Press Grab to capure a photo, the photo will be shown on the right part of the screen. You can apply some filters to the photo using the buttons on the right part of the screen or save the picture pressing Save.


On Windows 10, if the size of text has been set to a value different from 100% (on the Display settings screen of Windows), the live image of the camera may show not well aligned on the containing frame. This seems an issue of DirectShow, since I have the same behaviour on other applications.

DirectShow in Short Words
=========================

DirectShow is a framework to write multimedia applications. The building block of a DirectShow application is a filter, an object that performs a base operation like:

- Reading audio\video from a camera or a file
- Converting an audio\video from a format to another one
- Rendering audio\video to the screen or to a file

The filters can have input and output pins, and they can be connected together in order to perform the required job

DirectShow provides an object called Filter Graph that is responsible to collect the filters, link them and run them.

For our application, we need the following filters:

- A camera source filter, that reads the images from the camera
- A SampleGrabber filter that allows us to do some operation on each frame provided by the camera
- A video render filter that displays the live stream of the camera on the GUI

Depending on the camera, we may need additional filters to convert the images provided by the camera in images that can be used by the SampleGrabber. These additional filters are added automatically by directshow.

If you want to learn more about DirectShow, it's worth reading the documentation provided by Microsoft.

Using the Class FilterGraph
===========================

You can use the class FilterGraph (contained in the file dshow_graph.py) as standalone. The class represent a DirectShow Filter Graph object.

Example 1
---------

This code lists the cameras connected to your PC:


	# tested under Python 2 and 3

	from __future__ import print_function
	from pygrabber.dshow_graph import FilterGraph

	graph = FilterGraph()
	print(graph.get_input_devices())


Example 2
---------

This code shows a screen with the live image from the first camera in your PC.

We add to the graph two filters: one is a source filter corresponding to the first camera connected to your PC, the second is the default render, that shows the images from the camera in a window on the screen. Then we call prepare, that connects the two filters together, and run, to execute the graph.

Finally, we need a method to pause the program while watching the camera video. I use the Tkinter mainloop function which fetches and handles Windows events, so the application doesn’t seem frozen.

	from __future__ import print_function

	from pygrabber.dshow_graph import FilterGraph
	from tkinter import Tk, Message

	# tested under Python 2 and 3

	def on_closing(event=0):
		graph.stop()
		try:
			root.destroy()
		except:
			pass

	graph = FilterGraph()
	graph.add_input_device(0)
	graph.add_default_render()
	graph.prepare()
	graph.run()
	root = Tk()
	w = Message(root, text="Close this window for stopping the program")
	w.pack()
	root.protocol("WM_DELETE_WINDOW", on_closing)
	# root.withdraw() # hide Tkinter main window
	root.mainloop()
	
Example 3
---------

The following code uses the sample grabber filter to capture single images from the camera. To capture an image, the method grab_frame is called. The image will be retrieved from the callback function passed as parameter to the add_sample_grabber method. In this case, the image captured is shown using the function imshow of opencv.

	from __future__ import print_function

	from pygrabber.dshow_graph import FilterGraph
	import cv2

	# tested and works with Python 3, works not in Python 2

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

Example 4
---------

The following code captures an image from a camera in a synchronous way. An Event object is used to block the main thread until the image is ready.

The image is shown using matplotlib. Note that the function np.flip is used to invert the last dimension of the image, since the image returned by the sample grabber filter has the BGR format, but mathplotlib requires the RGB fromat. We didn't do this on the previous example since OpenCV accepts the format BGR.

	from __future__ import print_function
	from builtins import input

	from pygrabber.dshow_graph import FilterGraph
	import cv2
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

Example 5
---------

The following code is an improvement of Example 4 that allows you to capture images from two camera at the same time.

	from __future__ import print_function
	import threading
	import matplotlib.pyplot as plt
	import numpy as np
	from pygrabber.dshow_graph import FilterGraph

	class Camera:
	    def __init__(self, device_id):
	        self.graph = FilterGraph()
	        self.graph.add_input_device(device_id)
	        self.graph.add_sample_grabber(self.img_cb)
	        self.graph.add_null_render()
	        self.graph.display_format_dialog()
	        self.graph.prepare()
	        self.graph.run()

	        self.image_grabbed = None
	        self.image_done = threading.Event()

	    def img_cb(self, image):
	        self.image_grabbed = np.flip(image, 2)
	        self.image_done.set()

	    def capture(self):
	        self.graph.grab_frame()

	    def wait_image(self):
	        self.image_done.wait(1000)
	        return self.image_grabbed        

	print("Opening first camera")
	camera1 = Camera(0)
	print("Opening second camera")
	camera2 = Camera(1)
	input("Press ENTER to grab photos")
	camera1.capture()
	camera2.capture()
	print("Waiting images")
	image1 = camera1.wait_image()
	image2 = camera2.wait_image()
	print("Done")
	ax1 = plt.subplot(2, 1, 1)
	ax1.imshow(image1)
	ax2 = plt.subplot(2, 1, 2)
	ax2.imshow(image2)
	plt.show()

Example 6
---------

ScreenCaptureRecorder is a software that includes a direct show input filter that provides images taken from the current screen. We can use it with the FilterGraph class to create an app that captures screenshots.

You can install ScreenCaptureRecorder from https://github.com/rdp/screen-capture-recorder-to-video-windows-free/releases. In my case, the installer did not register the capture source filter, and I had to do this operation manually executing the following commands:

Regsvr32 C:\Program Files (x86)\Screen Capturer Recorder\screen-capture-recorder.dll
Regsvr32 C:\Program Files (x86)\Screen Capturer Recorder\screen-capture-recorder-x64.dll

Below is a variation of Example 4 that makes sure the screen-capture-recorder filter is used as input device, and that can be used to capture screenshots:

	import threading
	import matplotlib.pyplot as plt
	import numpy as np
	from pygrabber.dshow_graph import FilterGraph

	image_done = threading.Event()
	image_grabbed = None

	def img_cb(image):
	    global image_done
	    global image_grabbed
	    image_grabbed = np.flip(image, 2)
	    image_done.set()

	graph = FilterGraph()
	screen_recorder_id = next(device[0] for device in enumerate(graph.get_input_devices())
	                          if device[1] == "screen-capture-recorder")
	graph.add_input_device(screen_recorder_id)
	graph.add_sample_grabber(img_cb)
	graph.add_null_render()
	graph.prepare()
	graph.run()
	input("Press ENTER to capture a screenshot")
	graph.grab_frame()
	image_done.wait(1000)
	graph.stop()
	plt.imshow(image_grabbed)
	plt.show()
