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

    poor_grades = Mark.objects.filter(schoolkid=schoolkid, points__in=[2, 3])
    for poor_grade in poor_grades:
        poor_grade.points = 5
        poor_grade.save()


def remove_chastisements(schoolkid: Schoolkid):
    '''Removes all chastisements for the specified schoolkid'''
    Chastisement.objects.filter(schoolkid=schoolkid).delete()


def create_commendation(subject_name: str, schoolkid: Schoolkid):
    '''Finds the last lesson in a given subject for a specified student
    and creates a praise, randomly selected from a list of praises'''

    subject = Subject.objects.filter(title__icontains=subject_name,
                                     year_of_study=schoolkid.year_of_study
                                     ).first()
    random_praise = choice(WORDS_OF_PRAISE)
    last_lesson = Lesson.objects.filter(
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
            child = Schoolkid.objects.get(full_name__icontains=input(
                'Введите "Фамилию Имя Отчество" ученика: '))
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
    for subject_name in subject_names:
        create_commendation(subject_name=subject_name, schoolkid=child)
    print("За последний урок по каждому из предметов была добавлена похвала",
          "от учителя.")


if __name__ == '__main__':
    main()
