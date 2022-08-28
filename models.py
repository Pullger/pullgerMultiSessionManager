# import django.db.models
# from django.db import models
# from django.dispatch import receiver
# from django.db.models import signals
# from django.db.models import Q, F, ExpressionWrapper, Value
# from django.db.models import DateTimeField, IntegerField, BooleanField, DurationField
# from django.utils import timezone
# import logging
# import datetime
#
#
# class Accounts__Manager(models.Manager):
#     pass
#
#     def getActualList(self):
#         return self.filter(use=True, active=True)
#
#     def getByUUID(self, inUUID):
#         return Accounts.objects.filter(uuid=inUUID).first()
#
#     def getByLogin(self, inLogin):
#         return Accounts.objects.filter(login=inLogin).first()
#
#     def getAccesebleAccount(self):
#         # *F(timezone.timedelta(seconds=1))
#         # Accounts.objects.all().annotate(test=ExpressionWrapper(F('limitLastAccessMoment')+datetime.timedelta(hours=1), output_field=DateTimeField())).first()
#         # Accounts.objects.all().annotate(test=ExpressionWrapper(
#         #     F('limitLastAccessMoment') - F('limitMinIntervalFromLastAccess')
#         #     , output_field=DateTimeField()).first()
#         #
#         # models.DateField()
#         # models.DateTimeField())
#         #
#         # datetime.timedelta(hours=1)
#         # Accounts.objects.filter(use=True, active=True, limitLastAccessMoment__lte=F('limitLastAccessMoment') + datetime.timedelta(hours=1)).first()
#         #
#         # Accounts.objects.filter(use=True, active=True).first()
#         return Accounts.objects.filter(
#             use=True,
#             active=True,
#             limitLastAccessMoment__lte=datetime.datetime.now() - datetime.timedelta(seconds=1600),
#         ).first()
#
#
# class Accounts(models.Model):
#     uuid = models.CharField(max_length=36, primary_key = True)
#     use = models.BooleanField(null=True)
#     active = models.BooleanField(null=True)
#     service = models.CharField(max_length=50, null=False)
#     login = models.CharField(max_length=200, null=True)
#     password = models.CharField(max_length=200, null=False)
#     limitPeopleCount = models.IntegerField(null=True)
#     limitPeopleCircle = models.IntegerField(null=True)
#     limitPeopleMax = models.IntegerField(null=True)
#     limitCompanyCount = models.IntegerField(null=True)
#     limitCompanyCircle = models.IntegerField(null=True)
#     limitCompanyMax = models.IntegerField(null=True)
#     limitDateCounting = models.DateField(null=True)
#     limitLastAccessMoment = models.DateTimeField(null=True)
#     limitMinIntervalFromLastAccess = models.IntegerField(null=True)
#
#     objects = Accounts__Manager()
#
#     def renewAcessMoment(self):
#         self.limitLastAccessMoment = datetime.datetime.now()
#         self.save()
#
#     def getCircleLimitOfPeople(self):
#         return self.limitPeopleCircle
#
#     def getCircleLimitOfCompanies(self):
#         return self.limitCompanyCircle
#
#     def getCountLimitOfPeople(self):
#         return self.limitPeopleCount
#
#     def getCountLimitOfCompanies(self):
#         return self.limitCompanyCount
#
#     def getLoadingLimitOfPeople(self):
#         return self.limitPeopleMax
#
#     def getLoadingLimitOfCompanies(self):
#         return self.limitCompanyMax
#
#
#     def upCountOfPeople(self, upCount):
#         self.limitPeopleCount = self.limitPeopleCount + upCount
#         self.save()
#
#     def upCountOfCompany(self, upCount):
#         self.limitCompanyCount = self.limitCompanyCount + upCount
#         self.save()
#
#     def dataActualization(self, **kwargs):
#         if self.limitDateCounting < datetime.date(datetime.now()):
#             self.limitPeopleCount = 0;
#             self.limitCompanyCount = 0
#
#
#     @staticmethod
#     def putAccount(**kwargs):
#         purposeObject = None
#
#         if 'uuid' in kwargs:
#             purposeObject = Accounts.objects.getByUUID(kwargs['uuid'])
#
#         if purposeObject == None:
#             if 'login' in kwargs:
#                 purposeObject = Accounts.objects.getByLogin(kwargs['login'])
#             else:
#                 errorText = "Missed mandatory parameter 'login'"
#                 logging.error(errorText)
#                 raise Exception(errorText)
#
#         if purposeObject == None:
#             purposeObject = Accounts()
#
#         for key, value in kwargs.items():
#             if hasattr(purposeObject, key):
#                 setattr(purposeObject, key, value)
#
#         #Filling default DATA
#         purposeObject.use = purposeObject.use if purposeObject.use != None else True
#         purposeObject.active = purposeObject.active if purposeObject.active != None else True
#         purposeObject.limitPeopleCount = purposeObject.limitPeopleCount if purposeObject.limitPeopleCount != None else 0
#         purposeObject.limitPeopleCircle = purposeObject.limitPeopleCircle if purposeObject.limitPeopleCircle != None else 10
#         purposeObject.limitPeopleMax = purposeObject.limitPeopleMax if purposeObject.limitPeopleMax != None else 80
#         purposeObject.limitCompanyCount =  purposeObject.limitCompanyCount if purposeObject.limitCompanyCount != None else 0
#         purposeObject.limitCompanyCircle =  purposeObject.limitCompanyCircle if purposeObject.limitCompanyCircle != None else 20
#         purposeObject.limitCompanyMax =  purposeObject.limitCompanyMax if purposeObject.limitCompanyMax != None else 160
#         purposeObject.limitDateCounting =  purposeObject.limitDateCounting if purposeObject.limitDateCounting != None else datetime.date.today()
#         purposeObject.limitLastAccessMoment =  purposeObject.limitLastAccessMoment if purposeObject.limitLastAccessMoment != None else datetime.date(1,1,1)
#         purposeObject.limitMinIntervalFromLastAccess =  purposeObject.limitMinIntervalFromLastAccess if purposeObject.limitMinIntervalFromLastAccess != None else 1800
#
#         try:
#             purposeObject.save()
#         except Exception as e:
#             errorText = "Internal error on save"
#             logging.error(errorText)
#             raise Exception(errorText)
#
#
# @receiver(signals.pre_save, sender=Accounts)
# def add_people_uuid(sender, instance, **kwargs):
#     import uuid
#
#     if not instance.uuid:
#         instance.uuid = str(uuid.uuid1())
