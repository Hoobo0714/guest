from django.db import models

# Create your models here.

#创建发布表
class Event(models.Model):
    name = models.CharField(max_length=100)  #发布会标题
    limit = models.IntegerField() #参加人数
    status = models.BooleanField()  #状态
    address = models.CharField(max_lenth=200)   #地址
    start_time = models.DateTimeField('event time') #发布会时间
    create_time = models.DateTimeField(auto_now=True)   #创建时间（自动获取当前时间）

    def __str__(self):
        return self.name

#嘉宾表
class Guest(models.Model):
    enent =models.ForeignKey(Event)   #关联发布会id
    realname = models.CharField(max_lenth=64)   #姓名
    phone = models.CharField(max_length=16) #电话号
    email = models.EmailField() #邮箱
    sgin = models.BooleanField()    #签到状态
    create_time = models.DateTimeField(auto_now=True)   #创建时间

    class Meta:
        unique_together = ('event','phone')

    def __str__(self):
        return self.realname