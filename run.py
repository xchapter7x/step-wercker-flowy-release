import os

required_fields = [
  "WERCKER_FLOWY_DEPLOY_ACTION",
  "WERCKER_FLOWY_DEPLOY_TAG_VARIABLE_NAME"
]

field_flag_actions = {
  "WERCKER_FLOWY_DEPLOY_ACTION":              lambda v: v if v != None else "",
  "WERCKER_FLOWY_DEPLOY_TAG_VARIABLE_NAME":   lambda v: v if v != None else "",
  "WERCKER_FLOWY_DEPLOY_ACTIVE":              lambda v: v if v != None else True,
  "WERCKER_FLOWY_DEPLOY_TAG_REGEX":           lambda v: v if v != None else "v([0-9]{1,2})\.([0-9]{1,2})\.([0-9]{1,4})",
  "WERCKER_FLOWY_DEPLOY_START_VERSION":       lambda v: v if v != None else "v01.00.0001",
  "WERCKER_FLOWY_DEPLOY_TAG_MESSAGE":         lambda v: v if v != None else "Auto-Tag"
}

def run():
  print("do nothing")

if __name__ == '__main__':
  run()
