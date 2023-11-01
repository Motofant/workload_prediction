# Workload Prediction Experiment Setup
## Description
This Application is used to both aquire userdata during predefined tasks (Experiment), process the analysed Data ([Processing](###Processing)) and predict cognitive workload ([Prediction](###Prediction)). All of those module can be run independet from each other.
The App was developed, used and tested using Python 3.10.
### Experiment
This Part is used to collect user data when performing basic tasks while performing 0-Back and 1-Back as a secondary task plus a groundtruth round without secondary task. The collected Data contains Keyboard and Mouseevents, as well as Eyetracking from the Tobii Pro Spark and the keytravel distances provided from an analog keyboard from Wooting. Are either of those peripherals not at hand please refer to [the setup section](###WiP).
Furthermore the performance of the User is tracked. 
The Tasks are shown via a frontend build in [streamlit](https://streamlit.io), the data is collected via scripts in Python and C#.

### Processing

### Prediction
## Setup
### App
1. create new venv using python3.10
2. access venv and execute `pip install -r ./requirements.txt`
### Additional Software
Only necessary if the following peripheral are used. 
#### Tobii Pro Spark 
### WiP



