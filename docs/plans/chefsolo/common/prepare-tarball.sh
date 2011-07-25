#!/bin/bash

# directory containing this script and the chef cookbooks directory
COMMON_DIR_REL="`dirname $0`"
COMMON_DIR=`cd $COMMON_DIR_REL; pwd`

# move into this directory in order to make commands simpler
cd $COMMON_DIR

if [ ! -d cookbooks ]; then
  echo "error, packaging script cannot orient itself, no cookbooks directory?"
  exit 1
fi

if [ ! -f chefsolo.sh ]; then
  echo "error, packaging script cannot orient itself, no chefsolo.sh file?"
  exit 1
fi

if [ -f cookbooks.tar.gz ]; then
  rm cookbooks.tar.gz
  echo "Removed old cookbooks.tar.gz"
fi

cp chefsolo.sh cookbooks/run.sh
if [ $? -ne 0 ]; then
  echo "could not create run.sh"
  exit 1
fi

tar czf cookbooks.tar.gz cookbooks
if [ $? -ne 0 ]; then
  echo "could not create tarball"
  exit 1
fi

echo "Created cookbooks.tar.gz"
