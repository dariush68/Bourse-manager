# BourseManager
from bourseapp import models
list = models.Company.objects.filter(symbol__icontains='ک')
for itm in list:
    itm.symbol.replace('ك', 'ک')
    itm.save()
