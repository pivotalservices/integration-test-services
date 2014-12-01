#!/bin/sh
if [ ! -n "$WERCKER_CF_BOUND_SERVICE_INTEGRATION_TEST_API_URL" ]
then
    fail 'missing or empty option api_url, please check wercker.yml'
fi

if [ ! -n "$WERCKER_CF_BOUND_SERVICE_INTEGRATION_TEST_USER_NAME" ]
then
    fail 'missing or empty option user_name, please check wercker.yml'
fi

if [ ! -n "$WERCKER_CF_BOUND_SERVICE_INTEGRATION_TEST_USER_PASS" ]
then
    fail 'missing or empty option user_pass, please check wercker.yml'
fi

if [ ! -n "$WERCKER_CF_BOUND_SERVICE_INTEGRATION_TEST_ORG" ]
then
    fail 'missing or empty option org, please check wercker.yml'
fi

if [ ! -n "$WERCKER_CF_BOUND_SERVICE_INTEGRATION_TEST_SPACE" ]
then
    fail 'missing or empty option space, please check wercker.yml'
fi

if [ ! -n "$WERCKER_CF_BOUND_SERVICE_INTEGRATION_TEST_APP_NAME" ]
then
    fail 'missing or empty option app_name, please check wercker.yml'
fi

if [ ! -n "$WERCKER_CF_BOUND_SERVICE_INTEGRATION_TEST_SERVICE_INSTANCE_NAME" ]
then
    fail 'missing or empty option instance_name, please check wercker.yml'
fi

if [ ! -n "$WERCKER_CF_BOUND_SERVICE_INTEGRATION_TEST_SERVICE_TYPE" ]
then
    fail 'missing or empty option service_type, please check wercker.yml'
fi

if [ ! -n "$WERCKER_CF_BOUND_SERVICE_INTEGRATION_TEST_SERVICE_PLAN" ]
then
    fail 'missing or empty option service_plan, please check wercker.yml'
fi

if [ ! -n "$WERCKER_CF_BOUND_SERVICE_INTEGRATION_TEST_ACTION" ]
then
    fail 'missing or empty option action, please check wercker.yml'
fi

if [ ! -n "$WERCKER_CF_BOUND_SERVICE_INTEGRATION_TEST_OUTVAR_NAME" ]
then
    fail 'missing or empty option outvar_name, please check wercker.yml'
fi
 

wget http://go-cli.s3-website-us-east-1.amazonaws.com/releases/v6.3.2/cf-linux-amd64.tgz
tar -zxvf cf-linux-amd64.tgz
CF=$(pwd)/cf
${CF} api ${WERCKER_CF_BOUND_SERVICE_INTEGRATION_TEST_API_URL}

${CF} login -u ${WERCKER_CF_BOUND_SERVICE_INTEGRATION_TEST_USER_NAME} -p ${WERCKER_CF_BOUND_SERVICE_INTEGRATION_TEST_USER_PASS} -o ${WERCKER_CF_BOUND_SERVICE_INTEGRATION_TEST_ORG} -s ${WERCKER_CF_BOUND_SERVICE_INTEGRATION_TEST_SPACE}

export CF_CLI=${CF}
export ORG=${WERCKER_CF_BOUND_SERVICE_INTEGRATION_TEST_ORG}
export SPACE=${WERCKER_CF_BOUND_SERVICE_INTEGRATION_TEST_SPACE}
export APP_NAME=${WERCKER_CF_BOUND_SERVICE_INTEGRATION_TEST_APP_NAME}
export SERVICE_INSTANCE_NAME=${WERCKER_CF_BOUND_SERVICE_INTEGRATION_TEST_SERVICE_INSTANCE_NAME}
export SERVICE_TYPE=${WERCKER_CF_BOUND_SERVICE_INTEGRATION_TEST_SERVICE_TYPE}
export SERVICE_PLAN=${WERCKER_CF_BOUND_SERVICE_INTEGRATION_TEST_SERVICE_PLAN}
export ACTION=${WERCKER_CF_BOUND_SERVICE_INTEGRATION_TEST_ACTION}
TMPOUTPUT=(cd $WERCKER_STEP_ROOT && python run.py)
echo ${TMPOUTPUT}
eval "export ${WERCKER_CF_BOUND_SERVICE_INTEGRATION_TEST_OUTVAR_NAME}=${TMPOUTPUT}"

if [[ $? -ne 0 ]];then
    warning $push_output
    fail 'integration test helper run failed';

else
    success 'finished integration test helper run';

fi
