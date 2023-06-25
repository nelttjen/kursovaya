from django.db import models


class Teachers(models.Model):
    first_name = models.CharField(verbose_name='Имя', max_length=128)
    last_name = models.CharField(verbose_name='Фамилия', max_length=128)


class Cabinets(models.Model):
    name = models.CharField(verbose_name='Номер кабинета', max_length=40)


class Lessons(models.Model):
    name = models.CharField(verbose_name='Название', max_length=200)
    teacher = models.ForeignKey(verbose_name='Преподаватель', to='app.Teachers', on_delete=models.SET_NULL, null=True, blank=True)
    cabinet = models.ForeignKey(verbose_name='Кабинет', to='app.Cabinets', on_delete=models.SET_NULL, null=True, blank=True)


class Group(models.Model):
    name = models.CharField(verbose_name='Название группы', max_length=128)
    lessons = models.ManyToManyField(verbose_name='Предметы группы', to='app.Lessons')


class GeneratedSchedule(models.Model):
    name = models.CharField(verbose_name='Навзание', max_length=128)
    created_at = models.DateTimeField(verbose_name='Создано', auto_now_add=True)
    schedule = models.JSONField(verbose_name='Расписание', default={})