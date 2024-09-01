import datetime
import argparse
from termcolor import cprint


def get_timestamp():
    return datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

def print_status(msg):
    cprint(msg, "light_cyan")

def print_exception(msg):
    cprint(msg, 'light_red')

def parse_cmd_args(arg_count):
    #default definitions
    options = {'task':'', 'job':'', 'print_tasks':False, 'print_jobs':False, 'print_all':False}

    argParser = argparse.ArgumentParser()
    argParser.add_argument("-t", "--task", type=str, help="execute the specified task id") # most simple -> got args.a, type is `str`
    argParser.add_argument("-j", "--job", type=str, help="execute the specified job id")
    argParser.add_argument("--print-tasks", action="store_true", help="print all tasks")
    argParser.add_argument("--print-jobs", action="store_true", help="print all jobs")
    argParser.add_argument("--print-all", action="store_true", help="print all jobs and tasks")

    if arg_count > 1:
        args = argParser.parse_args()
    else:
        msg = 'No Arguments found! At least 1 argument must be given!'
        print_exception(msg)
        print()
        argParser.print_help()
        exit(1)
    
    if args.task != None:
        options['task'] = args.task
    if args.job != None:
        options['job'] = args.job
    if args.print_tasks:
        options['print_tasks'] = True
    if args.print_jobs:
        options['print_jobs'] = True
    if args.print_all:
        options['print_all'] = True

    return(options)

def test_rsync(rsync_bin):
    from shutil import which
    if which(rsync_bin): return True
    return False
