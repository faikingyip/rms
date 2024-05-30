from typing import Callable

from src.persistence.interface.ops.exceptions.ops_exceptions import (
    PersistenceOpsBaseError,
)


async def affect_existing_row(
    affect_existing_row_func: Callable[..., int],
    error_to_raise: Callable[[Exception], Exception],
    **kwargs: any
):
    """
    Generic function for calling persistent operations that affect only 1 row,
    i.e. deleting or updating a record.
    The persistent function specified as the argument affect_existing_row_func
    needs to report the number of rows affected. This function will assess
    the rowcount and raise the specified error if anything by 1 row was affected.

    kwargs represents any additional parameters that should be provided
    to the implementation of affect_existing_row_func.
    """
    try:
        rowcount = await affect_existing_row_func(**kwargs)
        if rowcount > 1:
            raise PersistenceOpsBaseError("More than 1 row was affected.")
        if rowcount < 1:
            raise PersistenceOpsBaseError("No rows were affected.")
    except PersistenceOpsBaseError as poe:
        raise error_to_raise(poe) from poe


async def get_data_list(
    page_index: int,
    page_size: int,
    sort_by: str,
    select_data_list_func: Callable[..., list],
    error_to_raise: Callable[[Exception], Exception],
    **kwargs: any
):
    """
    Generic function that performs standard checks
    on input paging data provided to a search query list function.

    The implementation of select_data_list_func must take as input
    the following parameters:

        page_index: int,
        page_size: int,
        sort_by: str,

    Use error_to_raise to specify an error that is related to the
    implementation of select_data_list_func.

    kwargs represents any additional parameters that should be provided
    to the implementation of select_data_list_func.
    """

    if page_index < 0:
        raise error_to_raise(ValueError("Invalid page index."))

    if page_size < 1:
        raise error_to_raise(ValueError("Invalid page size."))

    func_kwargs = kwargs.copy()
    func_kwargs.update(
        {"page_index": page_index, "page_size": page_size, "sort_by": sort_by}
    )

    try:
        return await select_data_list_func(**func_kwargs)

    except PersistenceOpsBaseError as poe:
        raise error_to_raise(poe) from poe
