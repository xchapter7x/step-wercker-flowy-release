import os
import subprocess
import sys

required_fields = [
  "WERCKER_FLOWY_DEPLOY_ACTION",
  "WERCKER_FLOWY_DEPLOY_TAG_VARIABLE_NAME"
]

def get_active_flag():
  active_string = os.environ.get("WERCKER_FLOWY_DEPLOY_ACTIVE", "true")
  active_flag = True

  if active_string == "false":
    active_flag = False

  return active_flag

field_flags = {
  "WERCKER_FLOWY_DEPLOY_ACTION":              os.environ.get("WERCKER_FLOWY_DEPLOY_ACTION", None),
  "WERCKER_FLOWY_DEPLOY_TAG_VARIABLE_NAME":   os.environ.get("WERCKER_FLOWY_DEPLOY_TAG_VARIABLE_NAME", None),
  "WERCKER_FLOWY_DEPLOY_ACTIVE":              get_active_flag(),
  "WERCKER_FLOWY_DEPLOY_TAG_REGEX":           os.environ.get("WERCKER_FLOWY_DEPLOY_TAG_REGEX", "v([0-9]{1,2})\.([0-9]{1,2})\.([0-9]{1,4})"),
  "WERCKER_FLOWY_DEPLOY_START_VERSION":       os.environ.get("WERCKER_FLOWY_DEPLOY_START_VERSION", "v01.00.0001"),
  "WERCKER_FLOWY_DEPLOY_TAG_MESSAGE":         os.environ.get("WERCKER_FLOWY_DEPLOY_TAG_MESSAGE", "Auto-Generated-Tag")
}

def required_field_check(required_fields, env_variables):
  checkPassed = True
  msg = ""

  for fieldname in required_fields:

    if not env_variables.has_key(fieldname):
      checkPassed = False
      msg += "Required ENV Variable not set: %s" % (fieldname)
    
  return (msg, checkPassed)

def is_active():
  return field_flags["WERCKER_FLOWY_DEPLOY_ACTIVE"]

def should_run():
  msg, passed = required_field_check(required_fields, os.environ)
  rerr = (not is_active() or not passed)
  return (msg, rerr)

def version_increment_string(current_version):
  return """echo """+current_version+""" | awk -F. -v OFS=. 'NF==1{print ++$NF};NF>1{if(length($NF+1)>length($NF))$(NF-1)++;$NF=sprintf("%0*d",length($NF),($NF+1)%(10^length($NF))); print}'"""

def tag_match_string():
  output = ""
  return ("git tag -l | egrep \"%s\"" % field_flags["WERCKER_FLOWY_DEPLOY_TAG_REGEX"])

def make_array_from_stdout(output):
  output = output.rstrip("\n").split("\n")
  return output

def system_call(cmdString):
  output = []
  err = False

  try:
    stdout = subprocess.check_output(cmdString, shell=True)
    output = make_array_from_stdout(stdout)
    
  except subprocess.CalledProcessError as e:
    output = "error: {0}".format(e)
    err = True

  return (output, err)

def get_current_tag(functor):
  current_tag = None
  out, err = functor(tag_match_string())

  if not err:
    tags = sorted(out, reverse=True)
    current_tag = tags[0]

  return current_tag

def get_next_tag(functor):
  current = get_current_tag(functor)
  
  if current == None:
    current = field_flags["WERCKER_FLOWY_DEPLOY_START_VERSION"]

  out, err = functor(version_increment_string(current))
  return out[0]


