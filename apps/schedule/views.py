from rest_framework import generics
from django.utils import timezone
from .models import Schedule
from .serializers import ScheduleSerializer

class ScheduleListView(generics.ListAPIView):
    """
    API view to retrieve the list of schedules.

    Query Parameters:
        for_today (str): If 'true', filters the schedules for the current day.
        class_name (str): Filters the schedules by class name.

    Returns:
        A list of schedules with details.
    """
    serializer_class = ScheduleSerializer

    def get_queryset(self):
        """
        Override the default queryset to provide filtering and optimization.

        Returns:
            QuerySet: The optimized queryset for schedules.
        """
        # Potential Improvement:
        # Implement full-text search capabilities, advanced filtering options, caching, and async processing.
        # More details are in the README.md file.
        
        # Base queryset with necessary select_related to optimize queries
        queryset = Schedule.objects.select_related(
            'class_assigned',
            'subject',
            'subject__teacher'
        )

        # Filter by 'for_today' parameter if present
        for_today = self.request.query_params.get('for_today')
        if for_today == 'true':
            today = timezone.now().weekday()
            queryset = queryset.filter(day_of_week=today)

        # Filter by 'class_name' parameter if present
        class_name = self.request.query_params.get('class_name')
        if class_name:
            queryset = queryset.filter(class_assigned__name=class_name)
            
        # Order by day_of_week and hour
        queryset = queryset.order_by('day_of_week', 'hour')

        return queryset
