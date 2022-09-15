# MuralTagLab: an image segmentation tool oriented to wall paintings

MuralTagLab is a tool based on TagLab (https://taglab.isti.cnr.it/) aimed for the digital restoration of wall paintings. The tool includes different types of CNN-based segmentation networks specially trained for agnostic (relative only to contours) or semantic recognition.

![ScreenShot](screenshot.png)


## Interaction
MuralTagLab allows to :

- zoom and navigate a large map using (zoom/mouse wheel, pan/'Move' tool selected + left button). With every other tool selected the pan is activated with ctrl + left button
- segment in a semi-automatic way by indicating the extremes of the desired blob with the 4-clicks tool. This is achieved using the Deep Extreme Cut network. Deep Extreme Cut original code can be found here: https://github.com/scaelles/DEXTR-PyTorch
- segment in a semi-automatic way by indicating the interior and the exterior of a blob using the positive-negative clicks tool. Use shift+left mouse button to assign the positive (the interior) points and shift+right mouse button to assign the negative (the exterior) points. This tool is based on the RITM interactive segmentation project, code and additional information can be found here: https://github.com/saic-vul/ritm_interactive_segmentation
- assign a class with the 'Assign class' tool or double-clicking the class in the labels panel
- Area, perimeter and other information are displayed in the region info panel on the right
- simultaneously turn off the visibility of one or more classes, (ctrl + left button/disable all but the selected, shift + left button, inverse operation), change the class transparency using the above slider
- perform boolean operations between existing labels (right button to open the menu)
- refine the incorrect borders automatically with the Refine operation or manually with the 'Edit Border' tool
- tracking changes in different time intervals
- import depth information
- import GeoTiff
- draw internal cracks with the 'Create Crack' tool
- make freehand measurements or measure the distance between centroids (Ruler tool).
- save the annotations (as polygons) and import them into a new project
- export a CSV file table containing the data of each annotation
- export a JPG file of a black background with totally opaque labels
- export shapefiles
- export a new dataset and train your network (!)


## Supported Platforms and Requirements
MuralTagLab runs on __Linux__, __Windows__, and __MacOS__. To run MuralTagLab, the main requirement is just __Python 3.6.x or 3.7.x__.

GPU accelerated computations are not supported on MacOS and on any machine that has not an NVIDIA graphics card.
To use them, you'll need to install the __NVIDIA CUDA Toolkit__, versions 9.2, 10.1 or 10.2 are supported.
If you don't have a NVida graphics card (or if you use MacOS), CPU will be used.

## Installing MuralTagLab

### Step 0: Dependencies
Before installing MuralTagLab, be sure to have installed __Python 3.6.x or 3.7.x__, and __NVIDIA CUDA Toolkit__ on Linux or Windows. You can check if they are properly installed by running the following commands in a shell (bash on Linux, poweshell on Windows; for MacOS just check the Python version):

```
python3 --version
nvcc --version
```
If python and cuda are properly installed, both commands will print their versions.

#### Linux

Under Linux, if you use a debian-based distribution (e.g. Ubuntu), except for python and nvcc, there are no other real requirements: the installer will take care of get and install all the dependencies. If you don't use the APT package manager (not ubuntu or debian derived distros), you'll need to install manually the gdal library (the command `gdal-config --version` should output the gdal library version), and `cmake`. Check out for your distribution how to install these two packages!

#### MacOS

On MacOS, the only real requirement (besides python) is the HomeBrew package manager: be sure to have it installed before running the installer. You can check [here](https://brew.sh/) the instructions on how to install it. If you don't want to install the HomeBrew package manager, be sure to install the gdal library manually (the command `gdal-config --version` should output the gdal library version), and `cmake`.

### Step 1: Clone the repository
Just click on the "Clone or Download" button at the top of this page and unzip the whole package in a folder of your choice.

### Step 2: Install all the dependencies

- open a terminal (not python prompt!);
- change directory to the MuralTagLab main directory: type `cd ` (be sure to type the space after `cd`) and then drag and drop into the terminal the MuralTagLab folder; then click `enter`;
- type the following command in the terminal:

```
python3 install.py
```
or, on Windows:

```
python.exe install.py
```

The script will automatically install the remaining libraries required by MuralTagLab and download the network weights.
If NVIDIA CUDA Toolkit is not supported by your machine, the script will ask to install the cpu version.
You can bypass this step and force to install the cpu version directly by running
```
python3 install.py cpu
```
or, on Windows:

```
python.exe install.py cpu
```

### Step 3: Run
Just start `TagLab.py` from a command shell or your preferred Python IDE.

From a terminal simply write:

```
python3 TagLab.py
```
or, on Windows:

```
python.exe taglab.py
```

To test if MuralTagLab works correctly, try to open the sample project available in the `projects` folder.

## Updating MuralTagLab

If you already installed MuralTagLab and you need to update to a new version, you can just run the `update.py` script from the terminal (be sure to be into the MuralTagLab main folder, see step 2):

```
python3 update.py
```
or, on Windows:

```
python.exe update.py
```

The script will automatically update MuralTagLab to the newest version available in this repository.

### Updating from 0.2

If you are updating MuralTagLab from 0.2 version, in order to download also the new networks, please run the `update.py` script twice:

```
python3 update.py
python3 update.py
```
