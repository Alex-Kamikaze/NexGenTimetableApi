from django.db import models
from timetable.models import Group

# Create your models here.
class CertificateType(models.Model):
    type_name = models.CharField(max_length=100, verbose_name="Название вида справки")

    class Meta:
        verbose_name = "Вид справки"
        verbose_name_plural = "Виды справок"

    def __str__(self):
        return self.type_name

class CertificateRequest(models.Model):
    """ Заказ справки """
    student_fio = models.CharField(max_length=100, verbose_name="ФИО студента")
    student_group = models.ForeignKey(Group, on_delete=models.PROTECT, verbose_name="Группа студента")
    date_of_birth = models.DateField(verbose_name="Дата рождения")
    certificate_type = models.ForeignKey(CertificateType, on_delete=models.PROTECT, verbose_name="Вид справки")
    organization_full_name = models.TextField(verbose_name="Полное название организации", blank=True)
    voenkomat_full_name = models.TextField(verbose_name="Полное название военкомата", blank=True)
    completed = models.BooleanField(verbose_name="Справка выдана", default=False)

    class Meta:
        verbose_name = "Заказ выдачи справки"
        verbose_name_plural = "Заказы выдачи справок"

    def __str__(self):
        return f"Заказ на справку вида {self.certificate_type.type_name} для {self.student_fio}"


