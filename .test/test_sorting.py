from helsinki_api import get_events, get_name, filter_events_by_days, student_answer, sort_chronologically


def test_events_are_in_chronological_order(student_answer: str):
    events = get_events()

    # exclude current and day 30 to prevent timing errors
    events = filter_events_by_days(events, 1, 29)
    events = sort_chronologically(events)

    output_index = 0
    for event in events:
        name = get_name(event)
        try:
            # make sure that the name can be found after the previous event name, and update the index
            output_index = student_answer.index(name, output_index + 1)
        except ValueError:
            raise Exception(
                f'Event {name} was not found in the correct position!')
