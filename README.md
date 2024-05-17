# Workload Prediction
This repository contains modules used to predict cognitive workload during office tasks based on, among eyetracking, data from an analog keyboard and the mouse. 

It is part of a master thesis named "Using Contextual Data to Predict Cognitive Load at the Workplace" at [TU Bergakademie Freiberg](https://tu-freiberg.de/).

## Description
The Software is split in three distinct parts.

The study-software is used to generate userdata under different cognitive load levels. 
The data processing uses the generated logging to calculate metrics. 
Those metrics are used in the data analysis, to find correlations to cognitive load. 
Furthermore the relevant metrics are used to predict cognitive load. 

Those modules can be used independent from each other. 
The App contains parts programmed in Python (Version 3.10) and C#.

### Study
The study is used to collect userdata in a controlled environment. 
The subject has to perform four different tasks, two based on writing, two based sorting movable objects on screen. 
The tasks are shown via a frontend build in [streamlit](https://streamlit.io).
The instructions and tasks are, when not specified differently written in german. 
All but one writing task are repeated while doing different secondary tasks. 
After every task the user has to fill out an [NASA TLX](https://humansystems.arc.nasa.gov/groups/TLX/).

#### Tasks
One writing task has the User write an E-Mail containing predefined Informations. 
This task is to do only once, because of its length and its high based cognitive load. 
The other writing task requires the user to copy short phrases from [this dataset](http://www.yorku.ca/mack/PhraseSets.zip). 
The phrases are written in english. 
The user has to write ten phrases in the default setting per level of cognitive load.
Both sorting tasks are designed the same way: the subject has to move "documents" in the corresponding target region. 
The clicktask is navigated by first clicking on the document to move, then clicking on the target region. 
The dragtask is navigated by drag and drop.
Both tasks are executed five times per cognitive load level.

#### Secondary Tasks
To get the subject to different cognitive load levels an n-Back-Task is used.
The subject listens to numbers over the Headset and completes the task by answering out loud. 
the answers are recorded by the headset. 
In the study "no secondary task", "0-back" and "1-back" are used.

#### Equipment
To use all the modules presented, headset and mouse are needed but don't have to be specific kind.
Furthermore the study uses the key depth measurements of the [Wooting two HE](https://wooting.io/wooting-two-he)-keyboard. 
For the Eyetracking the [Tobii Pro Spark](https://www.tobii.com/products/eye-trackers/screen-based/tobii-pro-spark) is used.

#### Process
After starting the app a username has to be entered.
The last four symbols show the order of primary and secondary task during the study. 
The fourth to last symbol defines the orderof the secondary task (0 -> "no secondary task", 1 -> "0-back", 2 -> "1.-back"), the three last symbols defines the orders of the primary tasks during each load level. (0 -> phrasetask, 1 -> dragtask, 2 -> clicktask).
The possible orders are:
- a -> 0,1,2
- b -> 1,2,0
- c -> 2,0,1
- d -> 2,1,0
- e -> 0,2,1
- f -> 1,0,2

After that, the repeatable tasks are presented to be tried out for 30 seconds each. 
To start the main part of the study, the user has to write the E-Mail. 
When a task is completeted sensor logging, as well as the tlx results are saved in the logging folder. 

### Data Processing
This part transforms the logging data from the study in predefined metrics. 
Those metrics are calculated in a rolling window. 
Furthermore the app logging is analysed to get the taskresults.
All results are saved split up in primary and secondary task. 
The Scripts are located in /data_processing/.

#### Eyetracking 
The Eyetracking class calculates metrics based on the pupil size as well as the location of the gaze on screen. 
The latter is logged by a tupel of values between 0 and 1. 
With (0,0) representing the top left corner of the screen, (1,1) bottom right.

Calculated are the minimum, maximum and average pupile size in the timeframe.
Based on the Gazedata the average distance and speeed of movements between ten gaze data points.

#### keyboard and mouse data
The data used, contains the mouse location on screen, as well as pressed- and released-Events of the keyboard.
Based on mouse logging, the average distance and speed of the mouse movements are calculated. 
The keyboard logging are used to calculate the number of keystrokes, as well as the deletions and the times in which no keys are pressed (so called deadtimes). 

#### Analog data
The special keyboard used allows to log the depth to which a key is pressed. 
Based on this, the maximum depth of a keystroke, as well as the time needed to press, hold and release the key. 
Additionally from the time needed and the depth the speed of press and release are calculated. 
The same can be said about the time needed for the entire keystroke.

#### App logging
Each task saves the userinputs to calculate the correctness of both. 
For the writing tasks the number of words and symbols cant be logged. 
Since the phrasetask has a target string, the user input can be compared to, the [levenshtein-distance](https://en.wikipedia.org/wiki/Levenshtein_distance) can be calculated.
For the mouse-tasks the number of correctly sorted files, as well as the needed moves are tracked per iteration of the task.

### Data Analysis
The data analysis is split up in two parts: the calculation of correlations and the prognosis of the cognitive load.

#### Correlations
The calculated metrics are compared with both the NASA-TLX results, as well as the cognitive load level. 
While the correlation between the first pair are calculated by pearsons, spearmans and kendalls coefficient. 
To see the differences between the cognitive load levels ANOVA and pairwise compairisons are used.

Based on the results here the relevant metrics are defined as follows:
when a correlation coefficient lies above 0.3, the metric shows a significant correlation.
The same goes for metrics, which show a p-value below 0.05 in ANOVA.

#### Prognosis
The prediction based on the NASA-TLX is done by a random forest regression. 
The prediction of the load level ist done by a random forest classifier, which can be sort in three or two classes. 
Those are either 0 -> no Secondary task, 1 -> 0-Back, 2 -> 1-Back (3 classes) or 0 -> no Secondary task, 1 -> 1-Back.

## Setup and Usage
### Study
1. create new venv using python3.10 in root folder `py -3.10 -m venv ./venv`
2. access venv and execute `pip install -r ./requirements.txt`
3. adjust following variables in config
    - sensor_console: show sensor console in 

    - no_phrases: number of phrases used in phrase task 
    - no_mouse: number of iterations during dragging task 
    - no_click: number of iterations during clicking task
    - sec_per_example: length of example task 
4. start app with `streamlit run ./study_view_main.py`
5. logging is saved in /logging/

### Data Processing 
1. use venv from Study
2. navigate to 
3. adjust following variables in rolling_window.py
    - rawdata path
        - one Folder: adjust loggin_path 
        - multiple folder: adjust list users
        - multiple_users: bool to use either option
    - window constraints
        - w_size: Größe Fenster
        - w_step: Stepsize
    - tasks: tasks included in prediction 
    - sensors: sensors included in prediction
    - output_path: location to save outputdata
4. start app with `python ./rolling_window.py`
5. results are saved in outputpath
    
### Correlations
1. navigate to ./ai_model/
2. create new venv using python3.10 `py -3.10 -m venv ./ai_venv`
3. access venv and execute `pip install -r ./req.txt`
4. adjust following variables in correl.py
    - weighted/workload_level: defines target value -> one has to be True
    - mode: taskcombination 
    - correl/anova: correlation type, anova als o does pairwise test
    - FILE_PATH: defines used inputdata (has to include processed data, demands, general_info )
5. start app with `python ./correl.py`
6. results are saved in ./correls_out/

### modell training
1. navigate to ./ai_model/
2. use venv from Correlations
3. adjust following variables in neural_network.py
    - Prediction system (one has to be True)
        - random_forest --> regression
        - random_forest_class --> classifier 
    - mode: taskcombination 
    - target value
        - weighted --> regression
        - workload_level --> classification
            - two --> use two or three classes in classification
    - data configuration
        - new_user --> if Ture -> use a Username as validation data rest is traindata 
            - if True -> define test_user 
    - FILE_PATH: defines used inputdata (has to include processed data, demands, general_info )
4. start app with `python ./neural_network.py`
5. results are saved
    - weights: ./weights/
    - results: ./validation/

### prognose tests
1. navigate to ./ai_model/
2. use venv from Correlations
3. adjust following variables in prognose_testing.py
    - WEIGHTS_PATH : path to weights
    - GEN_INFO_PATH: Path to geninfo --> can be the same as DATA_PATH
    - DATA_PATH: path to data to classify
    - model: Modeltype (classifier/ regression, n.o. classes)
    - training_mode --> datatype modell is trained on
    - testing_mode --> type of data to test
    - testing_user --> user to test
4. start app with `python ./prognose_testing.py`
5. results are saved in /prognose_test/
