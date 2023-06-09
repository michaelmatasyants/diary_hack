from random import choice
from datacenter.models import *


WORDS_OF_PRAISE = [
    "Молодец!", "Отлично!", "Хорошо!", "Гораздо лучше, чем я ожидал!",
    "Ты меня приятно удивил!", "Великолепно!", "Прекрасно!",
    "Ты меня очень обрадовал!", "Именно этого я давно ждал от тебя!",
    "Сказано здорово – просто и ясно!", "Ты, как всегда, точен!",
    "Очень хороший ответ!", "Талантливо!", "Ты сегодня прыгнул выше головы!",
    "Я тобой горжусь!", "С каждым разом у тебя получается всё лучше!",
    "Мы с тобой не зря поработали!", "Я вижу, как ты стараешься!",
    "Ты растешь над собой!", "Ты многое сделал, я это вижу!",
    "Теперь у тебя точно все получится!"
]


def fix_marks(schoolkid: Schoolkid):
    '''Corrects grades by replacing all bad grades (2s and 3s)
    with 5s for the specified student'''
    Mark.objects.filter(schoolkid=schoolkid, points__in=[2, 3]).update(
        points=5)


def remove_chastisements(schoolkid: Schoolkid):
    '''Removes all chastisements for the specified schoolkid'''
    Chastisement.objects.filter(schoolkid=schoolkid).delete()


def create_commendations(subject_names: list, schoolkid: Schoolkid):
    '''Finds the last lesson in a given subject for a specified student
    and creates a praise, randomly selected from a list of praises'''
    all_subjects = Subject.objects.filter(year_of_study=schoolkid.year_of_study)
    subjects_queryset = []
    for subject_name in subject_names:
        for subject in all_subjects:
            if subject_name in subject.title:
                subjects_queryset.append(subject)
                continue
    if not subjects_queryset:
        return print('There are no such subjectss.')
    for subject in subjects_queryset:
        random_praise = choice(WORDS_OF_PRAISE)
        last_lesson = Lesson.objects.select_related('teacher').filter(
            group_letter=schoolkid.group_letter,
            year_of_study=schoolkid.year_of_study,
            subject__title=subject.title).order_by('-date').first()
        Commendation.objects.create(text=random_praise,
                                    created=last_lesson.date,
                                    schoolkid=schoolkid,
                                    subject=subject,
                                    teacher=last_lesson.teacher)


def main():
    '''Fixes all marks, removes chastisements and creates commendations
    for given subjects for specified child'''
    while True:
        try:
            child = Schoolkid.objects.get(
                full_name__icontains=input('Введите ФИО ученика: '))
            break
        except Schoolkid.DoesNotExist:
            print("Ученика с подобным ФИО не существует.",
                  "Попробуйте указать полное имя ученика в следующем формате:",
                  "Фамилия Имя Отчество.", sep='\n', end='\n\n')
        except Schoolkid.MultipleObjectsReturned:
            print("По введеному Вами полю было найдено несколько учеников.",
                  "Попробуйте указать полное имя ученика в следующем формате:",
                  "Фамилия Имя Отчество.", sep='\n', end='\n\n')
    fix_marks(child)
    print("Все двойки и тройки были успешно заменены на пятерки.")
    remove_chastisements(child)
    print("Все замечания от учителей были успешно удалены.")
    subject_names = [
        'Краеведение', 'География', 'Математика', 'Музыка', 'Физкультура',
        'Изобразительное искусство', 'Технология', 'Русский язык',
        'Литература', 'Обществознание', 'Иностранный язык', 'Биология',
        'История', 'ОБЖ'
    ]
    create_commendations(subject_names=subject_names, schoolkid=child)
    print("За последний урок по каждому из предметов была добавлена похвала",
          "от учителя.")


if __name__ == '__main__':
    main()
