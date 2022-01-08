from django.db import models

# Create your models here.


class Schedule(models.Model):
    """APIで返すモデル
    PlanID: Pkey
    UserID: ユーザーID
    PlanFrom: 予定のスタート月日時分
    PlanTo: 予定終了月日時分
    Title:予定のタイトル
    PlanAbout: 予定内容

    """
    PlanID = models.AutoField(primary_key=True)
    UserID = models.TextField("ID", default="test")
    PlanFrom = models.DateTimeField("Start")
    PlanTo = models.DateTimeField("End")
    Title = models.TextField("Title", max_length=100, default="")
    PlanAbout = models.TextField("About")
    Color = models.TextField("表示色", default="black")
    CreateDate = models.DateTimeField(auto_now_add=True)
    UpdateDate = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['PlanFrom', 'PlanTo']
