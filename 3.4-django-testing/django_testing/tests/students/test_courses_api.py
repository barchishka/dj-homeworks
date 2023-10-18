import pytest
from model_bakery import baker
from students.models import Course, Student
from rest_framework.test import APIClient


@pytest.fixture
def client():
    return APIClient()


@pytest.fixture
def course_factory():
    def factory(*args, **kwargs):
        return baker.make(Course, *args, **kwargs)
    return factory


@pytest.fixture
def student_factory():
    def factory(*args, **kwargs):
        return baker.make(Student, *args, **kwargs)
    return factory


@pytest.mark.django_db
def test_get_cource(client, course_factory):
    # проверка получения первого курса (retrieve-логика)
    # Arrange (создаем курс через фабрику)
    courses = course_factory()
    # Act (строим урл и делаем запрос через тестовый клиент)
    response = client.get(f'/api/v1/courses/{courses.id}/')
    # Assert (проверяем, что вернулся именно тот курс, который запрашивали)
    data = response.json()
    assert response.status_code == 200
    assert courses.name == data['name']


@pytest.mark.django_db
def test_get_cources(client, course_factory):
    # проверка получения списка курсов (list-логика)
    # Arrange
    courses = course_factory(_quantity=5)
    # Act
    response = client.get('/api/v1/courses/')
    # Assert проверяем код возврата, количество и имена всех созданных курсов
    data = response.json()
    # Assert
    assert response.status_code == 200
    assert len(data) == len(courses)
    for i, course in enumerate(data):
        assert course['name'] == courses[i].name


@pytest.mark.django_db
def test_filter_courses_id(client, course_factory):
    # проверка фильтрации списка курсов по id
    # Arrange
    courses = course_factory(_quantity=5)
    # Act
    response = client.get('/api/v1/courses/', data={'id': courses[0].id})
    assert response.status_code == 200
    data = response.json()
    assert data[0]['name'] == courses[0].name


@pytest.mark.django_db
def test_filter_courses_name(client, course_factory):
    # проверка фильтрации списка курсов по name
    courses = course_factory(_quantity=5)

    response = client.get('/api/v1/courses/', data={'name': courses[0].name})

    assert response.status_code == 200
    data = response.json()
    for i, c in enumerate(data):
        assert c['name'] == courses[0].name


@pytest.mark.django_db
def test_creating_course(client):
    # тест успешного создания курса
    student_1 = Student.objects.create(name='student_1', birth_date='2018-05-03')
    student_2 = Student.objects.create(name='student_1', birth_date='2021-08-08')
    response = client.post('/api/v1/courses/', data={
        'name': 'course_1',
        'students': [student_1.id, student_2.id]
    })
    assert response.status_code == 201


@pytest.mark.django_db
def test_course_update(client, course_factory):
    # тест успешного обновления курса
    student = Student.objects.create(name='student_1', birth_date='2019-03-06')
    course = course_factory(_quantity=1)
    response = client.patch(f'/api/v1/courses/{course[0].id}/', data={
        'students': [student.id]
    })
    assert response.status_code == 200
    data = response.json()
    assert data['students'] == [student.id]


@pytest.mark.django_db
def test_delete_course(client, course_factory):
    # тест успешного удаления курса
    course = course_factory(_quantity=2)
    response = client.delete(f'/api/v1/courses/{course[0].id}/')
    assert response.status_code == 204
