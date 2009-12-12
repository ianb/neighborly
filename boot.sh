#!/usr/bin/env bash

echo "This will setup the neighborly environment in ./neighborly"

if [ -e ./neighborly ] ; then
    echo "But no... that already exists!"
    exit 2
fi

if [ ! -e virtualenv.py ] ; then
    wget http://bitbucket.org/ianb/virtualenv/raw/tip/virtualenv.py || exit 3
else
    echo "virtualenv.py already exists"
fi
python virtualenv.py neighborly || exit 4
cd neighborly
./bin/pip install Django 
mkdir src
cd src
git clone git@github.com:ianb/libcloud.git
cd ..

