from random import choice

from datacenter.models import Chastisement, Schoolkid, Mark, Commendation, Lesson, Subject


commendations = ['Молодец!', 'Отлично!', 'Хорошо!', 'Гораздо лучше, чем я ожидал!', 'Приятно удивил!', 'Хвалю',
                 'Великолепно!', 'Прекрасно!', 'Очень обрадовал!', 'Сказано здорово – просто и ясно!',
                 'Как всегда, точен!', 'Очень хороший ответ!', 'Талантливо!']


def get_schoolkid_by_name(name):
    """Gets schoolkid by name. If finds only one, returns it. If doesn't find, return None.

    :param name: name of schoolkid to search
    """

    if not name:
        print("Не указано имя. Исправьте.")
        return

    all_schollkids_with_name = Schoolkid.objects.filter(full_name__contains=name)
    if len(all_schollkids_with_name) > 1:
        print("Слишком много школьников с таким именем. Уточните имя.")
        return
    if not all_schollkids_with_name:
        print("Не нахожу учеников с таким именем. Попробуйте другое имя.")
        return

    return all_schollkids_with_name.first()


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

    subject = Subject.objects.get(title=subject_title, year_of_study=schoolkid.year_of_study, group_letter=schoolkid.group_letter)
    if not subject:
        print("Не нахожу предмета с таким названием для этого ученика. Проверьте написание.")
    last_lesson = Lesson.objects.filter(year_of_study=schoolkid.year_of_study, group_letter=schoolkid.group_letter,
                                        subject=subject).last()
    Commendation.objects.create(text=choice(commendations), created=last_lesson.date, schoolkid=schoolkid,
                                subject=subject, teacher=last_lesson.teacher)
