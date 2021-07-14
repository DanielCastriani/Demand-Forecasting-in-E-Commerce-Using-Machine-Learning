import os
import subprocess
from typing import List

env = os.environ.copy()
HADOOP_HOME = '/opt/hadoop'
env['PATH'] = f"{HADOOP_HOME}/bin:{HADOOP_HOME}/sbin:{env['PATH']}"


def run_cmd(args_list: List):
    print(f"> {' '.join(args_list)}")
    proc = subprocess.Popen(args_list, stdout=subprocess.PIPE, stderr=subprocess.PIPE, env=env)
    s_output, s_err = proc.communicate()
    print(s_output.decode() if s_output else s_err.decode())
