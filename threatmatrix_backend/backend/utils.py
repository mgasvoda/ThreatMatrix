import logging
import os
import time

import sqlalchemy
import pandas as pd
import numpy as np

from db import db_location
from sqlalchemy.dialects.sqlite import insert

log = logging.getLogger(os.path.dirname(__file__))
engine = sqlalchemy.create_engine(db_location)
conn = engine.connect()


def upsert(df, table, index=None):
    with engine.connect() as conn:
        metadata = sqlalchemy.MetaData(engine)
        metadata.reflect()
        table = metadata.tables[table]
        df = df.where((pd.notnull(df)), None)

        if len(df) == 0:
            log.info('Nothing new to add')
            return

        elif len(df) > 1000:
            for sub_df in np.array_split(df, len(df) / 1000):
                records = sub_df.to_dict(orient='records')
                insert_stmt = insert(table).values(records)
                if index:
                    do_nothing_stmt = insert_stmt.on_conflict_do_nothing(
                        index_elements=index
                    )
                    conn.execute(do_nothing_stmt)
                else:
                    conn.execute(insert_stmt)
                time.sleep(1)
        else:
            records = df.to_dict(orient='records')
            insert_stmt = insert(table).values(records)
            if index:
                do_nothing_stmt = insert_stmt.on_conflict_do_nothing(
                    index_elements=index
                )
                conn.execute(do_nothing_stmt)
            else:
                conn.execute(insert_stmt)

