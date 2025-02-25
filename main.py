"""
main
----
Top-level entry-point for running an individual pipeline step.

run_process()
    Run a single step in the thesaurus-analytics pipeline,
    as specified by command-line arguments.
"""

import sys
import time
import logging
import logging.handlers

import click

from src import config, router


@click.command()
@click.argument("processing_step", type=str)
def run_process(processing_step: str) -> None:
    """
    Run a single step in the thesaurus-analytics pipeline,
    as specified by command-line arguments.
    """
    # Log the process
    logger = _initialize_logger()
    start_message = processing_step
    logger.info(start_message)

    # Run the process
    start_time = time.time()
    router.run_process(processing_step)
    end_time = time.time()
    elapsed_minutes = int((end_time - start_time) / 60)

    # Log completion of the process
    end_message = f"{processing_step} completed ({elapsed_minutes} minutes)"
    logger.info(end_message)


def _initialize_logger() -> logging.Logger:
    """
    Initialize a logger to log details of the execution of the current step.

    Returns
    -------
        Logger object.
    """
    # Set up directory for log files if it does not already exist
    config.LOGGING_DIR.mkdir(mode=0o777, exist_ok=True)

    log_file = config.LOG_FILE
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    # Avoid getting log messages for every file the entry iterator processes
    logging.getLogger("lex.entryiterator").setLevel(logging.WARNING)

    # Create handlers (one for the log file, the other for the terminal)
    stream_handler = logging.StreamHandler()

    # limit the log file to 1Mb (older copies get rotated out)
    file_handler = logging.handlers.RotatingFileHandler(
        log_file,
        maxBytes=1000000,
        backupCount=5,
    )

    # create formatter and add it to the handlers
    formatter = logging.Formatter(
        fmt="%(asctime)s | %(name)s %(levelname)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M",
    )
    stream_handler.setFormatter(formatter)
    file_handler.setFormatter(formatter)

    # add the handlers to the logger
    logger.addHandler(stream_handler)
    logger.addHandler(file_handler)
    return logger


if __name__ == "__main__":
    sys.exit(run_process())
