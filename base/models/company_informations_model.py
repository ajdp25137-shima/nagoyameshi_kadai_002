from django.db import models

class CompanyInformation(models.Model):
    # PK: ID は Django が自動で作成します
    name = models.CharField(max_length=255, verbose_name="会社名")
    representative = models.CharField(max_length=255, verbose_name="代表者")
    established_date = models.DateField(verbose_name="設立日")
    postal_code = models.CharField(max_length=10, verbose_name="郵便番号")
    address = models.CharField(max_length=255, verbose_name="所在地")
    business_description = models.TextField(verbose_name="事業内容")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "会社情報"
        verbose_name_plural = "会社情報"

    def __str__(self):
        return self.name