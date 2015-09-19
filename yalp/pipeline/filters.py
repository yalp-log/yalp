# vim: set et ts=4 sw=4 fileencoding=utf-8:
'''
yalp.pipeline.filters
=====================
'''


def _event_has_field(fields, event):
    ''' Check if all fields are in event '''
    for field in fields:
        if field not in event:
            return False
    return True


def _event_not_has_field(fields, event):
    ''' Check if event does not have field '''
    for field in fields:
        if field in event:
            return False
    return True


def _event_has_any_field(fields, event):
    ''' Check if any field is in event '''
    for field in fields:
        if field in event:
            return True
    return False


def _field_equals(filters, event):
    ''' Check if field euqals value '''
    for filter_ in filters:
        field = filter_[0]
        match = filter_[1]
        if field not in event:
            return False
        if event[field] != match:
            return False
    return True


def _field_contains(filters, event):
    ''' Check if field is in event and contains value '''
    for filter_ in filters:
        field = filter_[0]
        match = filter_[1]
        if field not in event:
            return False
        if match not in event[field]:
            return False
    return True


FILTER_MAP = {
    'has_fields': _event_has_field,
    'not_has_fields': _event_not_has_field,
    'has_any_field': _event_has_any_field,
    'field_contains': _field_contains,
    'field_equals': _field_equals,
}
