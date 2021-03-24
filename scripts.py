from random import choice

from django.core.exceptions import MultipleObjectsReturned, ObjectDoesNotExist

from datacenter.models import Chastisement, Commendation, Lesson, \
    Mark, Schoolkid, Subject


commendations = ['Молодец!',
                 'Отлично!',
                 'Хорошо!',
                 'Гораздо лучше, чем я ожидал!',
                 'Приятно удивил!',
                 'Хвалю',
                 'Великолепно!',
                 'Прекрасно!',
                 'Очень обрадовал!',
                 'Сказано здорово – просто и ясно!',
                 'Как всегда, точен!',
                 'Очень хороший ответ!',
                 'Талантливо!',
                 ]


def get_schoolkid_by_name(name):
    """Gets schoolkid by name. If finds only one, returns it.
    If doesn't find, return None.

    :param name: name of schoolkid to search
    """

    if not name:
        print("Не указано имя. Исправьте.")
        return

    try:
        schoolkid = Schoolkid.objects.get(full_name__contains=name)
    except ObjectDoesNotExist:
        print("Не нахожу учеников с таким именем. Попробуйте другое имя.")
        return
    except MultipleObjectsReturned:
        print("Слишком много школьников с таким именем. Уточните имя.")
        return

    return schoolkid


def fix_marks(schoolkid):
    """Fix bad notes in journal.

    :param schoolkid: schoolkid which notes we are fixing.
    """

    bad_marks = Mark.objects.filter(schoolkid=schoolkid, points__in=[2, 3])
    for bad_mark in bad_marks:
        bad_mark.points = 5
        bad_mark.save()


def remove_chastisements(schoolkid):
    """Remove all chastisements.

    :param schoolkid: schoolkid which chastisements we are deleting.
    """

    chastisements = Chastisement.objects.filter(schoolkid=schoolkid)
    chastisements.delete()


def create_commendation(schoolkid, subject_title):
    """Creates commendations for schoolkid.

    :param schoolkid: schoolkid to give commendations
    :param subject_title: title of subject
    """

    try:
        subject = Subject.objects.get(title=subject_title.title(),
                                      year_of_study=schoolkid.year_of_study)
    except ObjectDoesNotExist:
        print("Не нахожу предмета с таким названием для этого ученика. "
              "Проверьте написание.")
        return

    last_lesson = Lesson.objects.filter(year_of_study=schoolkid.year_of_study,
                                        group_letter=schoolkid.group_letter,
                                        subject=subject).last()

    Commendation.objects.create(text=choice(commendations),
                                created=last_lesson.date,
                                schoolkid=schoolkid,
                                subject=subject,
                                teacher=last_lesson.teacher)
