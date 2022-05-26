import os
import logging
from typing import Any, Callable

from Services.common.custom_errors import ValueNotSetError

logger = logging.getLogger(__name__)


def get(var_name: str, required: bool = True) -> Any:
    _get: Callable[[str], Any] = os.environ.get
    value = _get(var_name)
    if value or not required:
        return value
    else:
        logger.error(f"Value for variables {var_name} not set in system")
        raise ValueNotSetError(f"Value for variables {var_name} not set in system")
