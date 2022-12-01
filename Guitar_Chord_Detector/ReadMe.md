# Chord Detection Project
## Author: MrHaso 2022

This is a Deep Learning project focused on the use of Convolutional Neural Networks to detect Chords played on a Guitar from a live feed Camera. 
The aim of this project is to understand the architechture of a CNN and its usage, as well as the reality of 'model complexity'. Looking at the results
we can determine that a more complex model will not necessarily perform better than a simpler model for a determined task. This means that experimentation
is the key behind finding a good model for the task at hand. 

A pre-trained model was not used intentionally since the goal of this project was not to use an API but to do the complete process of a Deep Learning project:
  
  1. Data collection
  2. Data Preprocessing
  3. Model Design and Creation
  4. Train / Test the Model   

The file with the name **guitabot.py** is the code that was written to load the CNN model into a Raspberry Pi with the aim of using a webcam to make live detections and move 6 SG90 Servo Motors into a position that mimics what is being seen in the frames of the CNN. 

Please note that you may (and probably will) need to update the ranges in which the servos move in the 'servos' dictionary.

e.g. servos = {'1':[5,185],} 

This is due to the fact that servos, even though they come from the same manufacturer, have different ranges of motion that vary slightly. This is physically translated in the fact that if you try to move different servos with the same settings, their movements will be slightly different (2-10 deg). The process to accurrately tune the ranges of motion was trial and error. 

Enjoy!

