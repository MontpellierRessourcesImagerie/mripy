# mripy
MRI ImageJ related python (jython) package.

* [api-doc](https://montpellierressourcesimagerie.github.io/mripy/)

## ijmpy
ijmpy is a jython wrapper of the imagej-macro-language. It allow to easily porting macros to jython by reimplementing the macro commands in jython.

The idea is to be able to import ijmpy, copy your ij-macro code and use it in jython, profiting from the python language and datastructures.

Try for example:
```python
  run("Duplicate...", " ");
  run("Find Edges");
  run("8-bit");
  run("Smooth");
  setAutoThreshold(thresholdMethod);
  run("Analyze Particles...", "size="+minSize+"-"+maxSize+" circularity=0.00-1.00 show=Masks exclude in_situ");
  run("Create Selection");
  run("Enlarge...", "enlarge=" + numberOfDilates + " pixel");
  roiManager("Add");
  close();
  roiManager("select", 0);
  run("Clear Outside");
```

## bialang
bialang is a bio-image analyst centric jython wrapper for the ImageJ1 api. In bialang the above code will look something like this:

```python
  image = duplicate(inputImage)
  findEdges(image)
  to8Bit(image)
  smooth(image)
  toMask(image,
     percentileThreshold(image),
     Filter(minSize, maxSize, minCirc, maxCirc, exclude))
  roi = createSelection(image)
  close(image)
  enlarge(roi, numberOfDilates, unit=units.pixel)
  clearOutside(inputImage, roi)
```
The operations like `duplicate`, `findEdges`, ... are implemented as functions and as objects which can be created and configured before run.

For example:

```python
Duplicate = Duplicate()
Duplicate.selectChannels(1, 3)
Duplicate.setZSices(1, 3, 5, 7)
Duplicate.run(image)
```

## bialangsj 
bialangsj (sj for sci-java) is a bio-image analyst centric jython wrapper for the ImageJ2 api. The idea is to create the same classes and functions as in bialang but implemented in ImageJ2 and sci-java.

##  How to use it

Clone or download the repository. Copy the mripy-folder into the folder jars/Lib of your FIJI installation. Import the module you want to use in your iython image analysis script.

```python
from mripy.ijmpy import *
```

```python
from mripy.bialang import *
from mripy.bialangsj import *
```
or 

```python
from mripy import bialang as bl
from mripy import bialangsj as blsj
```

Have a look at the unit tests for code-examples.

## Notes:

21.02.2020: **Currently it's only the beginning of a proove of concept.** 

Since `run`, `roiManager` and `setAutoTreshold` are implemented in ijmpy, some recorded ij-macros might already work. Please contact me if you want to participate in the project.
