#!/usr/bin/env python3
# VERSION January 23, 2023
# Copywrite (c) 2023 by MJ WOODWARD-GREENE


from tkinter import Tk
from tkinter import filedialog
from tkinter import messagebox
import pandas as pd
import os
import pathlib
import shutil
from datetime import datetime
import platform



def selectFiles():
    
    # Set up working (in user's home dir) and session (timestamped) directories in user's home directory
    timestamp = datetime.now()
    dayisf = timestamp.strftime('%Y_%b_%d')

    # Identify user's operating system, find their user home directory path
    opsys = platform.system()
    if opsys == 'Windows':
        home = os.environ['USERPROFILE']
    else:
        home = expanduser('~')
        
    # Create the working ARIS directory in the user's home folder (if not already there).
    try:
        os.mkdir(os.path.sep.join([home, 'ARISdata']))
    except FileExistsError:
        pass

    # Name full path of the session working directory (timestamped) in the home folder ARIS directory
    newsubdir = os.path.abspath((os.sep).join([home, 'ARISdata','ARISdata_'+dayisf]))

    # Create the working ARIS session directory inside the user's home folder (if not already there).
    try:
        os.mkdir(os.path.sep.join([newsubdir]))
    except FileExistsError:
        pass
    
    labelfnames = dict()
    labelfnames['workingdir'] = newsubdir
    print('labelfnames', labelfnames)
    
    # Open a GUI for the user to select files for processing. These should include ARIS 'Projects', 'Objective', and 'Approach' xlsx files.
    win = Tk()
    win.withdraw() # keep the root window from appearing
    win.wm_attributes('-topmost', True) # ensure the filedailog window is visible on top of other windows

    filenames = []

    while len(filenames) != 3:
        filenames = filedialog.askopenfilenames(parent=win, title="Select THREE ARIS INPUT FILES.")
        print(len(filenames), 'files selected\n', filenames)

        if filenames == 3:
             break
        
        elif len(filenames) != 3: # User did not select 3 ARIS input files.
            result = messagebox.askretrycancel(title="Select THREE ARIS INPUT FILES.",
                                           message="Select THREE ARIS INPUT FILES, \nProjects\nObjective\nApproach.")

            print('Retry?', result, ' You selected', len(filenames), 'file(s), You need three: ARIS Projects, Objective, and Approach.' )
            if result == False:
                import sys
                win.destroy()
                filenames = ['1', '2', '3'] # Exit while loop to call sys.exit()
                sys.exit()
                
            if result == True:
            
                pass
            
    print('\nInput files:')

    for f in filenames:
        test = f.lower()
        if 'projects' in test:
            projects_infile = f
            labelfnames['projects'] = f
        if 'objective' in test:
            objective_infile = f
            labelfnames['objective'] = f
        if 'approach' in test:
            approach_infile = f
            labelfnames['approach'] = f
    
    print('projects_infile =', projects_infile)
    print('objective_infile =', objective_infile)
    print('approach_infile =', approach_infile)
        
    # check file types
    files2process = []

    for f in filenames:
        dir_path = os.path.dirname(os.path.realpath(f))
        name = os.path.realpath(f)
        ext = pathlib.Path(name).suffix.lower()
        dirpath, fname = os.path.split(name)

        if ext == '.csv':
            # if input is already csv, move a copy to new directory created for this quarter's data
            # leave the original input file in the original directory.
            movedname = os.path.sep.join([newsubdir, fname])
            shutil.copy2(name, newsubdir)
            files2process.append(os.path.abspath(movedname))
            
        elif ext == '.xlsx':
            # if input is an xlsx, create a csv file, and save to new directory created for this quarter's data
            # leave the original xlsx input file in the original directory.

            # Create the csv filename, read the xlsx data to it within the original directory.
            csvname = name[:-4]+'csv'
            pd.read_excel(name).to_csv(csvname, index=None, header=True)
            _, csvfname = os.path.split(csvname)

            # Move the csv to the new directory, and delete the working csv in the original directory.
            # Delete the converted file from the original directory, (the copy is in the new directory).
            movedname = os.path.sep.join([newsubdir, csvfname])
            shutil.copy2(csvname, newsubdir)
            os.remove(csvname)
            files2process.append(os.path.abspath(movedname))

    print('\nARIS csv files unit tested for csv format.\n Prepped csv files saved for processing in', os.path.abspath(newsubdir))
    print()
    print('Prepped for processing as csv:')
    for f in files2process:
        test = f.lower()
        if 'projects' in test:
            projects_file = f
            labelfnames['projectscsv'] = f
        if 'objective' in test:
            objective_file = f
            labelfnames['objectivecsv'] = f
        if 'approach' in test:
            approach_file = f
            labelfnames['approachcsv'] = f

    labelfnames['workingdir'] = newsubdir
    print('projects_file =', projects_file)
    print('objective_file =', objective_file)
    print('approach_file =', approach_file)
    

    return labelfnames

      
if __name__ == '__main__':
    selectFiles()
