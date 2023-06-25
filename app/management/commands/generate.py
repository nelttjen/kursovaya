import random

from django.core.management.base import BaseCommand

from app.models import *


class Command(BaseCommand):
    def handle(self, *args, **options):
        added_groups = []
        lessons_settings = {}

        day_keys = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday']

        generated_schedule = {}
        for key in day_keys:
            generated_schedule[key] = {}

        groups = Group.objects.prefetch_related('lessons').all()

        for group in groups:
            while True:
                is_add = input(f'Добавить группу {group.name} в генератор? ("+" / "-"): ')
                if is_add in ('+', '-'):
                    break
                print('Должно быть + или -')
            if is_add == '-':
                continue

            lessons = list(group.lessons.exclude(teacher_id__isnull=True, cabinet_id__isnull=True))

            if len(lessons) == 0:
                print(f'У группы {group.name} нет предметов, скип')
                continue

            setattr(group, 'lessons_list', lessons)

            added_groups.append(group)
            lessons_settings[group.id] = {}

            for lesson in lessons:
                while True:
                    count = input(f'Сколько {lesson.name} в неделю? (число больше нуля): ')
                    if not count.isdigit():
                        print('Должно быть числом')
                        continue
                    if (count := int(count)) <= 0:
                        print('Должно быть больше нуля')
                        continue
                    lessons_settings[group.id][lesson.id] = count
                    break

        name = input('Название рассписания: ')

        # generator
        for group in added_groups:
            for key in day_keys:
                generated_schedule[key][group.name] = {}

            for lesson in group.lessons_list:
                this_count = lessons_settings[group.id][lesson.id]

                days = day_keys.copy()
                random.shuffle(days)

                while days:
                    this_day = days.pop()

                    indexes = [1, 2, 3, 4]
                    indexes.reverse()
                    if this_count == 0:
                        break

                    while indexes:
                        index = indexes.pop()

                        if index in generated_schedule[this_day][group.name].keys():
                            continue

                        available = True

                        for key_group in generated_schedule[this_day].keys():
                            if key_group == group.name:
                                continue
                            other_group_day = generated_schedule[this_day][key_group]
                            if index not in other_group_day.keys():
                                continue
                            other_group_lesson = other_group_day[index]
                            if other_group_lesson.cabinet_id == lesson.cabinet_id or other_group_lesson.teacher_id == lesson.teacher_id:
                                available = False
                                break

                        if not available:
                            continue

                        generated_schedule[this_day][group.name][index] = lesson
                        this_count -= 1

                        if this_count == 0:
                            break

                if this_count > 0:
                    raise Exception(f'Невозможно сгенерировать расписание с такими настройками, \n'
                                    f'{lesson.name}: учитель или кабинет заняты')

        for day in day_keys:
            for key_group in generated_schedule[day]:
                for index in generated_schedule[day][key_group].keys():
                    generated_schedule[day][key_group][index] = generated_schedule[day][key_group][index].name

        GeneratedSchedule.objects.create(
            name=name,
            schedule=generated_schedule
        )
        print('Сохранено')