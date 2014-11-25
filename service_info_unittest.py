from pyvows import Vows, expect
from service_info import ServiceInfo
import json
import re

ORGFILE = "fixtures/orgs.json"
SPACEFILE = "fixtures/spaces.json"
APPFILE = "fixtures/apps.json"
APPENVFILE = "fixtures/appenv.json"
ADD_SERVICE_FILE = "fixtures/create_service.out"
REMOVE_SERVICE_FILE = "fixtures/delete_service.out"
BIND_SERVICE_FILE = "fixtures/bind_service.out"
PUSH_APP_FILE = "fixtures/push_app.out"
DELETE_APP_FILE = "fixtures/delete_service.out"
TARGET_FILE = "fixtures/target.out"
HIJACK_MOCK_CALLS = [ 
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
  },
  {
    "rgx": re.compile(".* create-service .* .* .*"),
    "name": ADD_SERVICE_FILE
  },
  {
    "rgx": re.compile(".* delete-service .* -f"),
    "name": REMOVE_SERVICE_FILE
  },
  {
    "rgx": re.compile(".* bind-service .* .*"),
    "name": BIND_SERVICE_FILE
  },
  {
    "rgx": re.compile(".* push .* -p ./mockapp -b https://github.com/cloudfoundry-community/staticfile-buildpack.git --no-start --no-route --no-manifest"),
    "name": PUSH_APP_FILE
  },
  {
    "rgx": re.compile(".* delete .* -f"),
    "name": DELETE_APP_FILE
  },
  {
    "rgx": re.compile(".* target -o .* -s .*"),
    "name": TARGET_FILE
  }
]

def mock_success_cli_sys_call(cmd_str):
  return_string = ""

  for i in HIJACK_MOCK_CALLS:
    if i["rgx"].match(cmd_str) != None:
      return_string = _get_filestring(i["name"])

  return (return_string, False)

def _get_filestring(filename):
  data = ""

  with open(filename, "r") as myfile:
    data=myfile.read().replace('\n', '')

  return data

def test_cli_success_output(filename, functor):
  control_output = _get_filestring(filename)
  output, err = functor()
  expect(output).to_equal(control_output)
  expect(err).to_equal(False)

@Vows.batch
class ModuleTestsForAppInfo(Vows.Context):
  def topic(self):
    env = {}
    env["CF_CLI"] = "cf"
    env["ORG"] = "pivotalservices"
    env["SPACE"] = "development"
    env["APP_NAME"] = "sample-todo"
    env["SERVICE_INSTANCE_NAME"] = "sample-todo-service"
    env["SERVICE_TYPE"] = "pubnub"
    env["SERVICE_PLAN"] = "free"
    return env

  class WhenMakingCallsSuccessfully(Vows.Context):
    def topic(self, env):
      app_info = ServiceInfo( SYS_CALL=mock_success_cli_sys_call,
                          ENV_VARIABLES=env )
      return app_info

    def we_get_a_error_value_of_False(self, topic):
      app_info = topic
      expect(app_info).Not.to_be_null() 

    def get_app_env_details_should_yield_json(self, topic):
      app_info = topic
      app_details_control = json.loads(_get_filestring(APPENVFILE))
      app_details, err = app_info.get_app_env_details()
      non_empty_errors = [ x for x in err if x ]
      error_count = len(non_empty_errors)
      expect(app_details).to_equal(app_details_control)
      expect(error_count).to_equal(0)
    
    def delete_app_should_yield_success_output(self, topic):
      test_cli_success_output(DELETE_APP_FILE, topic.delete_app)

    def push_app_should_yield_success_output(self, topic):
      test_cli_success_output(PUSH_APP_FILE, topic.push_app)

    def bind_service_should_yield_success_output(self, topic):
      test_cli_success_output(BIND_SERVICE_FILE, topic.bind_service)

    def remove_service_should_yield_success_output(self, topic):
      test_cli_success_output(REMOVE_SERVICE_FILE, topic.remove_service)

    def add_service_should_yield_success_output(self, topic):
      test_cli_success_output(ADD_SERVICE_FILE, topic.add_service)

    def set_target_should_yield_success_output(self, topic):
      test_cli_success_output(TARGET_FILE, topic.set_target)

    



