# pushd /development/echomesh/code/python

find echomesh -name \*Test\*.py -exec ../bash/run_one_test.sh {} \;
echo "Tests complete."

# popd