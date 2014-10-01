import os
import subprocess
import sys
import core

def get_a_tag_using(functorArg, mainFunctor):
  msg = ""
  err = False
  variable_keyname = "WERCKER_FLOWY_RELEASE_TAG_VARIABLE_NAME"
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

def gitflow_release_start_command_string(version):
  return "git flow release start {0} {1}".format(version, "develop")

def gitflow_release_finish_command_string(version):
  message_text = core.field_flags["WERCKER_FLOWY_RELEASE_TAG_MESSAGE"].replace(" ", "-")
  tag_message = "{0}-{1}".format(message_text, version)
  return "git flow release finish -p -m \"{1}\" {0}".format(version, tag_message)

def complete_release(functor):
  tag = core.get_next_tag(functor)
  functor("git config --global user.name \"{0}\"".format(core.field_flags["WERCKER_FLOWY_RELEASE_GIT_NAME"]))
  functor("git config --global user.email \"{0}\"".format(core.field_flags["WERCKER_FLOWY_RELEASE_GIT_EMAIL"]))
  functor("git checkout -b master origin/master")
  functor("git checkout -b develop origin/develop")
  functor("git flow init -fd")
  smsg, serr = functor(gitflow_release_start_command_string(tag))
  fmsg, ferr = functor(gitflow_release_finish_command_string(tag))
  print(functor("git tag -l"))
  print(functor("git log master | head -10"))
  msg_chain = smsg+fmsg
  err_chain = (serr or ferr)
  return (msg_chain, err_chain)

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
      "complete-release": complete_release,
      "get-latest": get_latest,
      "get-next": get_next
    }
    imsg, ierr = run_action(core.field_flags["WERCKER_FLOWY_RELEASE_ACTION"], supported_actions)
    print(imsg, ierr)
    
    if ierr:
      exitcode = 1
  
  elif not core.is_active():
    print("Step Skipped")
    exitcode = 0

  else:
    print("FAILED!!! %s" % msg)
    exitcode = 1

  exit(exitcode)

if __name__ == '__main__':
  run()

