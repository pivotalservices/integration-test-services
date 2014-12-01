# integration-test-services
====================

a utility to help with integration tests
of bound services in cloud foundry.

allows you to standup and destroy cf 
services, pull binding information and
destroy instances.

### SAMPLE SCRIPTS: (sample_setup.sh & sample_teardown.sh)

w/ support for wercker in the form of
a wercker step to standup and destroy
service instances and grab binding information


### SAMPLE WERCKER USAGE:

```
deploy:
  steps:
    - xchapter7x/cf-bound-service-integration-test:
        user_name: $cfuser
        user_pass: $cfpass
        org: $cforg
        space: $cfspace
        api_url: $cfurl
        app_name: $cfappname
        service_instance: $serviceinstance
        service_type: $servicetype
        action: (setup / cleanup)
        outvar_name: $varname
```
