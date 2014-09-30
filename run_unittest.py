import unittest
import run
import core
import os

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
    variable_keyname = "WERCKER_FLOWY_DEPLOY_TAG_VARIABLE_NAME"
    core.field_flags[variable_keyname] = "MY_TEST_VAR"
    latest, err = run.get_latest(mock_error_passthrough)
    self.assertTrue(err)

  def test_for_get_latest(self):
    """
    get latest should return version_tag
    returned from the functor
    """
    variable_keyname = "WERCKER_FLOWY_DEPLOY_TAG_VARIABLE_NAME"
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
    variable_keyname = "WERCKER_FLOWY_DEPLOY_TAG_VARIABLE_NAME"
    core.field_flags[variable_keyname] = None
    latest, err = run.get_latest(mock_success_passthrough)
    self.assertTrue(err)


















  def test_for_create_tag(self):
    """
    test
    """
    control = None
    latest, err = run.create_tag(mock_error_passthrough)
    self.assertEqual(latest, control)

  def test_for_get_next(self):
    """
    test
    """
    control = None
    latest, err = run.get_next(mock_error_passthrough)
    self.assertEqual(latest, control)

  def test_for_cut_release(self):
    """
    test
    """
    control = None
    latest, err = run.cut_release(mock_error_passthrough)
    self.assertEqual(latest, control)


if __name__ == '__main__':
  unittest.main()
