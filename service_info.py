import json
from utils import get_first

JSON_STRUCT = {
  "ENTITY": "entity",
  "META": "metadata",
  "RES": "resources",
  "SPACE_NAME": "name",
  "ROUTE_NAME": "host",
  "ORG_NAME": "name",
  "APP_NAME": "name",
  "SPACE_URL": "spaces_url",
  "APP_URL": "apps_url",
  "APP_ID" : "guid",
  "ACTION_SETUP": "setup",
  "ACTION_DESTROY": "cleanup"
}

URLS = {
  "orgs": "/v2/organizations",
  "envs": "/v2/apps/{0}/env"
}

CMDS = {
  "gets": "{0} curl {1} -X 'GET'",
  "add_service": "{0} create-service {1} {2} {3}",
  "remove_service": "{0} delete-service {1} -f",
  "bind_service": "{0} bind-service {1} {2}",
  "push_app": "{0} push {1} -p ./mockapp --no-start --no-route --no-manifest",
  "delete_app": "{0} delete {1} -f",
  "target": "{0} target -o {1} -s {2}"
}

class ServiceInfo():

  def __init__(self, **kwargs):
    self.env = kwargs.get("ENV_VARIABLES")
    self.sys_call = kwargs.get("SYS_CALL")
    self.cf_cli = self.env["CF_CLI"]
    self.org = self.env["ORG"]
    self.space = self.env["SPACE"]
    self.app_name = self.env["APP_NAME"]
    self.service_instance_name = self.env["SERVICE_INSTANCE_NAME"]
    self.service_type = self.env["SERVICE_TYPE"]
    self.service_plan = self.env["SERVICE_PLAN"]
    self.action = self.env["ACTION"]

  def _prior_run_was_clean(self, error_array):
    return len([ x for x in error_array if x ]) == 0

  def get_app_env_details(self):
    return_object = ""
    org_err = None
    space_err = None
    app_err = None
    appenv_err = None
    spaceurl, org_err = self._get_entity(self._orgs_url(), self._space_url_generator)
    
    if self._prior_run_was_clean([org_err, space_err, app_err, appenv_err]):
      appurl, space_err = self._get_entity(spaceurl, self._app_url_generator)

    if self._prior_run_was_clean([org_err, space_err, app_err, appenv_err]):
      appenvurl, app_err = self._get_entity(appurl, self._app_env_url)

    if self._prior_run_was_clean([org_err, space_err, app_err, appenv_err]):
      appenv_obj, appenv_err = self._get_entity(appenvurl, self._app_env_obj)
      return_object = json.dumps(appenv_obj)

    return (return_object, [org_err, space_err, app_err, appenv_err])
  
  def _setup_run(self):
    target_error = None
    service_error = None
    push_error = None
    bind_error = None
    details_error = None
    response_string = ""
    response_string, target_error = self.set_target()

    if self._prior_run_was_clean([target_error, service_error, push_error, bind_error, details_error]):
      response_string, service_error = self.add_service()
    
    if self._prior_run_was_clean([target_error, service_error, push_error, bind_error, details_error]):
      response_string, push_error = self.push_app()
    
    if self._prior_run_was_clean([target_error, service_error, push_error, bind_error, details_error]):
      response_string, service_error = self.bind_service()
    
    if self._prior_run_was_clean([target_error, service_error, push_error, bind_error, details_error]):
      response_string, details_error = self.get_app_env_details()
    
    return (response_string, [target_error, service_error, push_error, bind_error]+details_error)

  def _cleanup_run(self):
    target_error = None
    delete_error = None
    service_error = None
    response = []
    out, target_error = self.set_target()
    response.append(out)

    if self._prior_run_was_clean([target_error, delete_error, service_error]):
      out, delete_error = self.delete_app()
      response.append(out)
    
    if self._prior_run_was_clean([target_error, delete_error, service_error]):
      out, service_error = self.remove_service()
      response.append(out)

    return (response, [target_error, delete_error, service_error])

  def run(self):
    msg = ""
    err = False

    if self.action == JSON_STRUCT["ACTION_SETUP"]:
      msg, err = self._setup_run()

    elif self.action == JSON_STRUCT["ACTION_DESTROY"]:
      msg, err = self._cleanup_run()

    else:
      msg = "unset or invalid ACTION env variable"
      err = True

    return (msg, err)

  def delete_app(self):
    cmd = CMDS["delete_app"].format(self.cf_cli, self.app_name)
    res, err = self.sys_call(cmd)
    return (res, err)

  def push_app(self):
    cmd = CMDS["push_app"].format(self.cf_cli, self.app_name)
    res, err = self.sys_call(cmd)
    return (res, err)

  def bind_service(self):
    cmd = CMDS["bind_service"].format(self.cf_cli, self.app_name, self.service_instance_name)
    res, err = self.sys_call(cmd)
    return (res, err)

  def remove_service(self):
    cmd = CMDS["remove_service"].format(self.cf_cli, self.service_instance_name)
    res, err = self.sys_call(cmd)
    return (res, err)

  def add_service(self):
    cmd = CMDS["add_service"].format(self.cf_cli, self.service_type, self.service_plan, self.service_instance_name)
    res, err = self.sys_call(cmd)
    return (res, err)

  def set_target(self):
    cmd = CMDS["target"].format(self.cf_cli, self.org, self.space) 
    res, err = self.sys_call(cmd)
    return (res, err)

  def _orgs_url(self):
    return URLS["orgs"]

  def _space_url_generator(self, json_string):
    org_object = self._url_generator(json_string, JSON_STRUCT["ORG_NAME"], self.org, self._default_compare )
    space_url = get_first(org_object)[JSON_STRUCT["SPACE_URL"]]
    return space_url

  def _app_url_generator(self, json_string):
    route_object = self._url_generator(json_string, JSON_STRUCT["SPACE_NAME"], self.space, self._default_compare )
    app_url = get_first(route_object)[JSON_STRUCT["APP_URL"]]
    return app_url

  def _app_env_url(self, json_string):
    appinfo = self._url_generator_base(json_string, JSON_STRUCT["APP_NAME"], self.app_name, self._default_compare, JSON_STRUCT["META"] )
    app_guid = get_first(appinfo)[JSON_STRUCT["APP_ID"]]
    app_env_url = URLS["envs"].format(app_guid)
    return app_env_url

  def _app_env_obj(self, json_string):
    json_obj = json.loads(json_string)
    return json_obj

  def _default_compare(self, l, r):
    return l == r

  def _url_generator(self, json_string, keyname, compare_value, compare_functor):
    return self._url_generator_base(json_string, keyname, compare_value, compare_functor, JSON_STRUCT["ENTITY"])
    
  def _url_generator_base(self, json_string, keyname, compare_value, compare_functor, return_key):
    json_obj = json.loads(json_string)
    url = [ x[return_key] for x in json_obj[JSON_STRUCT["RES"]] if compare_functor(x[JSON_STRUCT["ENTITY"]][keyname], compare_value)]
    return url

  def _command_create(self, url):
    return CMDS["gets"].format(self.cf_cli, url)
 
  def _get_entity(self, url, response_parser):
    cmd = self._command_create(url)
    stdout, err = self.sys_call(cmd)

    if not err:
      response = response_parser(stdout)
    
    else:
      response = stdout

    return (response, err)


