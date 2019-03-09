#!/usr/bin/env python
from distutils.core import setup

setup(
    name='pygrabber',
    version='1.0',
    author='Andreas Bunkahle',
    author_email='abunkahle@t-online.de',
    description='Capture photo from webcam and simple image processing using DirectShow and OpenCV',
    license='MIT',
    py_modules=['pygrabber.__init__', 'pygrabber.dshow_graph', 'pygrabber.win_api_extra', 'pygrabber.PyGrabber', 'pygrabber.moniker', 'pygrabber.image_process', 'pygrabber.dshow_structures', 'pygrabber.dshow_ids'],
    python_requires='>=2.7',
    url='https://github.com/bunkahle/pygrabber',
    long_description=open('README.md').read(),
    platforms = ['win'],
    install_requires=['matplotlib', 'opencv-python', 'comtypes', 'numpy']
)
