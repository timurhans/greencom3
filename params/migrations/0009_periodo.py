# Generated by Django 2.1.7 on 2020-09-07 12:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('params', '0008_auto_20200618_2218'),
    ]

    operations = [
        migrations.CreateModel(
            name='Periodo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ordem', models.IntegerField(unique=True)),
                ('periodo_faturamento', models.DateField()),
                ('periodo_vendas', models.DateField()),
                ('desc_periodo', models.CharField(max_length=150)),
            ],
        ),
    ]
