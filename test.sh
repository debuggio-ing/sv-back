#! /bin/bash

rm "app/database/test.sqlite";

for FILE in app/api/tests/*; do
  coverage run --source=app/api/routers,app/database/crud_helpers -a -m pytest $FILE -W ignore::pytest.PytestCollectionWarning;
  rm "app/database/test.sqlite";
done

coverage report -i;
coverage erase;
