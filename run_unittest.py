import unittest
import run
import os

success_output = "some success output"
failure_output = "some error output"

def system_call_mock_success(cmdString):
  return (success_output, False)

def system_call_mock_failure(cmdString):
  return (failure_output, True)

def current_tag_functor_default_mock(cmdString):
  return ([cmdString], True)

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
    response = run.required_field_check(self.required_fields, mockEnv)
    self.assertFalse(response)

  def test_required_field_check_partial(self):
    """
    should return False if some fields
    are not set
    """
    mockEnv = {}
    mockEnv["WERCKER_FLOWY_DEPLOY_ACTION"] = "test"
    response = run.required_field_check(self.required_fields, mockEnv)
    self.assertFalse(response)

  def test_required_field_check_clean(self):
    """
    should return true if all requireds are set
    """
    mockEnv = {}
    mockEnv["WERCKER_FLOWY_DEPLOY_ACTION"] = "test"
    mockEnv["WERCKER_FLOWY_DEPLOY_TAG_VARIABLE_NAME"] = "test"
    response = run.required_field_check(self.required_fields, mockEnv)
    self.assertTrue(response)

  #def test_get_current_tag(self):
    #"""
    #this should return the current tag from 
    #the given functor when the functor is
    #passed the proper string
    #"""
    #response = run.get_current_tag(current_tag_functor_default_mock)
    #print(response)
    #self.assertTrue(response)

"""
    def test_tag_match_string:
    def test_version_increment_string:
    
    
    def test_get_next_tag
    def test_run
"""

if __name__ == '__main__':
  unittest.main()
