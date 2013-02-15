# pushd /development/echomesh/code/python

PYTHONPATH="./external:." find test -name \*.py -exec ../bash/run_one_test.sh {} \;
echo "Tests complete."

# popd