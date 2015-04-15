
UTILNAME:=yaml
PKGNAME:=ruamel.yaml
VERSION:=$(shell python setup.py --version)
REGEN:=/home/bin/ruamel_util_new util --published --command YAML --skip-hg

include ~/.config/ruamel_util_new/Makefile.inc

clean:	clean_common


#tstvenv: testvenv testsetup testtest
#
#testvenv:
#	virtualenv -p /opt/python/2.7/bin/python testvenv
#
#testsetup:
#	testvenv/bin/pip install -e .
#	testvenv/bin/pip install pytest
#
#testtest:
#	testvenv/bin/py.test
