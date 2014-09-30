step-wercker-flowy-deploy
====================

a wercker step to help with automatic deploys inspired by gitflow


SAMPLE USAGE:

```
deploy:
  steps:
    - xchapter7x/flowy-deploy:
        action: "get-latest | get-next | complete-release"
        tag_variable_name: "my_tag_var" 
        active: true                                              #default
        tag_regex: "v([0-9]{1,2})\.([0-9]{1,2})\.([0-9]{1,4})"    #default
        start_version: "v01.00.0001"                              #default
        tag_message: "Auto-Tag"                                   #default
```
