
UTILNAME:=yaml
PKGNAME:=ruamel.yaml
VERSION:=$$(python setup.py --version)
REGEN:=/usr/local/bin/ruamel_util_new util --published --command YAML --skip-hg

include ~/.config/ruamel_util_new/Makefile.inc

# updatereadme for inclusion of examples in README.rst

clean:
	rm -rf build .tox $(PKGNAME).egg-info/ README.pdf
	find . -name "*.pyc" -exec rm {} +
	@find . -name "__pycache__" -print0  | xargs -r -0 rm -rf

