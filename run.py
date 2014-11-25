from service_info import ServiceInfo
from utils import exec_string
import os

if __name__ == '__main__':
  exit_code = 0
  app_info = ServiceInfo( SYS_CALL=exec_string,
                          ENV_VARIABLES=os.environ )
  
  msg, err = app_info.run()

  if err:
    exit_code = 1
  
  print(msg)
  exit(exit_code)


