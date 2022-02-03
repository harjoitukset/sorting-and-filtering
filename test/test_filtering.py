from helsinki_api import get_events, get_name, filter_events_by_days, get_start_time, student_answer


def test_output_contains_all_events_in_range(student_answer):
    events = get_events()

    # ignore current and day 30 to prevent timing errors
    included_events = filter_events_by_days(events, 1, 29)

    for event in included_events:
        name = get_name(event)
        start_time = get_start_time(event)

        assert name in student_answer, f'Event "{name}" on {start_time} should be included in output.'


def test_output_does_not_contain_events_beyond_30_days(student_answer):
    events = get_events()

    # Allow events that are just a bit over the limits
    allowed_events = filter_events_by_days(events, -1, 31)

    # These events before current day and after a month must be excluded
    excluded_events = filter_events_by_days(
        events, -1_000, -2) + filter_events_by_days(events, 32, 1_000)

    # The same name or a part of it can appear in both allowed and
    # disallowed names if the event is recurring or otherwise generic.
    # Therefore make a whitelist string of allowed event names:
    whitelist = ' '.join([get_name(event) for event in allowed_events])

    for event in excluded_events:
        name = get_name(event)
        if name not in whitelist:
            assert name not in student_answer, f'Event "{name}" should be excluded from output.'
