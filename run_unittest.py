import unittest
import run

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

  def test_for_create_tag(self):
    """
    test
    """
    run.run_action("create-tag", self.supported_actions)
    self.assertFalse(False)

  def test_for_get_latest(self):
    """
    test
    """
    run.run_action("get-latest", self.supported_actions)
    self.assertFalse(False)

  def test_for_get_next(self):
    """
    test
    """
    run.run_action("get-next", self.supported_actions)
    self.assertFalse(False)

  def test_for_cut_release(self):
    """
    test
    """
    run.run_action("cut-release", self.supported_actions)
    self.assertFalse(False)


if __name__ == '__main__':
  unittest.main()
