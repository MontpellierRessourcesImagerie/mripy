from __future__ import print_function, division
import __builtin__
from mripy.ijmpy import *

name = "Coco"
Dialog.create("Greetings");
Dialog.addMessage("I will greet you!", 18, 'Blue');
Dialog.addString("Enter your name: ", "Monty", 12);
if  not Dialog.show().wasCanceled():
	name = Dialog.getString();
print("Hello " + name + "!");
