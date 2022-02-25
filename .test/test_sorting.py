from pathlib import Path
from pytest import fixture
from helsinki_api import (filter_events_by_days, get_events, get_name,
                          sort_chronologically)


@fixture
def student_answer():
    return (Path(__file__).parent.parent / 'student_output.txt').resolve().read_text(encoding='utf-8')


def test_events_are_in_chronological_order(student_answer: str):
    events = get_events()

    # exclude current and day 30 to prevent timing errors
    events = filter_events_by_days(events, 1, 29)
    events = sort_chronologically(events)

    output_index = 0
    for i, event in enumerate(events):
        name = get_name(event)

        # make sure that the name can be found after the previous event name, and update the index
        output_index = student_answer.find(name, output_index + 1)

        if output_index == -1:
            prev_name = get_name(events[i-1]) if i >= 1 else '[start]'
            next_name = get_name(
                events[i+1]) if i < len(events) - 1 else '[end]'
            raise Exception(
                f'Event "{name}" was not found in the correct position between "{prev_name}" and "{next_name}"!')
