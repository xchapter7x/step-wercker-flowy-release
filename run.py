import os
import subprocess
import sys
import core

def create_tag():
  print("create tag")

def get_latest():
  core.get_current_tag(core.system_call) 
  print("get latest")

def get_next():
  print("get next")

def cut_release():
  print("cut release")

def run_action(action, supported_actions):
  msg = ""
  err = False
  supported_actions = {
    "create-tag": create_tag,
    "get-latest": get_latest,
    "get-next": get_next,
    "cut-release": cut_release
  }

  if action in supported_actions:
    supported_actions[action]()

  else:
    err = True
    msg = "Key {0} does not exist".format(action)

  return (msg, err)

def run():
  exitcode = 0
  msg, err = core.required_field_check(core.required_fields, os.environ)

  if not err:
    run_action(core.field_flags["WERCKER_FLOWY_DEPLOY_ACTION"])

    """
    print("do nothing")
    out, err = system_call(tag_match_string())
    print(out, err)
    out, err = system_call(version_increment_string("v1.0.4"))
    print(out, err)
    print( get_current_tag(system_call) )
    print(  get_next_tag(system_call) )
    """

  else:
    print("FAILED!!! %s" % msg)
    exitcode = 1

  exit(exitcode)

if __name__ == '__main__':
  run()
