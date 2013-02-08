# pushd /development/echomesh/code/python

#EXCLUDE=".*/(Echomesh|FilePlayer|Microphone|Processor|Sound|Sprite|Keyboard).py"
# find -E echomesh \( -name \*Test\*.py -and -not -regex "$EXCLUDE" \) -exec ../bash/run_one_test.sh {} \;

find echomesh -name \*Test\*.py -exec ../bash/run_one_test.sh {} \;
echo "Tests complete."

# popd