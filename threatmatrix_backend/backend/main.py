import pandas as pd 
import sqlalchemy
import logging

from data_sources import *
from utils import upsert

log = logging.getLogger(__name__)


def main():
    log.info('starting')
    df = acled.get_data()
    upsert(df, 'events')


if __name__ == "__main__":
    logging.basicConfig(level="INFO")
    main()
