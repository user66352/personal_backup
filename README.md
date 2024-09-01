## What is "personal_backup" ?

As the name says, its another backup solution.  
Nothing big. That's why i wrote it.  
I didn't want to add a lot of requirements to my system outside of python libraries nor did i want to learn long cli commands for minute backup jobs.  
In the backend rsync manages the actual file transfers. So generally speaking this script is automating simple backup jobs via rsync.  
Its purpose is not to be a replacement for anything already existing but to provide an easy to understand and quick way to setup private backups.  
I have written and tested that script only on Linux (Debian 12).  
Without a few changes it might very likely not run on Windows.  

## How it works

As simple as possible. That at least is the goal.  
The backups are controlled with 2 CSV files in the 'config' folder.  
Tasks are bundled in jobs so to have multiple directories/tasks executed just a single job needs to be started.  
At the moment only entire directories can be included in a task, not single files (might work, not tested, not optimized for).  
Each task can have an exclude list to exclude specific file types or sub directories.  

## Requirements

For the backup itself 'rsync' must be installed and available via the '$PATH' variable.  
Alternatively the path to rsync can be added to the file 'bkphandler.py' in the line 'self.rsync_bin = "rsync"'.  

Required python libraries:

* os, sys
* shutil
* tabulate
* datetime
* argparse
* termcolor

## Installation

Install the python requirements:

`python3 -m pip install shutil tabulate datetime argparse termcolor`

Download the src folder content/zip file and extract it to a target folder of your choice.

## How to use it

First a task has to be configured in 'config/tasks.csv'.  
A line starting with # will be ignored.  
Each task has the formate "*task_ID, type, source, target, action, exclude_list*".  

* task_ID: must be a unique integer
* type: at the moment only 'dir' is supported, so just add 'dir'
* source: source directory
* target: target directory
* action: can be either 'copy' or 'update', in 'copy' mode target files with the same name will not be overwritten, 'update' will overwrite an already existing target file if the source file is newer.
* exclude_list: will exclude specific file types or subdirectories, entries are separated by '|'

To backup /home/peter/Documents to /backup/home/peter/Documents and exclude all \*.dat and \*.log files.  
Also exclude subdirectory /home/peter/Documents/temp:  

1,dir,/home/peter/Documents,/backup/home/peter/Documents,copy,temp/|\*.dat|\*.log  

If multiple backup tasks got created that should be executed in sequence add them to the 'config/jobs.csv' file.  
Then execute that job with '`python3 backup.py --job 1`'. 1 is the unique job ID in this example.  
Alternatively a single task is started with '`python3 backup.py --task <task_id>`'.  
For all command options, which is not a lot, start it with '-h' or '--help'.  
