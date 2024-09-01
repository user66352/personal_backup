import os
from modules import util


class backup:
    def __init__(self, job_list, task_list, action) -> None:
        self.rsync_bin = 'rsync'        # if rsync is not in $PATH or a specific rsync binary should be used put in '/path/to/rsync'
        self.is_rsync()
        self.job_list = job_list
        self.task_list = task_list
        self.select_action(action)

    def is_rsync(self):
        if not util.test_rsync(self.rsync_bin):
            msg = f"rsync binary '{self.rsync_bin}' could not be found in $PATH!"
            util.print_exception(msg)
            exit(1)

    def select_action(self, action_dict):
        #action is a dictionary: {action : 'task|job', id : 'task_id|job_id'}
        action = action_dict['action']
        id = action_dict['id']
        if action == 'job':
            self.exec_job(id)
        elif action == 'task':
            self.exec_task(id)
        else:
            timestamp = util.get_timestamp()
            msg = f'{timestamp} | Error in Action select_action(self, action) | "{action}" not found!'
            util.print_exception(msg)
            exit(1)

    def exec_job(self, job_id):
        msg = f'Executing Job ID {job_id}'
        util.print_status(msg)
        job = []
        for line in self.job_list:
            if line[0] == job_id:
                job = line
                break
        if job == []:
            msg = f'Job ID {job_id} not found!'
            util.print_exception(msg)
            exit(1)
        else:
            tasks = job[1].split('|')

        for task in tasks:
            self.exec_task(task)

    def exec_task(self, task_id):
        for line in self.task_list:
            if line[0] == task_id:
                task = line
                break

        category = task[1]
        src = task[2]
        tgt = task[3]
        act = task[4]
        excl_list = task[5] # exclude file extensions list from task.csv

        exec = False
        if category == "dir":
            msg = "{timestamp} : Executing Task {task_id}".format(timestamp=util.get_timestamp(),task_id=task_id)
            util.print_status(msg)
            msg = f"from dir: {src}"
            util.print_status(msg)
            msg = f"to dir:   {tgt}"
            util.print_status(msg)

            brc = self.backup_dir(src,tgt,act,excl_list)
            if brc == 0:
                self.sync(tgt)
                msg = "{timestamp} : Backup Task {task_id} finished successfully".format(timestamp=util.get_timestamp(),task_id=task_id)
                util.print_status(msg)
                print()
            else:
                msg = "{timestamp} : Backup Task {task_id} returned error code: {brc}".format(timestamp=util.get_timestamp(),task_id=task_id,brc=str(brc))
                util.print_exception(msg)
                print()
            exec = True
        if not exec:
            msg = "{timestamp} : No type found for backup task {task_id}".format(timestamp=util.get_timestamp(),task_id=task_id)
            print(msg)

    def format_rsync_for_exclude(self, excl):
        excl_cmd = ''
        excl_list = excl.split('|')
        for e in excl_list:
            tmp_str = f' --exclude "{e}" '
            excl_cmd = excl_cmd + tmp_str
        return excl_cmd

    def backup_dir(self, src, dst, option, excl_list):
        options = {"copy": "-axv", "update": "-rlptgoDuv"}
        cmd = f'{self.rsync_bin} {options[option]}'
        if len(excl_list) > 0:
            excl_cmd_list = self.format_rsync_for_exclude(excl_list)
        else:
            excl_cmd_list = ' '
        shell_command = '{cmd}{excl}{src} {dst}'.format(cmd=cmd,excl=excl_cmd_list,src=src,dst=dst)
        rc = os.system(shell_command)
        return rc

    def sync(self, tgt):
        msg = 'Syncing...'
        util.print_status(msg)
        rc = os.system(f'sync -f {tgt}')
        return rc
