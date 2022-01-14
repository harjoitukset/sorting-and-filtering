from helsinki_api import get_events, get_name, filter_events_by_days, student_answer


def test_output_contains_all_events_in_range(student_answer):
    events = get_events()
    included_events = filter_events_by_days(events, 1, 29)

    for event in included_events:
        assert get_name(event) in student_answer


def test_output_does_not_contain_events_beyond_30_days(student_answer):
    events = get_events()

    # ignore current and day 30 to prevent timing errors
    included_events = filter_events_by_days(events, 1, 29)

    excluded_events = filter_events_by_days(
        events, -1_000, -1) + filter_events_by_days(events, 31, 1_000)

    # The same name or a part of it can appear in both allowed and
    # disallowed names. Therefore make a whitelist string of allowed event names:
    allowed_output = " ".join([get_name(event) for event in included_events])

    for event in excluded_events:
        name = get_name(event)
        if name not in allowed_output:
            assert get_name(event) not in student_answer
