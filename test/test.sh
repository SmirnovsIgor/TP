#! /bin/bash

pytest -vv --ds=TicketProer.settings apps/events/tests/test_events.py::TestEventsCreate
