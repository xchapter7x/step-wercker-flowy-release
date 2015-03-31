import os
import subprocess
import sys
import core

def write_statefile(env_var_name, msg):
  f = open('.statefile', 'w')
  state_string = "export {0}={1}".format(env_var_name, msg)
  f.write(state_string)

def get_a_tag_using(functorArg, mainFunctor):
  msg = ""
  err = False
  variable_keyname = "WERCKER_FLOWY_RELEASE_TAG_VARIABLE_NAME"
  env_var_name = core.field_flags[variable_keyname]
  tag = mainFunctor(functorArg) 

  if env_var_name != None and tag != None:
    msg = tag
    os.environ[env_var_name] = msg
    write_statefile(env_var_name, msg)
    
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
  return "git flow release finish -m \"{1}\" {0}".format(version, tag_message)

def gitflow_release_push_string():
  return "git push origin master && git push --tags && git checkout develop && git push origin develop"

def setup_git_state(functor):
  functor("git config --global user.name \"{0}\"".format(core.field_flags["WERCKER_FLOWY_RELEASE_GIT_NAME"]))
  functor("git config --global user.email \"{0}\"".format(core.field_flags["WERCKER_FLOWY_RELEASE_GIT_EMAIL"]))
  functor("git checkout -b master origin/master && git pull origin master")
  functor("git checkout -b develop origin/develop")
  functor("git fetch --tags")
  functor("git flow init -fd")

def listify(l1, l2, l3):
  l = list(l1) + list(l2) + list(l3)
  return l

def tag_only_release(functor):
  tag = core.get_next_tag(functor)
  print(functor("git checkout -fq "+str(os.environ["WERCKER_GIT_COMMIT"])))
  print(functor("git submodule update --init --recursive"))
  print(functor("echo "+str(tag)))
  print(functor("git branch"))
  print(functor("git status"))
  print(functor("git log | head -10"))
  print(functor("git tag -a "+str(tag)+" -m \"version "+str(tag)+"\""))
  print(functor("git checkout -b localbuild || true"))
  print(functor("git checkout -b master origin/master || true"))
  print(functor("git checkout master"))
  print(functor("git pull origin master"))
  print(functor("git merge localbuild"))
  print(functor("git status"))
  print(functor("git log | head -10"))
  print(functor("git push origin master"))
  print(functor("git push --tags"))
  return (None, None)

def complete_release(functor):
  tag = core.get_next_tag(functor)
  smsg, serr = functor(gitflow_release_start_command_string(tag))
  fmsg, ferr = functor(gitflow_release_finish_command_string(tag))
  pmsg, perr = functor(gitflow_release_push_string())
  print(functor("git tag -l"))
  print(functor("git log master | head -10"))
  msg_chain = listify(smsg, fmsg, pmsg)
  err_chain = (serr or ferr or perr)
  return (msg_chain, err_chain)

def run_action(action, supported_actions):
  msg = ""
  err = False
  
  if action in supported_actions:
    setup_git_state(core.system_call)
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
      "tag-only-release": tag_only_release,
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

  return exitcode

if __name__ == '__main__':
  exit(run())

