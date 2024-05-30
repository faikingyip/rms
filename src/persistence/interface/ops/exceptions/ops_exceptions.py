from typing import Optional


class PersistenceOpsBaseError(Exception):
    def __init__(self, original_exception: Optional[Exception] = None):
        super().__init__(str(original_exception))
