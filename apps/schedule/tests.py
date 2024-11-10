from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from django.utils import timezone

from .models import Class, Teacher, Subject, Schedule, Student

class TeacherModelTest(APITestCase):
    """
    Test case for the Teacher model.
    """

    def test_string_representation(self):
        """
        Test the string representation of the Teacher model.
        """
        teacher = Teacher(name='Alex')
        self.assertEqual(str(teacher), 'Alex')


class SubjectModelTest(APITestCase):
    """
    Test case for the Subject model.
    """

    def setUp(self):
        """
        Set up test data for Subject model tests.
        """
        self.teacher = Teacher.objects.create(name='Alex')

    def test_string_representation(self):
        """
        Test the string representation of the Subject model.
        """
        subject = Subject(name='Math', teacher=self.teacher)
        self.assertEqual(str(subject), 'Math')


class ClassModelTest(APITestCase):
    """
    Test case for the Class model.
    """

    def test_string_representation(self):
        """
        Test the string representation of the Class model.
        """
        class_obj = Class(name='5A')
        self.assertEqual(str(class_obj), '5A')


class StudentModelTest(APITestCase):
    """
    Test case for the Student model.
    """

    def setUp(self):
        """
        Set up test data for Student model tests.
        """
        self.class_obj = Class.objects.create(name='5A')

    def test_string_representation(self):
        """
        Test the string representation of the Student model.
        """
        student = Student(name='John Doe', class_assigned=self.class_obj)
        self.assertEqual(str(student), 'John Doe')


class ScheduleModelTest(APITestCase):
    """
    Test case for the Schedule model.
    """

    def setUp(self):
        """
        Set up test data for Schedule model tests.
        """
        self.teacher = Teacher.objects.create(name='Alex')
        self.subject = Subject.objects.create(name='Math', teacher=self.teacher)
        self.class_obj = Class.objects.create(name='5A')
        self.schedule = Schedule.objects.create(
            class_assigned=self.class_obj,
            subject=self.subject,
            day_of_week=0,
            hour='09:00:00',
        )

    def test_string_representation(self):
        """
        Test the string representation of the Schedule model.
        """
        self.assertEqual(
            str(self.schedule),
            '5A - Math on Monday at 09:00:00'
        )

    def test_unique_constraint(self):
        """
        Test the unique constraint on Schedule model.
        """
        with self.assertRaises(Exception):
            Schedule.objects.create(
                class_assigned=self.class_obj,
                subject=self.subject,
                day_of_week=0,
                hour='09:00:00',
            )


class ScheduleAPITestCase(APITestCase):
    """
    Test case for the Schedule API.

    This class contains tests for retrieving all schedules and schedules filtered by parameters.
    """

    def setUp(self):
        """
        Set up test data for the test case.

        Creates instances of Teacher, Subject, Class, Student, and Schedule models.
        """
        # Create a teacher
        self.teacher1 = Teacher.objects.create(name='Alex')
        self.teacher2 = Teacher.objects.create(name='John')

        # Create subjects
        self.subject_math = Subject.objects.create(name='Math', teacher=self.teacher1)
        self.subject_en = Subject.objects.create(name='English', teacher=self.teacher2)

        # Create a class
        self.class_5A = Class.objects.create(name='5A')
        self.class_5B = Class.objects.create(name='5B')

        # Create students
        Student.objects.create(name='Student1', class_assigned=self.class_5A)
        Student.objects.create(name='Student2', class_assigned=self.class_5A)
        Student.objects.create(name='Student3', class_assigned=self.class_5B)

        # Create schedules
        self.today_weekday = timezone.now().weekday()
        Schedule.objects.create(
            class_assigned=self.class_5A,
            subject=self.subject_math,
            day_of_week=self.today_weekday,
            hour='09:00:00',
        )
        Schedule.objects.create(
            class_assigned=self.class_5A,
            subject=self.subject_en,
            day_of_week=(self.today_weekday + 1) % 7,
            hour='10:00:00',
        )
        Schedule.objects.create(
            class_assigned=self.class_5B,
            subject=self.subject_math,
            day_of_week=(self.today_weekday + 1) % 7,
            hour='10:00:00',
        )

    def test_get_all_schedules(self):
        """
        Test retrieving all schedules.

        Ensures that the API returns a list of schedules without any filters.
        """
        url = reverse('schedule-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 3)
        
    def test_get_schedule_for_today_only(self):
        """
        Test retrieving schedules filtered by today's date only.

        Ensures that the API returns all schedules for the current day regardless of class.
        """
        url = reverse('schedule-list')
        response = self.client.get(url, {'for_today': 'true'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()
        self.assertEqual(data['count'], 1)  # Only one schedule matches today's date
        schedule = data['results'][0]
        self.assertEqual(schedule['class_assigned']['name'], '5A')
        self.assertEqual(schedule['subject']['name'], 'Math')
        
    def test_get_schedule_by_class_name_only(self):
        """
        Test retrieving schedules filtered by class name only.

        Ensures that the API returns all schedules for the specified class without filtering by day.
        """
        url = reverse('schedule-list')
        response = self.client.get(url, {'class_name': '5B'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()
        self.assertEqual(data['count'], 1)  # Schedules for class 5B only
        for schedule in data['results']:
            self.assertEqual(schedule['class_assigned']['name'], '5B')

    def test_get_class_schedule_for_today(self):
        """
        Test retrieving class schedule for today.

        Ensures that the API returns schedules for the specified class and current day.
        """
        url = reverse('schedule-list')
        response = self.client.get(url, {'for_today': 'true', 'class_name': '5A'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()
        self.assertEqual(data['count'], 1)
        schedule = data['results'][0]
        self.assertEqual(schedule['class_assigned']['name'], '5A')
        self.assertEqual(schedule['subject']['name'], 'Math')

    def test_get_schedule_with_invalid_filter_values(self):
        """
        Test retrieving schedules with invalid filter values.

        Ensures that the API handles invalid filter values and returns an empty list or default result.
        """
        url = reverse('schedule-list')

        # Invalid 'for_today' value
        response = self.client.get(url, {'for_today': 'invalid'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()
        self.assertEqual(data['count'], 3)  # Ignore 'for_today' if invalid and return all

        # Invalid class name
        response = self.client.get(url, {'class_name': 'NaN'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()
        self.assertEqual(data['count'], 0)  # No schedules match NaN class_name

        # Both invalid 'for_today' and class name
        response = self.client.get(url, {'for_today': 'invalid', 'class_name': 'NonExistentClass'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()
        self.assertEqual(data['count'], 0)  # No schedules match invalid for_today and class_name
        
class ScheduleOrderingTest(APITestCase):
    """
    Test case to verify that schedules are ordered by day_of_week and hour.
    """

    def setUp(self):
        """
        Set up test data for ordering tests.
        """
        teacher = Teacher.objects.create(name='Alex')
        subject = Subject.objects.create(name='Math', teacher=teacher)
        class_obj = Class.objects.create(name='5A')

        # Create schedules out of order
        Schedule.objects.create(
            class_assigned=class_obj,
            subject=subject,
            day_of_week=1,
            hour='10:00',
        )
        Schedule.objects.create(
            class_assigned=class_obj,
            subject=subject,
            day_of_week=0,
            hour='09:00',
        )
        Schedule.objects.create(
            class_assigned=class_obj,
            subject=subject,
            day_of_week=0,
            hour='08:00',
        )

    def test_schedule_ordering(self):
        """
        Test that schedules are returned in the correct order.
        """
        url = reverse('schedule-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        data = response.json()

        # Extract day_of_week and hour from response data
        schedule_list = data['results']
        days_hours = [(item['day_of_week'], item['hour']) for item in schedule_list]

        # Expected order
        expected_order = [
            ('Monday', '08:00:00'),
            ('Monday', '09:00:00'),
            ('Tuesday', '10:00:00'),
        ]

        self.assertEqual(days_hours, expected_order)
