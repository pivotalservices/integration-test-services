import subprocess

def exec_string(cmdString):
  stdout = ""
  err = False

  try:
    stdout, _ = subprocess.Popen(cmdString, stdout=subprocess.PIPE, shell=True).communicate()

  except subprocess.CalledProcessError as e:
    stdout = "error: {0}".format(e)
    err = True

  return (stdout, err)

def get_first(arr):
  return arr[0]
