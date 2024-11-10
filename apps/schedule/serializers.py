from rest_framework import serializers
from .models import Teacher, Subject, Class, Student, Schedule

class TeacherSerializer(serializers.ModelSerializer):
    """
    Serializer for Teacher Model.
    """
    
    class Meta:
        model = Teacher
        fields = ['name']
        
class SubjectSerializer(serializers.ModelSerializer):
    """
    Serializer for the Subject model.
    """
    
    class Meta:
        model = Subject
        fields = ['name']
        
class ClassSerializer(serializers.ModelSerializer):
    """
    Serializer for the Class model, including student count.
    """
    student_count = serializers.IntegerField(source='students.count', read_only=True)
    
    class Meta:
        model = Class
        fields = ['name', 'student_count']

class ScheduleSerializer(serializers.ModelSerializer):
    """
    Serializer for the Schedule model, including nested class and subject details.
    """
    class_assigned = ClassSerializer()
    subject = SubjectSerializer()
    teacher = TeacherSerializer(source='subject.teacher')
    day_of_week = serializers.CharField(source='get_day_of_week_display')

    class Meta:
        model = Schedule
        fields = ['class_assigned', 'subject', 'day_of_week', 'hour', 'teacher']
