import os
import subprocess
import sys

required_fields = [
  "WERCKER_FLOWY_RELEASE_ACTION",
  "WERCKER_FLOWY_RELEASE_TAG_VARIABLE_NAME",
  "WERCKER_FLOWY_RELEASE_GIT_NAME",
  "WERCKER_FLOWY_RELEASE_GIT_EMAIL"
]

def get_active_flag():
  active_string = os.environ.get("WERCKER_FLOWY_RELEASE_ACTIVE", "true")
  active_flag = True

  if active_string == "false":
    active_flag = False

  return active_flag

field_flags = {
  "WERCKER_FLOWY_RELEASE_ACTION":              os.environ.get("WERCKER_FLOWY_RELEASE_ACTION", None),
  "WERCKER_FLOWY_RELEASE_TAG_VARIABLE_NAME":   os.environ.get("WERCKER_FLOWY_RELEASE_TAG_VARIABLE_NAME", None),
  "WERCKER_FLOWY_RELEASE_GIT_NAME":            os.environ.get("WERCKER_FLOWY_RELEASE_GIT_NAME", None),
  "WERCKER_FLOWY_RELEASE_GIT_EMAIL":           os.environ.get("WERCKER_FLOWY_RELEASE_GIT_EMAIL", None),
  "WERCKER_FLOWY_RELEASE_ACTIVE":              get_active_flag(),
  "WERCKER_FLOWY_RELEASE_TAG_REGEX":           os.environ.get("WERCKER_FLOWY_RELEASE_TAG_REGEX", "v([0-9]{1,2})\.([0-9]{1,2})\.([0-9]{1,4})"),
  "WERCKER_FLOWY_RELEASE_START_VERSION":       os.environ.get("WERCKER_FLOWY_RELEASE_START_VERSION", "v01.00.0001"),
  "WERCKER_FLOWY_RELEASE_TAG_MESSAGE":         os.environ.get("WERCKER_FLOWY_RELEASE_TAG_MESSAGE", "Auto-Generated-Tag")
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
  return field_flags["WERCKER_FLOWY_RELEASE_ACTIVE"]

def should_run():
  msg, passed = required_field_check(required_fields, os.environ)
  rerr = (not is_active() or not passed)
  return (msg, rerr)

def version_increment_string(current_version):
  return """echo """+current_version+""" | perl -ne 'chomp; print join(".", splice(@{[split/\./,$_]}, 0, -1), map {++$_} pop @{[split/\./,$_]});'"""

def tag_match_string():
  output = ""
  return ("git tag -l | egrep \"%s\"" % field_flags["WERCKER_FLOWY_RELEASE_TAG_REGEX"])

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

def version_sorted(version_array):
  v_sorted_response = []

  try:
    v_sorted_response = sorted(version_array, key=lambda s: map(int, s.split('.')), reverse=True)
  
  except:
    v_sorted_response = sorted(version_array, key=lambda s: map(str, s.split('.')), reverse=True)

  return v_sorted_response

def get_current_tag(functor):
  current_tag = None
  out, err = functor(tag_match_string())

  if not err:
    tags = version_sorted(out)
    current_tag = tags[0]

  return current_tag

def get_next_tag(functor):
  current = get_current_tag(functor)
  
  if current == None:
    current = field_flags["WERCKER_FLOWY_RELEASE_START_VERSION"]

  out, err = functor(version_increment_string(current))
  return out[0]


