from rest_framework import serializers
from schedule.models import Schedule


class ScheduleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Schedule
        fields = ["PlanID", "UserID", "PlanFrom", "Color",
                  "PlanTo", "Title", "PlanAbout"]
