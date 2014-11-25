import subprocess

def exec_string(self, cmdString):
  stdout = ""
  err = False

  try:
    stdout = subprocess.check_output(cmdString, shell=True)
    
  except subprocess.CalledProcessError as e:
    stdout = "error: {0}".format(e)
    err = True

  return (stdout, err)

def get_first(arr):
  return arr[0]
