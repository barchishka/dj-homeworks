from django.shortcuts import render

from .models import Student, Teacher


def students_list(request):
    template = 'school/students_list.html'

    teacher_objects = Teacher.objects.all()
    list({'name': t.name, 'subject': t.subject}
         for t in teacher_objects)

    student_objects = Student.objects.all()
    students = list({'name': st.name, 'teachers': Teacher.objects, 'group': st.group}
                    for st in student_objects)
    context = {'object_list': students}

    # используйте этот параметр для упорядочивания результатов
    # https://docs.djangoproject.com/en/2.2/ref/models/querysets/#django.db.models.query.QuerySet.order_by
    'group'

    return render(request, template, context)
