from django.db import models

class TimeStempedModel(models.Model):
    created = models.DateTimeField('criado em', auto_now_add=True, auto_now=False)
    modified = models.DateTimeField('modificado em', auto_now_add=False, auto_now=True),


    # usado como herança em outros models 
    class Meta:
        abstract = True