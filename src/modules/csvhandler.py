from modules import util


class csvhandler:
    def __init__(self) -> None:
        self.task_file = './config/tasks.csv'
        self.job_file = './config/jobs.csv'
        self.task_list = self.read_tasks()
        self.job_list = self.read_jobs()


    def read_tasks(self):
        try:
            fh = open(self.task_file, 'r')
            lines = fh.readlines()
            fh.close()
        except Exception as e:
            timestamp = util.get_timestamp()
            msg = f'{timestamp} | Exception in csvhandler.read_tasks: {e}'
            util.print_exception(msg)
            exit(1)
        #remove line feed from lines
        task_list = []
        for line in lines:
            if line[0] != '#':
                line = line.strip()
                line = line.split(',')
                task_list.append(line)

        return task_list

    def read_jobs(self):
        try:
            fh = open(self.job_file, 'r')
            lines = fh.readlines()
            fh.close()
        except Exception as e:
            timestamp = util.get_timestamp()
            msg = f'{timestamp} | Exception in csvhandler.read_jobs: {e}'
            util.print_exception(msg)
            exit(1)
        #remove line feed from lines
        job_list = []
        for line in lines:
            if line[0] != '#':
                line = line.strip()
                line = line.split(',')
                job_list.append(line)
        
        return job_list
