from voluptuous import Schema


CONTACT_LIST_SCHEMA = Schema(
    {'listId': int, 'name': str, 'dynamic': bool},
    required=True,
    extra=True,
    )


CONTACT_LIST_MEMBERSHIP_UPDATE_SCHEMA = \
    Schema({'updated': list}, required=True, extra=True)
