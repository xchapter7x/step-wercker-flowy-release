import unittest
import run
import os

success_output = "some success output"
failure_output = "some error output"
next_tag = "v1.0.02"
default_next_tag = "v01.00.0002"
current_tag = "v1.0.01"
default_current_tag = "v01.00.0001"

def system_call_mock_success(cmdString):
  return (success_output, False)

def system_call_mock_next_tag(cmdString):

  if cmdString == run.version_increment_string(current_tag):
    return run.system_call(cmdString)

  else:
    return ([current_tag], False)

def system_call_mock_next_tag_default(cmdString):

  if cmdString == run.version_increment_string(default_current_tag):
    return run.system_call(cmdString)

  else:
    return ([run.field_flags["WERCKER_FLOWY_DEPLOY_START_VERSION"]], False)


def system_call_mock_failure(cmdString):
  return (failure_output, True)

def current_tag_functor_default_mock(cmdString):
  return ([cmdString], False)

class ParserTestCase(unittest.TestCase):
  """Tests for `run.py`."""
  
  @classmethod
  def setUpClass(self):
    self.required_fields = [
      "WERCKER_FLOWY_DEPLOY_ACTION",
      "WERCKER_FLOWY_DEPLOY_TAG_VARIABLE_NAME"
    ]

  def test_system_call_success(self):
    """
    success should yield False error and
    an array matching out control
    """
    control = ["hi there"]
    o, e = run.system_call("echo "+control[0])
    self.assertFalse(e)
    self.assertEqual(o, control, "{0} != {1}".format(o, control) )

  def test_system_call_failure(self):
    """
    failure result from the command sent to
    system_call should yield a 'True' error value 
    response
    """
    o, e = run.system_call("exit 1")
    self.assertTrue(e)

  def test_make_array_from_stdout(self):
    """
    make_array_from_stdout should split the
    string output properly
    and clean trailing empty values
    """
    controlString = "hi\nthere\nmy test\nis done\n"
    controlResult = controlString.split("\n")
    del controlResult[-1]
    out = run.make_array_from_stdout(controlString)
    self.assertEqual(out, controlResult, "{0} != {1}".format(out, controlResult) )

  def test_make_array_from_stdout_noempty(self):
    """
    if no trailing empties then no
    deleting of record  
    """
    controlString = "hi\nthere\nmy test\nis done"
    controlResult = controlString.split("\n")
    out = run.make_array_from_stdout(controlString)
    self.assertEqual(out, controlResult, "{0} != {1}".format(out, controlResult) )

  def test_required_field_check(self):
    """
    should return False if all required fields
    are not set
    """
    mockEnv = {}
    msg, response = run.required_field_check(self.required_fields, mockEnv)
    self.assertFalse(response)

  def test_required_field_check_partial(self):
    """
    should return False if some fields
    are not set
    """
    mockEnv = {}
    mockEnv["WERCKER_FLOWY_DEPLOY_ACTION"] = "test"
    msg, response = run.required_field_check(self.required_fields, mockEnv)
    self.assertFalse(response)

  def test_required_field_check_clean(self):
    """
    should return true if all requireds are set
    """
    mockEnv = {}
    mockEnv["WERCKER_FLOWY_DEPLOY_ACTION"] = "test"
    mockEnv["WERCKER_FLOWY_DEPLOY_TAG_VARIABLE_NAME"] = "test"
    msg, response = run.required_field_check(self.required_fields, mockEnv)
    self.assertTrue(response)

  def test_get_current_tag_default(self):
    """
    should run the functor passed the default value
    """
    control = 'git tag -l | egrep "v([0-9]{1,2})\.([0-9]{1,2})\.([0-9]{1,4})"'
    response = run.get_current_tag(current_tag_functor_default_mock)
    self.assertEqual(response, control)

  def test_get_current_tag_env(self):
    """
    should run the functor passed the ENV_VAR value
    """
    revert = run.field_flags["WERCKER_FLOWY_DEPLOY_TAG_REGEX"]
    control = 'my control env variable'
    run.field_flags["WERCKER_FLOWY_DEPLOY_TAG_REGEX"] = control
    response = run.get_current_tag(current_tag_functor_default_mock)
    self.assertEqual(response, "git tag -l | egrep \"{0}\"".format(control))
    run.field_flags["WERCKER_FLOWY_DEPLOY_TAG_REGEX"] = revert

  def test_get_next_tag(self):
    """
    should return an incremented version
    tag from the value it is passed
    """
    current = current_tag
    control = next_tag
    newVersion = run.get_next_tag(system_call_mock_next_tag)
    self.assertEqual(newVersion, control)

  def test_get_next_tag_default(self):
    """
    should return an incremented version
    tag from the default version
    """
    control = default_next_tag
    newVersion = run.get_next_tag(system_call_mock_next_tag_default)
    self.assertEqual(newVersion, control)

if __name__ == '__main__':
  unittest.main()
