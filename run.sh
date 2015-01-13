#!/bin/sh

sudo wget -P /tmp http://launchpadlibrarian.net/84618376/git-flow_0.4.1-2_all.deb
sudo dpkg -i /tmp/git-flow_0.4.1-2_all.deb

FAILED_RUN=0

python $WERCKER_STEP_ROOT/run.py

if [ $? != 0 ]; then
  FAILED_RUN=1
fi

if [ -f .statefile ];then
   source .statefile
fi

git checkout -fq ${WERCKER_GIT_COMMIT}
git submodule update --init --recursive

if [ $FAILED_RUN != 0 ]; then
  fail "Failure"

else
  success "Success"
fi
