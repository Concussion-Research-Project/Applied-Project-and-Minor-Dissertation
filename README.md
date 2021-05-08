
<a href="https://www.gmit.ie/" >
<p align="center"><img src="https://i.ibb.co/f1ZQSkt/logo-gmit.png"
alt="GMIT Logo" width="500" height="200"/>
</p></a>

***

| **Project Title** | Concussion Detection Application
| :------------- |:-------------|
| **Course**              | BSc (Hons) in Software Development |
| **Module**              | Applied Project and Minor Dissertation |
| **Institute**           | [Galway-Mayo Institute of Technology](https://www.gmit.ie/) |
| **Students**             | [Anthony Moore](https://github.com/AntoMoore) - G00170900@gmit.ie <br> [Darragh Lally](https://github.com/DarraghLally) - G00220290@gmit.ie <br> [Michael Mulholland](https://github.com/Michael-Mulholland) - G00362383@gmit.ie  |
| **Project Supervisor**     | Damien Costello |
| **Module Supervisor**   | Dr. John Healy |

***

## Table of Contents
1. [Project Information](#project-information)
2. [Technologies](#technologies)
3. [Deployment Environment](#deployment-environment)
4. [Installation](#installation)
5. [Operating](#Operating)
6. [Repository Contents](#repositiory-contents)
7. [Video Presentation](#video-presentation)

***


## Project Information
Our goal was to create an application which can detect a concussive injury on an individual by tracking their eye movement and analyzing the data we capture. Our intention was to develop software that will map and evaluate an injured parties oculomotor function. We aimed to provide an affordable solution that could be adapted into the current Head Injury Assessment (HIA).

The following methods where used to achieve our goals:

Capture
-	Using a video feed, we tracked the individual’s eyes and then mapped the pupils movement. The first capture is the base-line test. This is taken when the individual is in a non-injured state. The second test will occur after the individual has had a suspected concussive injury.

Process
-	Using the data captured we created graphical representations using the x,y coordinates from both eyes as points in the plane.

Analyse
-	The data is then used to make the determination. This is done by comparing the baseline data with the post incident data. We should see a deviation in patterns as the eyes movement will be altered while in a concussive state.

Store
-	The data from both tests are stored in separate databases. The baseline data could be taken and stored weeks or months before a concussive injury occurs.

Report
-	As this application should be operated by a party other than the ’patient’, it should provide visual feedback of the results of the assessment.  This can be achieved through the use of a GUI.

### Screenshot
![RoadMap](https://github.com/DarraghLally/README_Template/blob/main/images/objectivesupdated.png?raw=true)

***

## Technologies

A list of technologies used within the project:
* [Ubuntu](https://releases.ubuntu.com/18.04/): Version 18.04.5
* [MongoDB](https://www.mongodb.com/)
* [Amazon Web Services](https://aws.amazon.com/)
* [PyQt5](https://gist.github.com/ujjwal96/1dcd57542bdaf3c9d1b0dd526ccd44ff)
* [Python](https://www.python.org/downloads/release/python-369/): Version 3.6.9 

Packages
* [matplotlib](https://pypi.org/project/matplotlib/): Version 3.3.4
* [opencv-python](https://pypi.org/project/opencv-python/3.4.5.20/): Version 3.4.5.20
* [dlib](https://pypi.org/project/dlib/): Version 19.21.0 
* [scikit-learn](https://scikit-learn.org/stable/auto_examples/release_highlights/plot_release_highlights_0_24_0.html): Version 0.24.1
* [keras](https://pypi.org/project/keras/): Version 2.4.3
* [dnspython](https://fossies.org/linux/misc/dns/dnspython-1.16.0.tar.gz/): Version 1.16.0
* [keras](https://pypi.org/project/keras/): Version 2.4.3
* [numpy](https://pypi.org/project/numpy/1.19.5/): Version 1.19.5
* [pip3](https://pypi.org/project/pip/21.0.1/): Version 21.0.1
* [pymongo](https://pypi.org/project/pymongo/3.11.3/): Version 3.11.3
* [pyqt5](https://pypi.org/project/PyQt5/): Version 5.15.4
* [tensorflow](https://pypi.org/project/tensorflow/): Version 2.4.1

***

## Deployment Environment 

This application runs on the Linux OS. 

[Ubuntu](https://releases.ubuntu.com/18.04/): Version 18.04 LTS 


1. **Python3**: Version 3.6.9 (pre-installed with Ubuntu 18.04)
2. **pip3**: Version 9.0.1 
3. **openCV**: Version 3.4.5.20
    ```
    $ pip3 install opencv-python==3.4.5.20
    ```

    Install the following openCV packages
    ```
    $ sudo apt-get update
    $ sudo apt-get install build-essential cmake
    $ sudo apt-get install libopenblas-dev liblapack-dev 
    $ sudo apt-get install libx11-dev libgtk-3-dev
    ```
    
4. **numpy & dlib**
    ```
    $ pip3 install numpy
    $ pip3 install dlib
    ```

## Installation

Now the development environment is set up, you can clone and run the application. 
```
$ git clone https://github.com/Concussion-Research-Project/Applied-Project-and-Minor-Dissertation
$ cd ../path/to/the/file
$ python3 ....
```
Note: To use the application in a special environment use ```lorem ipsum``` to start.



### Clone the Project
Open a directory of your choice and enter the following command into the command line.

```git clone https://github.com/Concussion-Research-Project/Applied-Project-and-Minor-Dissertation.git```

***

### Running the Project
Change into the directory

```cd ../path/to/the/file```

To start the application run the following command:

```python client.py```

***










## Operating
***

## Repository Contents
***

## Video Presentation
