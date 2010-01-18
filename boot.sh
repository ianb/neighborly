#!/usr/bin/env bash

get_virtualenv () {
    if [ ! -e 'virtualenv.py' ] ; then
        echo -n "Fetching virtualenv..."
        wget -q http://bitbucket.org/ianb/virtualenv/raw/tip/virtualenv.py || exit 3
        echo "done."
    else
        echo "virtualenv.py already exists"
    fi
}

if [ "$1" = "setup-toppcloud" ] ; then
    shift
    DIR="$1"
    if [ -z "$DIR" ] ; then
        echo "You did not give a DIR argument"
        echo "usage: $(basename $0) setup-toppcloud DIR"
        exit 2
    fi
    get_virtualenv
    python2.6 virtualenv.py "$DIR"
    $DIR/bin/pip install http://bitbucket.org/ianb/toppcloud/raw/tip/requirements.txt
    echo
    echo "toppcloud installed"
    echo "Add $DIR/bin to your path, like:"
    echo "    \$ export PATH=\"$DIR/bin:$PATH\""
    echo "You may want to put this in ~/.bash_profile"
    echo "What the heck, I can do that for you.  Enter 'y' to have me do so:"
    read ANSWER
    if [ "$ANSWER" = y ] ; then
        echo "# Added by Neighborly's boot.sh" >> ~/.bash_profile
        echo "export PATH=\"$DIR/bin:\$PATH\"" >> ~/.bash_profile
        echo "Note: you must do:    source ~/.bash_profile"
        echo "before this path change will be made active"
    else
        echo "Alright, do it yourself then..."
    fi
    echo "Now we will configure toppcloud..."
    $DIR/bin/toppcloud
    exit
fi

if ! which toppcloud ; then
    if [ -e ~/.toppcloud.conf ] ; then
        echo "It appears toppcloud is (probably) installed, but not present on \$PATH"
        echo "Make sure to put the TOPPCLOUD_DIR/bin on your \$PATH"
        echo "Or reinstall toppcloud with ./boot.sh setup-toppcloud TOPPCLOUD_DIR"
    else
        echo "toppcloud is not setup on your environment; please call ./boot.sh setup-toppcloud TOPPCLOUD_DIR"
    fi
    exit 2
fi

if ! which git ; then
    echo "You must install git first"
    exit 3
fi

DIR="$1"

echo "This will setup the neighborly environment in $DIR"

toppcloud init $DIR
pushd $DIR
mkdir -p src/neighborly
if [ ! -e src/neighborly/.git ] ; then
    ## FIXME: this might fail if they don't have commit or authorization for ssh git access:
    git clone git@github.com:ianb/neighborly.git src/neighborly
else
    echo "Neighborly has already been checked out into $DIR/src/neighborly"
fi

if [ ! -L app.ini ] ; then
    rm app.ini
    ln -s src/neighborly/toppcloud-app.ini app.ini
fi

if [ ! -e lib/python/.git ] ; then
    if [ -e lib/python ] ; then
        echo "Removing lib/python"
        rm -r lib/python
    fi
    git clone git@github.com:ianb/neighborly-lib.git lib/python
else
    echo "neighborly-lib has already been checked out into $DIR/lib/python"
fi

if [ ! -L bin ] ; then
    echo "Moving bin/ into place"
    mv bin/activate bin/activate_this.py bin/python bin/python2.6 bin/pip bin/easy_install bin/easy_install-2.6 lib/python/bin
    rmdir bin
    ln -s lib/python/bin bin
fi

if ! which psql ; then
    echo "PostgreSQL does not appear to be installed, you must install it and the PostGIS extensions"
    exit 3
fi

T_POSTGIS="$(psql -l | grep template_postgis)"
if [ -z "$T_POSTGIS" ] ; then
    echo "It appears the template_postgis database does not exist"
    echo "Please create it, something like:"
    echo "    \$ createdb template_postgis"
    echo "    \$ psql template_postgis < PATH_TO_POSTGIS_FILES/lwpostgis.sql"
    echo "    \$ psql template_postgis < PATH_TO_POSTGIS_FILES/spatial_ref_sys.sql"
    exit 3
fi

T_NEIGHBORLY="$(psql -l | grep neighborly)"
if [ -z "$T_NEIGHBORLY" ] ; then
    echo "Creating neighborly database..."
    ## FIXME: not sure about the user here...
    PGUSER=postgres createdb -T template_postgis neighborly
else
    echo "neighborly database already created"
fi
