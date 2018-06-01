#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 12 11:45:18 2018

@author: peterkraemer
"""
#def recall_snacks(run):
run=1
# EXP INFO & INITIALIZE
#   import packages
#    import csv
import os
from expyriment import design, control, stimuli, misc, io
import pandas as pd
import constants
#control.set_develop_mode(True)

# Inputs
filename = constants.latestfilename('folder','*data.h5')
#    path_folder= constants.pathFolder

subjID      =   constants.getsubjid(filename)

#    run=4#experimental run

control.defaults.event_logging = 2
    
#   initialize the experiment
exp         =   design.Experiment(name="Recall")
control.initialize(exp)

StimList              =   pd.read_hdf(filename,key='StimLists/StimListRec_Set%d'%run,mode='r')


#   creating most elements on screen
fix         =   stimuli.Circle(3, colour=None, line_width=None, position=None, anti_aliasing=None)
pos         =   [(-300,0), (300,0), (0, 0)]
rect_b      =   stimuli.Rectangle((80,80), colour=(255,255,255), position=pos[2])
blank       =   stimuli.BlankScreen()

c1    =   stimuli.BlankScreen()      
blank.plot(c1)
c1.preload()
c2    =   stimuli.BlankScreen()     
fix.plot(c2)
c2.preload()
c3    =   stimuli.BlankScreen()     
fix.plot(c3)
rect_b.plot(c3)
c3.preload()
    
txt_input = io.TextInput("")

# DESIGN
b   =   design.Block()
for trial in range(len(StimList)):
    t    =   design.Trial()
    
    # blank screen

    t.add_stimulus(c1)
    
    # fixation dot

    t.add_stimulus(c2)

    # rectangles

    t.add_stimulus(c3)

    # pictures
    c4    =   stimuli.BlankScreen()     
    fix.plot(c4)
    rect_b.plot(c4)

#    path_symbol =   os.path.join(path_folder,'PICTURES','symbol'+str(StimList[trial][0])+'.bmp')
    path_symbol =   StimList['Symbol'][trial]
    symbol      =   stimuli.Picture(path_symbol, position=pos[2])
    symbol.plot(c4)
    
    c4.preload()
    t.add_stimulus(c4)
    
    # adding trial to block
    b.add_trial(t)

exp.add_block(b)


exp.data_variable_names     =   ["subjID","runID","TrialID","decisionTime","EstSnackID","EstSource"]
### START ###
control.start(experiment=None, auto_create_subject_id=None, subject_id=subjID, skip_ready_screen=False)
#control.start(exp,skip_ready_screen=True)
for block in exp.blocks:
    for trial in block.trials:
        
        trial.stimuli[0].present()
        exp.clock.wait(2000)
                
        trial.stimuli[1].present()
        exp.clock.wait(1000)      
        
        trial.stimuli[2].present()
        exp.clock.wait(1000)
        
        trial.stimuli[3].present()
#        exp.clock.wait(2000)
#        trial.stimuli[3].present()
#        exp.clock.wait(2000)background_stimulus=None
        key, rt = exp.keyboard.wait(misc.constants.K_SPACE)
        txt_input = io.TextInput(message = "which ID?")
        answer=txt_input.get()
        txt_input = io.TextInput(message = "left=1,right=2")
        source=txt_input.get()
        exp.data.add([subjID,run,trial.id,rt,answer,source])
### END EXPERIMENT ###
control.end()

    ############################ save data in hdf5file ############################
db = pd.HDFStore(filename)
path_data = os.path.join(os.getcwd(),constants.latestfilename('data','recall*.xpd'))
data = pd.read_csv(path_data,sep=',',header=14)
df = pd.DataFrame(data)
db.put('recall/ResultsRec%d'%run, df, format = 'table', data_columns = True)
db.close()