#!/usr/bin/python3
#ver. 0.4.2
version = '0.4.2'

import os, sys
from tabulate import tabulate
from modules.csvhandler import csvhandler
from modules.bkphandler import backup
from modules import util

def print_tasks(task_list):
    header = ['TaskID', 'Type', 'Source', 'Destination', 'Method', 'Exclude']
    task_list.insert(0, header)
    print(tabulate(task_list, headers='firstrow', tablefmt='fancy_grid'))

def print_jobs(job_list):
    header = ['JobID', 'Tasks', 'Comments']
    job_list.insert(0, header)
    print(tabulate(job_list, headers='firstrow', tablefmt='fancy_grid'))

def print_all(task_list, job_list):
    print('Jobs:')
    print_jobs(job_list)
    print()
    print('Tasks:')
    print_tasks(task_list)

def parse_options(options, task_list, job_list):
    if options['print_tasks']:
        print_tasks(task_list)
        exit(0)
    if options['print_jobs']:
        print_jobs(job_list)
        exit(0)
    if options['print_all']:
        print_all(task_list, job_list)
        exit(0)
    if options['task'] != '' and options['job'] != '':
        msg = 'Only one job or task can be selected. Not job & task at the same time.'
        util.print_exception(msg)
        exit(1)
    if options['task'] != '':
        task_id = options['task']
        action = {'action':'task', 'id':task_id}
    if options['job'] != '':
        job_id = options['job']
        action = {'action':'job', 'id':job_id}
    return action

def main(options):
    ch = csvhandler()
    action = parse_options(options, ch.task_list, ch.job_list)
    bp = backup(ch.job_list, ch.task_list, action)
    exit(0)


if __name__ == "__main__":
    #change working directory to current dir of script
    os.chdir(sys.path[0])

    msg = f'backup.py v{version}'
    util.print_status(msg)
    print()

    # manage arguments
    arg_count = len(sys.argv)
    options = util.parse_cmd_args(arg_count)

    main(options)
