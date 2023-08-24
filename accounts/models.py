from django.db import models
class AccountModels(models.Model):
    MEMBERSHIP_TYPE = [
        ('special','ویژه'),
        ('Normal','عادی')
    ]
    frist_name = models.CharField(max_length=255,null=True,blank=True)
    last_name = models.CharField(max_length=255,null=True,blank=True)
    email = models.EmailField()
    phon_number = models.ImageField()
    membershipـtype = models.CharField(max_length=30,choices=MEMBERSHIP_TYPE,default=[1])
    Membership_validity_date = models.DateField()
    Membership_expiration_date = models.DateField()
    
    def __str__(self) -> str:
        return self.membershipـtype