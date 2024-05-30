def _build_sort_criteria(entity_type, sort_by: str):
    """EXAMPLE sort_by string: sort_by = \"created_on DESC, username\" """
    sort_criteria = []
    if sort_by:
        for column_sort in sort_by.split(","):
            column, *direction = column_sort.strip().split()
            if direction and direction[0].upper() == "DESC":
                sort_criteria.append(getattr(entity_type, column).desc())
            else:
                sort_criteria.append(getattr(entity_type, column))
    return sort_criteria


def _add_sort_criteria_to_query(query, sort_criteria):
    for criterion in sort_criteria:
        query = query.order_by(criterion)
    return query


def _apply_sorting_criteria(query, entity_type, sort_by: str):
    return _add_sort_criteria_to_query(
        query, _build_sort_criteria(entity_type, sort_by)
    )


def _apply_paging(query, page_index: int, page_size: int):
    return query.offset(page_index * page_size).limit(page_size)


def apply_sorting_and_paging_to_list_query(
    query, entity_type, page_index: int = 0, page_size: int = 10, sort_by: str = None
):
    """entity_type: This is the class reference
    to the entity that extends DeclarativeBase"""

    return _apply_paging(
        _apply_sorting_criteria(query, entity_type, sort_by), page_index, page_size
    )
