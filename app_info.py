import json

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
  "APP_ID" : "guid"
}

URLS = {
  "orgs": "/v2/organizations",
  "envs": "/v2/apps/{0}/env",
  "gets": "cf curl {0} -X 'GET'"
}

class AppInfo():

  def __init__(self, **kwargs):
    self.env = kwargs.get("ENV_VARIABLES")
    self.sys_call = kwargs.get("SYS_CALL")
    self.org = self.env["ORG"]
    self.space = self.env["SPACE"]
    self.app_name = self.env["APP_NAME"]
    self.service_instance_name = self.env["SERVICE_INSTANCE_NAME"]
    self.service_type = self.env["SERVICE_TYPE"]
    self.service_plan = self.env["SERVICE_PLAN"]
  
  def _orgs_url(self):
    return URLS["orgs"]

  def _space_url_generator(self, json_string):
    org_object = self._url_generator(json_string, JSON_STRUCT["ORG_NAME"], self.org, self._default_compare )
    space_url = org_object[0][JSON_STRUCT["SPACE_URL"]]
    return space_url

  def _app_url_generator(self, json_string):
    route_object = self._url_generator(json_string, JSON_STRUCT["SPACE_NAME"], self.space, self._default_compare )
    app_url = route_object[0][JSON_STRUCT["APP_URL"]]
    return app_url

  def _app_env_url(self, json_string):
    appinfo = self._url_generator_base(json_string, JSON_STRUCT["APP_NAME"], self.app_name, self._default_compare, JSON_STRUCT["META"] )
    app_guid = appinfo[0][JSON_STRUCT["APP_ID"]]
    app_env_url = URLS["envs"].format(app_guid)
    return app_env_url

  def _app_env_obj(self, json_string):
    jsonO = json.loads(json_string)
    return jsonO

  def _default_compare(self, l, r):
    return l == r

  def _url_generator(self, json_string, keyname, compare_value, compare_functor):
    return self._url_generator_base(json_string, keyname, compare_value, compare_functor, JSON_STRUCT["ENTITY"])
    
  def _url_generator_base(self, json_string, keyname, compare_value, compare_functor, return_key):
    jsonO = json.loads(json_string)
    url = [ x[return_key] for x in jsonO[JSON_STRUCT["RES"]] if compare_functor(x[JSON_STRUCT["ENTITY"]][keyname], compare_value)]
    return url

  def get_app_env_details(self):
    spaceurl, org_err = self._get_entity(self._orgs_url(), self._space_url_generator)
    appurl, space_err = self._get_entity(spaceurl, self._app_url_generator)
    appenvurl, app_err = self._get_entity(appurl, self._app_env_url)
    appenv_obj, appenv_err = self._get_entity(appenvurl, self._app_env_obj)
    return (appenv_obj, [org_err, space_err, app_err, appenv_err])

  def _command_create(self, url):
    return URLS["gets"].format(url)
 
  def _get_entity(self, url, response_parser):
    cmd = self._command_create(url)
    stdout, err = self.sys_call(cmd)

    if not err:
      response = response_parser(stdout)
    
    else:
      response = stdout

    return (response, err)


