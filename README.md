Title: Driverless experience on Indian roads.

Background:
Unethical driving practices in India lead to thousands of deaths every year.Specially abled people are not able to use vehicles as per their interests.
Using computer vision and behavioural cloning to help drivers assist and lead vehicles to an autonomous future ensuring saftey.

Problem Descripton:
Unlike the already present pipeline method (used by tesla) for autonomous driving , which uses multiple sensor inputs and combines them to a  single input (sensor fusion method), 
which requires multiple sensors which are expensive and not easily available to most of the population in India.
Our approach is way simpler and efficient , as it involves use of a  single camera sensor and a steering sensor. 
It reduces the cost of application as well as manufacture and could be scaled easily.
Using this , our model learns to imitate human behaviour by looking at multiple recorded data of “driving scenarios”.

Key features:
1.Autonomus driving
Keeps the car on road by detecting turns and road conditions.
2.Driver saftey measures
Checks if the driver is looking at the road to ensure saftey.


Solution:
A data set is trained in which the steering angle is mapped to the curve of the road.
This data set is then implemented using sensor fusion method to run the car on the road.


WorkFlow:
There are 3 folders respectively for the 3 team members working on 3 features.
sam = contains all the ui and front-end involved
avi = working on eye detection and driver saftey
arsh  = working on the autonomus driving feature

IN the end we will merge all the folders and run it using a single file



