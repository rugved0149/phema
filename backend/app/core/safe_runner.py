# app/core/safe_runner.py

import logging


def run_safe(module_name, func, *args, **kwargs):
    """
    Execute module safely so one failure does not crash the pipeline.
    """

    try:
        return func(*args, **kwargs)

    except Exception as e:

        logging.error(
            f"[MODULE FAILURE] {module_name}: {str(e)}"
        )

        return None