from django.db import models


class Entity(models.Model):
    # user_id = models.ForeignKey('users.user',
    #                             on_delete=models.SET_NULL,
    #                             related_name='user_id', null=True)
    user_id = models.IntegerField(default=1)
    duration = models.IntegerField()
    date = models.DateField()
    distance = models.IntegerField()

    @property
    def speed(self):
        try:
            return round(self.distance / self.duration, 2)
        except Exception as e:
            return -1

    @property
    def week_number(self):
        try:
            return self.date.isocalendar()[1]
        except Exception as e:
            return -1
