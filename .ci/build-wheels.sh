#!/bin/bash
set -e -x

export FOR_PRODUCTION=1

for PYBIN in /opt/python/*/bin; do
    if [ `${PYBIN}/python -c "import sys; print(1 if sys.version_info[:2] >= (3, 5) else 0)"` -eq 1 ]; then
        "${PYBIN}/pip" install --upgrade pip wheel
        "${PYBIN}/pip" install --upgrade setuptools
        # "${PYBIN}/pip" install -r /io/dev-requirements.txt
        "${PYBIN}/pip" install Cython
        "${PYBIN}/pip" wheel /io/ -w wheelhouse/
    fi
done

for whl in wheelhouse/*.whl; do
    auditwheel repair "$whl" -w /io/wheelhouse/
done

# for PYBIN in /opt/python/*/bin/; do
#     "${PYBIN}/pip" install python-manylinux-demo --no-index -f /io/wheelhouse
#     (cd "$HOME"; "${PYBIN}/nosetests" pymanylinuxdemo)
# done
