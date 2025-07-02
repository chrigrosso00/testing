from src.database.db_operations import csv_to_sql
from src.logging.log_setup import get_logger

logger = get_logger(__name__)


def main():
    csv_to_sql()


if __name__ == "__main__":
    main()