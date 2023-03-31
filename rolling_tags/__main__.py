import logging

from rolling_tags.config import setup_logger, token
from rolling_tags.rolling_tags_client import client


def main():
    setup_logger(logging.getLogger(__package__))
    client.run(token)


if __name__ == "__main__":
    main()
