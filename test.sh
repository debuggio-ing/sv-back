#! /bin/bash

rm "app/database/test.sqlite";

for FILE in app/tests/*; do
  coverage run --source=app/routers,app/crud -a -m pytest $FILE -W ignore::pytest.PytestCollectionWarning;
  rm "app/database/test.sqlite";
done

coverage report -m;
coverage erase;
