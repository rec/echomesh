python -m doctest "$1"

if [ $? -ne 0 ]
then
  echo "ERROR: $1"
fi