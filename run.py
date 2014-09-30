import os
import subprocess
import sys
import core

def get_a_tag_using(functorArg, mainFunctor):
  msg = ""
  err = False
  variable_keyname = "WERCKER_FLOWY_DEPLOY_TAG_VARIABLE_NAME"
  env_var_name = core.field_flags[variable_keyname]
  tag = mainFunctor(functorArg) 

  if env_var_name != None and tag != None:
    msg = tag
    os.environ[env_var_name] = msg

  else:
    msg = "no variable name value passed or None Tag Value"
    err = True
  
  return (msg, err)

def get_latest(functor):
  return get_a_tag_using(functor, core.get_current_tag)

def get_next(functor):
  return get_a_tag_using(functor, core.get_next_tag)

def create_tag(functor):
  return (None, False)

def cut_release(functor):
  return (None, False)

def run_action(action, supported_actions):
  msg = ""
  err = False
  
  if action in supported_actions:
    msg, err = supported_actions[action](core.system_call)

  else:
    err = True
    msg = "Key {0} does not exist".format(action)

  return (msg, err)

def run():
  exitcode = 0
  msg, err = core.should_run()

  if not err:
    supported_actions = {
      "create-tag": create_tag,
      "get-latest": get_latest,
      "get-next": get_next,
      "cut-release": cut_release
    }
    imsg, ierr = run_action(core.field_flags["WERCKER_FLOWY_DEPLOY_ACTION"], supported_actions)
    print(imsg, ierr)

  else:
    print("FAILED!!! %s" % msg)
    exitcode = 1

  exit(exitcode)

if __name__ == '__main__':
  run()


  
"""
print("do nothing")
out, err = system_call(tag_match_string())
print(out, err)
out, err = system_call(version_increment_string("v1.0.4"))
print(out, err)
print( get_current_tag(system_call) )
print(  get_next_tag(system_call) )
"""

