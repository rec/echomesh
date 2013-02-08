pushd /development/echomesh/code/python

EXCLUDE=".*/(Echomesh|FilePlayer|Microphone|Processor|Sound|Sprite|Keyboard).py"

find -E echomesh \( -name \*.py -and -not -regex "$EXCLUDE" \) -exec ../bash/run_one_test.sh {} \;
echo "Tests complete."