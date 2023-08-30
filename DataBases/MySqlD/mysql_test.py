import testing.mysqld
from sqlalchemy import create_engine

# prevent generating brand new db every time.  Speeds up tests.
MYSQLD_FACTORY = testing.mysqld.MysqldFactory(cache_initialized_db=True, port=7531)

