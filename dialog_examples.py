'''
Dialog examples.

	1. Dialog.addMessage(...)
	2. Dialog.addNumber(integer)
	3. Dialog.addNumber(float)
	4. Dialog.addSlider(...)
	5. Dialog.addCheckbox(...)
	6. Dialog.addCheckboxGroup(...)
	7. Dialog.getRadioButtonGroup(...)
	8. Dialog.getChoice(...)
	9. Dialog.addHelp(url)
	10. Dialog.addHelp(html)
	
'''

from __future__ import print_function, division
import __builtin__
import math
from mripy.ijmpy import *

name = "Coco"
Dialog.create("Greetings");
Dialog.addMessage("I will greet you!", 18, 'Blue');
Dialog.addString("Enter your name: ", "Monty", 12);
if  not Dialog.show().wasCanceled():
	name = Dialog.getString();
print("Hello " + name + "!");

number = 42
Dialog.create("Even/Odd");
Dialog.addNumber('number: ',  number, );
if  not Dialog.show().wasCanceled():
	number = int(Dialog.getNumber());
if number%2==0:
	message = "even"
else:
	message = "odd"
print(str(number) + " is " + message + ".");

number = PI
Dialog.create("fractional part");
Dialog.addNumber('real: ',  number, 7, 8, "rad");
if  not Dialog.show().wasCanceled():
	number = Dialog.getNumber();
frac, whole = math.modf(number)
print("The fractional part of "+str(number)+ " is " + str(frac) + '.')
 
min1, max1, value1 = 0, 100, 50
min2, max2, value2 = 0, 1, 0.5
Dialog.create("... and slidin'");
Dialog.addSlider("percent: ", min1, max1, value1)
Dialog.addSlider("fraction: ", min2, max2, value2)
if  not Dialog.show().wasCanceled():
	value1 = Dialog.getNumber()
	value2 = Dialog.getNumber()
print(str(int(value1)) + "% and a fraction of " + str(value2) + '.')

checked = false
unchecked = true
Dialog.create("check");
Dialog.addCheckbox("check", checked);
Dialog.addCheckbox("uncheck", unchecked);
if not Dialog.show().wasCanceled():
	checked = Dialog.getCheckbox();
	unchecked = Dialog.getCheckbox();
if checked and not unchecked:
	print("Yes, you did it!");
else:
	print("Nah, try again!");

defaults = r1c1, r1c2, r1c3, r2c1, r2c2, r2c3 = (true, false, true, false, true, false)
defaults = list(defaults)
Dialog.create("checkbox group")
Dialog.addCheckboxGroup(2, 3, ['1,1', '1,2', '1,3', '2,1', '2,2', '2,3'], defaults)
if not Dialog.show().wasCanceled():
	r1c1, r1c2, r1c3, r2c1, r2c2, r2c3 = Dialog.getCheckbox(), Dialog.getCheckbox(), Dialog.getCheckbox(), Dialog.getCheckbox(), Dialog.getCheckbox(), Dialog.getCheckbox()
print(r1c1, r1c2, r1c3, r2c1, r2c2, r2c3)  	

myStation = 'Nights with Alice Cooper'
Dialog.create("all we hear is...")
Dialog.addRadioButtonGroup("radio", ['WDR', 'DLF', 'Nights with Alice Cooper', 'France Musique'], 2, 2, myStation)
if not Dialog.show().wasCanceled():
	myStation = Dialog.getRadioButton()
print('All we hear is radio ' + myStation + '...')

myChoice = 'freewill'
choices = ['a ready guide in some celestial voice', 'not to decide', 'phantom fears', 'kindness that can kill', "a path that's clear", 'freewill']
Dialog.create('Choices under pressure')
Dialog.addChoice('You can choose: ', choices, myChoice);
if not Dialog.show().wasCanceled():
	myChoice = Dialog.getChoice()
if myChoice=='not to decide':
	print('you still have made a choice')
else:
	print(myChoice + ', a good choice.')

Dialog.create('ijmpy help')
Dialog.addMessage('Press the help-button to visit the ijmpy api-doc!')
Dialog.addHelp('https://montpellierressourcesimagerie.github.io/mripy/')
Dialog.show()

Dialog.create('ijmpy about')
Dialog.addMessage('Press the help-button to read about ijmpy!')
Dialog.addHelp('<html><h1>About ijmpy</h1><p>ijmpy is a jython wrapper of the imagej-macro-language.\nIt allow to easily porting macros to jython by reimplementing the macro commands in jython.</html>')
Dialog.show()