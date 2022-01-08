from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework import serializers
from rest_framework.parsers import JSONParser
from schedule.models import Schedule
from schedule.serializers import ScheduleSerializer

# Create your views here.


@csrf_exempt
def schedule_list(request, userID: str = "test"):
    """
    List all code Schedules, or create a new Schedule.
    """
    if request.method == 'GET':
        if userID == "test":
            schedules = Schedule.objects.all()
        else:
            schedules = Schedule.objects.filter(UserID=userID)

        serializer = ScheduleSerializer(schedules, many=True)
        return JsonResponse(serializer.data, safe=False)


@csrf_exempt
def schedule_detail(request, planid: int = 0):
    """
    Retrieve, update or delete a code Schedule.
    """
    if request.method == 'GET':
        try:
            schedule = Schedule.objects.get(PlanID=planid)
        except Schedule.DoesNotExist:
            return HttpResponse(status=404)

        serializer = ScheduleSerializer(schedule)
        return JsonResponse(serializer.data)

    elif request.method == 'PUT':
        # データ更新
        data = JSONParser().parse(request)
        print(data)
        print(planid)
        if planid == 0:
            # insert を呼ぶシリアライザー
            serializer = ScheduleSerializer(Schedule(), data=data)
        else:
            # updateを呼ぶシリアライザー
            schedule = Schedule.objects.get(PlanID=planid)
            serializer = ScheduleSerializer(schedule, data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data)
        return JsonResponse(serializer.errors, status=400)

    elif request.method == 'DELETE':
        try:
            schedule = Schedule.objects.get(PlanID=planid)
            print(schedule)
        except Schedule.DoesNotExist:
            return HttpResponse(status=404)
        schedule.delete()
        return HttpResponse(status=204)
