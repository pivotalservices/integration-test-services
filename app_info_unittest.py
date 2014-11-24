from pyvows import Vows, expect
from app_info import AppInfo
import json
import re

ORGFILE = "fixtures/orgs.json"
SPACEFILE = "fixtures/spaces.json"
ROUTEFILE = "fixtures/routes.json"
APPFILE = "fixtures/apps.json"
APPENVFILE = "fixtures/appenv.json"
KNOWN_EXPRESSIONS = [ 
  {
    "rgx": re.compile("cf curl /v2/organizations -X 'GET'"),
    "name": ORGFILE
  },
  {
    "rgx": re.compile("cf curl /v2/organizations/.*/spaces -X 'GET'"),
    "name": SPACEFILE
  },
  {
    "rgx": re.compile("cf curl /v2/spaces/.*/apps -X 'GET'"),
    "name": APPFILE
  },
  {
    "rgx": re.compile("cf curl /v2/apps/.*/env -X 'GET'"),
    "name": APPENVFILE
  }
]

def mock_success_sys_call(cmd_str):
  return_string = ""

  for i in KNOWN_EXPRESSIONS:
    if i["rgx"].match(cmd_str) != None:
      return_string = _get_filestring(i["name"])

  return (return_string, False)

def mock_failure_sys_call(cmd_str):
  return (cmd_str, True)

def _get_filestring(filename):
  data = ""

  with open(filename, "r") as myfile:
    data=myfile.read().replace('\n', '')

  return data

@Vows.batch
class ModuleTestsForAppInfo(Vows.Context):
  def topic(self):
    env = {}
    env["ORG"] = "pivotalservices"
    env["SPACE"] = "development"
    env["APP_NAME"] = "sample-todo"
    env["SERVICE_INSTANCE_NAME"] = "sample-todo-service"
    env["SERVICE_TYPE"] = "pubnub"
    env["SERVICE_PLAN"] = "free"
    return env

  class WhenGettingRoutingTableSuccessfully(Vows.Context):
    def topic(self, env):
      app_info = AppInfo( SYS_CALL=mock_success_sys_call,
                          ENV_VARIABLES=env )
      return app_info

    def we_get_a_error_value_of_False(self, topic):
      app_info = topic
      expect(app_info).Not.to_be_null() 

    def get_app_env_details_should_yield_json(self, topic):
      app_info = topic
      app_details_control = json.loads(_get_filestring(APPENVFILE))
      app_details, err = app_info.get_app_env_details()
      expect(app_details).to_equal(app_details_control)
      expect(len([ x for x in err if x ])).to_equal(0)

