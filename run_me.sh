#!/bin/bash

for cmd in gsutil docker python java; do
  
  if hash "$cmd" 2>/dev/null; then
    :
  else
    echo "\"$cmd\"" is missing
    exit 1
  fi
done

FILE=cromwell.jar
if [ ! -f "$FILE" ]; then
    echo "$FILE does not exist."
    exit 1
fi

docker compose build

gsutil -m cp -r gs://terra-featured-workspaces/Cumulus/cellranger_output .

python rename_h5.py -i cellranger_output -o .

java -Dconfig.file=custom.conf -jar cromwell.jar run single_cell.wdl -i input_many.json
