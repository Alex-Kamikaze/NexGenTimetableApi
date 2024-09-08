from django.db import models

# Create your models here.
class Group(models.Model):
    """ Учебная группа """

    group_name = models.CharField(max_length=8, verbose_name='Название группы')
    group_course = models.IntegerField(default=1, verbose_name='Номер курса')

    class Meta:
        verbose_name = "Учебная группа"
        verbose_name_plural = "Учебные группы"

    def __str__(self):
        return self.group_name
    
    def as_json(self):
        return dict(group_id = self.pk, group_name = self.group_name, group_course = self.group_course)
    
class Teacher(models.Model):
    teacher_name = models.CharField(max_length=250, verbose_name="ФИО Преподавателя")
    teacher_is_active = models.BooleanField(default=True, verbose_name="Действующий сотрудник") #В случае увольнения - поставить False, и тогда будут внесены изменения в составление замещений для клиентов


    class Meta:
        verbose_name = "Преподаватель"
        verbose_name_plural = "Преподаватели"

    def __str__(self):
        return self.teacher_name
    
    def as_json(self):
        return dict(teacher_id = self.pk, teacher_name = self.teacher_name, teacher_is_active = self.teacher_is_active)
    
class Subject(models.Model):
    """ Учебные дисциплины """
    subject_name = models.CharField(max_length=120, verbose_name="Название дисциплины")
    teacher_id = models.ForeignKey(Teacher, on_delete=models.PROTECT, verbose_name="Преподаватель")

    class Meta:
        verbose_name = "Дисциплина"
        verbose_name_plural = "Дисциплины"

    def __str__(self):
        return self.subject_name
    
    def as_json(self):
        return dict(subject_id = self.pk, subject_name = self.subject_name)



class Timetable(models.Model):
    pair_numbers = (
        ("1", "1"), ("2", "2"), ("3", "3"), ("4", "4")
    )

    days_of_week = (
        ("0", "Понедельник"), ("1", "Вторник"), ("2", "Среда"), ("3", "Четверг"), ("4", "Пятница"), ("5", "Суббота")
    )

    denominator_types = (
        ("n", "Числитель"), ("d", "Знаменатель"), ("b", "Оба")
    )

    day_of_week = models.CharField(max_length=1, choices=days_of_week, verbose_name="День недели", default="0")
    pair_number = models.CharField(max_length=1, choices=pair_numbers, verbose_name="Номер пары")
    subject_id = models.ForeignKey(Subject, on_delete=models.PROTECT, verbose_name="Учебная дисциплина")
    teacher_id = models.ForeignKey(Teacher, on_delete=models.PROTECT, verbose_name="Преподаватель")
    group_id = models.ForeignKey(Group, on_delete=models.CASCADE, verbose_name="Учебная группа")
    distant_pair = models.BooleanField(default=False, verbose_name="Дистанционное занятие")
    cabinet_number = models.CharField(max_length=6, verbose_name="Номер кабинета", blank=True) # Оставлять пустым только в случае, если занятие дистанционное
    pair_begin_time = models.TimeField(verbose_name="Время начала пары")
    pair_end_time = models.TimeField(verbose_name="Время конца пары")
    denominator_options = models.CharField(max_length=1, choices=denominator_types, default="b", verbose_name="Настройка числителя/знаменателя")

    class Meta:
        verbose_name = "Занятие"
        verbose_name_plural = "Занятия"
        ordering = ["pair_number", "day_of_week"]

    def __str__(self):
        return f"{self.pair_number} пара для группы {self.group_id.group_name}"
    
    # TODO: Добавить as_json

    def as_json(self):
        return dict(timetable_id = self.pk, pair_number = self.pair_number, group_id = self.group_id.pk, cabinet_number = self.cabinet_number, teacher_name = self.teacher_id.teacher_name, start_time = f"{self.pair_begin_time.hour}:{self.pair_begin_time.min}", end_time=f"{self.pair_end_time.hour}:{self.pair_end_time.min}")

class Substitution(models.Model):
    date_of_substitution = models.DateField(verbose_name="Дата замещения")
    original_class = models.ForeignKey(Timetable, on_delete=models.CASCADE, verbose_name="Пара для замены")
    subject_on_substitution = models.ForeignKey(Subject, on_delete=models.CASCADE, verbose_name="Предмет для замещения")
    teacher_on_substitution = models.ForeignKey(Teacher, on_delete=models.CASCADE, verbose_name="Преподаватель на замещаемой паре")
    cabinet_on_substitution = models.CharField(max_length=6, blank=True, verbose_name="Кабинет")
    distant_pair = models.BooleanField(default=False, verbose_name="Дистанционное занятие")

    class Meta:
        verbose_name = "Замещение"
        verbose_name_plural = "Замещения"
        ordering = ["-date_of_substitution"]

    def __str__(self):
        return f"Замещение для группы {self.original_class.group_id.group_name} на {self.date_of_substitution.day}.{self.date_of_substitution.month:02}.{self.date_of_substitution.year}"

