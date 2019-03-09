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