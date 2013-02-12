# pushd /development/echomesh/code/python

PYTHONPATH="./external:." find echomesh -name \*Test\*.py -exec ../bash/run_one_test.sh {} \;
echo "Tests complete."

# popd