#! /bin/bash

for FILE in app/api/tests/*; do
  pytest $FILE -W ignore::pytest.PytestCollectionWarning;
  rm "app/database/test.sqlite";
done
