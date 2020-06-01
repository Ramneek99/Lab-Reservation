from django.db import models
from django.urls import reverse

Labs = [('nab0101','NAB 0101'),
        ('nab0103','NAB 0103'),
        ('nab0104', 'NAB 0104'),
        ('nab0105', 'NAB 0105'),
        ('nab0106', 'NAB 0106'),
        ('nab0109', 'NAB 0109'),
        ('nab0111', 'NAB 0111'),
        ('nab0113', 'NAB 0113'),
        ('nab0117', 'NAB 0117'),
        ('nab3104', 'NAB 3104'),
        ('studn3326', 'STUDN 3326'),]

class Event(models.Model):
    my_id = models.AutoField(primary_key = True)
    title = models.CharField(max_length=100)
    room_number = models.CharField(max_length=10, choices=Labs, default='nab0101')
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # self.id = None

    @property
    def get_html_url(self):
         url = reverse('cal:event_edit', args=(self.id,))
        # return f'<a href="{url}"> {self.title} </a>'

    def __str__(self):
        return 'my_id: {}\ntitle: {}\nroom_number: {}\nstart_time: {}\nend_time: {}'.format(
            self.my_id, self.title, self.room_number, self.start_time, self.end_time)
