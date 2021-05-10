
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
2. [Deployment Environment](#deployment-environment)
3. [Installation](#installation)
4. [Repository Contents](#repository-contents)
5. [Video Presentation](#video-presentation)

***


## Project Information
Our goal was to create an application which will detect a concussive injury on an individual by tracking their eye movement and analyzing the data we capture. We aimed to provide an affordable solution that could be adapted into the current Head Injury Assessment (HIA).

The following objectives where identified to achieve our goals:

**Capture Data** - Using a video feed, we tracked the individual’s eyes and then mapped the pupils movement. The first capture is the base-line test. This is taken when the individual is in a non-injured state. The second test will occur after the individual has had a suspected concussive injury.

**Process Data** - Using the data captured we created graphical representations using the x,y coordinates from both eyes as points in the plane.

**Analyse Data** - The data is then used to make the determination. This is done by comparing the baseline data with the post incident data. We should see a deviation in patterns as the eyes movement will be altered while in a concussive state.

**Store Data** - The data from both tests are stored in separate databases. The baseline data could be taken and stored weeks or months before a concussive injury occurs.

**Report Findings** - As this application should be operated by a party other than the ’patient’, it should provide visual feedback of the results of the assessment.  This is achieved through the use of a GUI.

### Screenshot
![RoadMap](https://github.com/Concussion-Research-Project/Applied-Project-and-Minor-Dissertation/blob/main/Images/objectivesupdated.png)

***

## Deployment Environment 

The application was developed for the Linux operating system. Below is a list of requirements. 

1. [**Ubuntu**](https://releases.ubuntu.com/18.04/): Version 18.04 LTS 

2. [**MongoDB**](https://github.com/Michael-Mulholland/Applied-Project-Documentation/wiki/MongoDB-Setup)


4. [**Amazon Web Services**](https://aws.amazon.com/)
5. [**Python3**](https://www.python.org/downloads/release/python-369/): Version 3.6.9 (pre-installed with Ubuntu 18.04)
6. [**pip3**](https://pypi.org/project/pip/21.0.1/): Version 21.0.1
    
6. [**openCV**](https://pypi.org/project/opencv-python/3.4.5.20/): Version 3.4.5.20
    
7. [**numpy**](https://pypi.org/project/numpy/1.19.5/): Version 1.19.5

8. [**dlib**](https://pypi.org/project/dlib/): Version 19.21.0 

9. [**matplotlib**](https://pypi.org/project/matplotlib/): Version 3.3.4

10. [**scikit-learn**](https://pypi.org/project/scikit-learn/0.24.1/): Version 0.24.1

11. [**keras**](https://pypi.org/project/keras/): Version 2.4.3

12. [**dnspython**](https://pypi.org/project/dnspython/1.16.0/): Version 1.16.0

13. [**pymongo**](https://pypi.org/project/pymongo/3.11.3/): Version 3.11.3

14. [**pyqt5**](https://pypi.org/project/PyQt5/): Version 5.15.4

15. [**tensorflow**](https://pypi.org/project/tensorflow/): Version 2.4.1


***

## Installation

### Clone the Project

```
$ git clone https://github.com/Concussion-Research-Project/Applied-Project-and-Minor-Dissertation.git
```

***

### Run Application

```
cd ../path/to/the/cloned/file
```

To start the application run the following command:

```
$ python3 client.py
```

## User Guide
Click the [link](https://github.com/Michael-Mulholland/Applied-Project-Documentation/wiki/User-Guide) for instructions on how to use our application.

***


## Video Presentation

A video of the application running can be found here - [YouTube](https://www.youtube.com/watch?v=rTPTsTVICl4) 
