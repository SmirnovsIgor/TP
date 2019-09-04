from django.core.management.base import BaseCommand, CommandError

from apps.users.models import User, Organization
from apps.locations.models import Address, Place
from apps.events.models import Event


class Command(BaseCommand):
    help = 'Populate the event entity'

    def add_arguments(self, parser):
        parser.add_argument('event_ids', nargs='+', type=str)

    def handle(self, *args, **options):
        for event_id in options['event_ids']:
            try:
                event = Event.objects.get(pk=event_id)
            except Event.DoesNotExist:
                raise CommandError('Poll "%s" does not exist' % event_id)

            event.opened = False
            event.save()

            self.stdout.write(self.style.SUCCESS('Successfully closed poll "%s"' % event_id))
