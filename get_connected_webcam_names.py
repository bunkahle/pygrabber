#!/usr/bin/env python
# -*- coding: utf-8 -*-

# tested under Python 2 and 3

from __future__ import print_function
from pygrabber.dshow_graph import FilterGraph

graph = FilterGraph()
print(graph.get_input_devices())
