from datetime import datetime
from pony.orm import *

from app.database.crud_helpers.vote import *
from app.database.crud_helpers.game import *
from app.database.crud_helpers.player import *
from app.database.crud_helpers.user import *
from app.database.crud_helpers.lobby import *
from app.database.crud_helpers.populate_database import *


if True:
    db.bind(provider='sqlite', filename='testing1.sqlite', create_db=True)
else:
    db.bind(provider='sqlite', filename='testing2.sqlite', create_db=True)
db.generate_mapping(create_tables=True)
