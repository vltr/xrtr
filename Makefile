SPHINXOPTS    =
SPHINXBUILD   = sphinx-build
SPHINXPROJ    = xrtr
SOURCEDIR     = docs/source
BUILDDIR      = docs/build

# Put it first so that "make" without argument is like "make help".
help:
	@$(SPHINXBUILD) -M help "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)
	@echo "clean - let this project be near mint"
	@echo "test - run tests with coverage"
	@echo "docker-build - build this package using pypa's docker images"

.PHONY: help Makefile

%: Makefile
	@$(SPHINXBUILD) -M $@ "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)

black:
	black ./src/ ./tests setup.py

cleanpycache:
	find . -type d | grep "__pycache__" | xargs rm -rf

clean: cleanpycache
	rm -f ./.coverage
	rm -f ./.coverage.*
	rm -rf ./.pytest_cache
	rm -rf ./.tox
	rm -rf ./build
	rm -rf ./dist
	rm -rf ./htmlcov
	rm -rf ./src/*.egg-info
	rm -rf ./src/*.c
	rm -rf ./src/*.so

test: clean
	python setup.py build_ext --force --inplace
	PYTHONPATH=$(PYTHONPATH):./src pytest --cov --cov-report=term-missing -vv tests

requirements-dev:
	pip install pip-tools
	pip-compile -r -U requirements-dev.in --output-file requirements-dev.txt
	# pip-compile -r -U
	# pip-sync requirements-dev.txt requirements.txt
	pip-sync requirements-dev.txt

docker-build: clean
	python setup.py clean --all sdist
	docker pull quay.io/pypa/manylinux1_x86_64:latest
	docker pull quay.io/pypa/manylinux1_i686:latest
	docker run --rm -i -v `pwd`:/io quay.io/pypa/manylinux1_x86_64 /io/.ci/build-wheels.sh
	docker run --rm -i -v `pwd`:/io quay.io/pypa/manylinux1_i686 /io/.ci/build-wheels.sh
	cp wheelhouse/*.whl dist/

# release:
# 	tox -e check
# 	python setup.py clean --all sdist bdist
# 	twine upload --skip-existing dist/*.whl dist/*.gz dist/*.zip
