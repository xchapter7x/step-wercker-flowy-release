#!/bin/sh

sudo wget -P /tmp http://launchpadlibrarian.net/84618376/git-flow_0.4.1-2_all.deb
sudo dpkg -i /tmp/git-flow_0.4.1-2_all.deb

python $WERCKER_STEP_ROOT/run.py

if [ $? != 0 ]; then
  fail "Failure"

else
  success "Success"
fi
