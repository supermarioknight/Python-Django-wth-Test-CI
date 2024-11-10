from django.db import models

class Teacher(models.Model):
    """
    Teacher Model
    
    Attributes:
        name (str): The name of the teacher
    """
    name = models.CharField(max_length=100)
    
    def __str__(self):
        """
        String representation of the Teacher model
        
        Returns:
            str: The name of the teacher
        """
        return self.name
    
class Subject(models.Model):
    """
    Model representing a subject taught by a teacher
    
    Attributes:
        name (str): The name of the subject
        teacher (Teacher): The teacher who teaches this subject
    """
    name = models.CharField(max_length=100)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, related_name='subjects')
    
    def __str__(self):
        """
        String representation of the subject
        
        Returns:
            str: The name of the subject
        """
        return self.name
    
class Class(models.Model):
    """
    Model representing a class of students
    
    Attributes:
        name (str): The name of the class
    """
    name = models.CharField(max_length=10)
    
    def __str__(self):
        """
        String representation of the Class model
        
        Returns:
            str: The name of the class
        """
        return self.name
    
class Student(models.Model):
    """
    Model representing a student in a class.

    Attributes:
        name (str): The name of the student.
        class_assigned (Class): The class to which the student is assigned.
    """
    name = models.CharField(max_length=100)
    class_assigned = models.ForeignKey(Class, on_delete=models.CASCADE, related_name='students')

    def __str__(self):
        """
        String representation of the Student model.

        Returns:
            str: The name of the student.
        """
        return self.name
    
class Schedule (models.Model):
    """
    Model representing a schedule of classes.
    
    Attributes:
        class_assigned (Class): The class for which the schedule is.
        subject (Subject): The subject being taught.
        day_of_week (int): The day of the week (0=Mon, ..., 6=Sun).
        hour (Time): The hour of the lesson.
    """
    DAYS_OF_WEEK = [
        (0, 'Monday'),
        (1, 'Tuesday'),
        (2, 'Wednesday'),
        (3, 'Thursday'),
        (4, 'Friday'),
        (5, 'Saturday'),
        (6, 'Sunday'),
    ]
    
    class_assigned = models.ForeignKey(Class, on_delete=models.CASCADE, related_name='schedules')
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='schedules')
    day_of_week = models.IntegerField(choices=DAYS_OF_WEEK)
    hour = models.TimeField()
    
    class Meta:
        """
        Meta options for Schedule model.        
        """
        unique_together = ('class_assigned', 'day_of_week', 'hour')
        ordering = ['day_of_week', 'hour']
        indexes = [
            models.Index(fields=['day_of_week', 'class_assigned']),
        ]
        
    def __str__(self):
        """
        String representation of the Schedule model.
        
        Returns:
            str: The name of the schedule with class, subject, day, hour
        """
        day = self.get_day_of_week_display()
        return f"{self.class_assigned.name} - {self.subject.name} on {day} at {self.hour}"
 