import unittest
import run
import core
import os

control_version = "v1.0.3"

def mock_version_functor(cmdString):
  return ([control_version], False)

def mock_success_passthrough(cmdString):
  return ([cmdString], False)

def mock_error_passthrough(cmdString):
  return ([cmdString], True)

class RunTestCase(unittest.TestCase):
  """Tests for `run.py`."""
  
  @classmethod
  def setUpClass(self):
    self.supported_actions = {
      "create-tag": lambda: True,
      "get-latest": lambda: True,
      "get-next": lambda: True,
      "cut-release": lambda: True
    }

  def test_for_get_latest_unset(self):
    """
    get latest should return None when no previous tags
    are found
    """
    variable_keyname = "WERCKER_FLOWY_RELEASE_TAG_VARIABLE_NAME"
    core.field_flags[variable_keyname] = "MY_TEST_VAR"
    latest, err = run.get_latest(mock_error_passthrough)
    self.assertTrue(err)

  def test_for_get_latest(self):
    """
    get latest should return version_tag
    returned from the functor
    """
    variable_keyname = "WERCKER_FLOWY_RELEASE_TAG_VARIABLE_NAME"
    core.field_flags[variable_keyname] = "MY_TEST_VAR"
    control = 'git tag -l | egrep "v([0-9]{1,2})\\.([0-9]{1,2})\\.([0-9]{1,4})"'
    latest, err = run.get_latest(mock_success_passthrough)
    self.assertEqual(latest, control)
    self.assertEqual(os.environ[core.field_flags[variable_keyname]], control)
    self.assertFalse(err)

  def test_for_get_latest_unset_var(self):
    """
    get latest should return an 
    error if there is no variable name set
    """
    variable_keyname = "WERCKER_FLOWY_RELEASE_TAG_VARIABLE_NAME"
    core.field_flags[variable_keyname] = None
    latest, err = run.get_latest(mock_success_passthrough)
    self.assertTrue(err)

  def test_for_get_next_unset(self):
    """
    get_next should return a default based value when no tags
    are found
    """
    control = 'echo v01.00.0001 | awk -F. -v OFS=. \'NF==1{print ++$NF};NF>1{if(length($NF+1)>length($NF))$(NF-1)++;$NF=sprintf("%0*d",length($NF),($NF+1)%(10^length($NF))); print}\''
    variable_keyname = "WERCKER_FLOWY_RELEASE_TAG_VARIABLE_NAME"
    core.field_flags[variable_keyname] = "MY_TEST_VAR"
    latest, err = run.get_next(mock_error_passthrough)
    self.assertEqual(latest, control)
    self.assertFalse(err)

  def test_for_get_next(self):
    """
    get_next should return version_tag
    returned from the functor
    """
    variable_keyname = "WERCKER_FLOWY_RELEASE_TAG_VARIABLE_NAME"
    core.field_flags[variable_keyname] = "MY_TEST_VAR"
    control = 'echo git tag -l | egrep "v([0-9]{1,2})\\.([0-9]{1,2})\\.([0-9]{1,4})" | awk -F. -v OFS=. \'NF==1{print ++$NF};NF>1{if(length($NF+1)>length($NF))$(NF-1)++;$NF=sprintf("%0*d",length($NF),($NF+1)%(10^length($NF))); print}\''
    latest, err = run.get_next(mock_success_passthrough)
    self.assertEqual(latest, control)
    self.assertEqual(os.environ[core.field_flags[variable_keyname]], control)
    self.assertFalse(err)

  def test_for_get_next_unset_var(self):
    """
    get_next should return an 
    error if there is no variable name set
    """
    variable_keyname = "WERCKER_FLOWY_RELEASE_TAG_VARIABLE_NAME"
    core.field_flags[variable_keyname] = None
    latest, err = run.get_next(mock_success_passthrough)
    self.assertTrue(err)

  def test_for_complete_release(self):
    """
    should return no errors from either
    command and a proper concatenation of 
    return message values
    """
    control = [control_version, control_version, control_version, control_version]
    latest, err = run.complete_release(mock_version_functor)
    self.assertEqual(latest, control)
    self.assertFalse(err)

if __name__ == '__main__':
  unittest.main()
