from django.db import models
from django.contrib.auth.models import User
from django_countries.fields import CountryField


class Employee(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    slack_user = models.CharField(max_length=20, unique=True)
    country = CountryField()

    def __str__(self):
        return '%s %s' % (self.user.first_name, self.user.last_name)


class Meal(models.Model):

    name = models.CharField(max_length=60, null=False)

    def __str__(self):
        return self.name


class Menu(models.Model):

    STATE_OPEN = 'open'
    STATE_CLOSED = 'closed'
    STATES = (
        (STATE_OPEN, 'Open'),
        (STATE_CLOSED, 'Closed'),
    )

    date = models.DateField(blank=False)
    state = models.CharField(max_length=20, choices=STATES, default=STATE_OPEN)
    meals = models.ManyToManyField(Meal)
    published = models.BooleanField(default=False)
    country = CountryField()

    def close(self):
        if self.state != Menu.STATE_OPEN:
            return self, False

        self.state = Menu.STATE_CLOSED
        self.save()

        return self, True

    def to_published(self):
        if self.published:
            return self, False

        self.published = True
        self.save()
        return self, True

    def can_publish(self):
        if self.state == Menu.STATE_CLOSED or self.published:
            return False
        return True


class Order(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    menu = models.ForeignKey(Menu, on_delete=models.CASCADE)
    meal = models.ForeignKey(Meal, on_delete=models.CASCADE)
    customization = models.TextField(blank=True)
    # rate = models.IntegerField(choices=list(zip(range(1, 6), range(1, 6))))
    created = models.DateTimeField(auto_now_add=True, null=True)
