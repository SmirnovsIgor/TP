#! /bin/bash

pytest -vv --ds=TicketProer.settings apps/users/tests apps/locations/tests apps/events
