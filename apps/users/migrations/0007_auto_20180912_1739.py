# Generated by Django 2.1 on 2018-09-12 17:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0006_auto_20180912_1737'),
    ]

    operations = [
        migrations.AlterField(
            model_name='emailverifyrecord',
            name='send_type',
            field=models.CharField(choices=[('register', '注册'), ('forget', '找回密码'), ('modify_email', '修改邮箱')], max_length=20, verbose_name='验证码类型'),
        ),
    ]