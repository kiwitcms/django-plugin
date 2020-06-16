from django.db import models


class PageInfo(models.Model):
    page_title = models.CharField(max_length=20)
