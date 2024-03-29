# -*- coding: utf-8 -*-
# Generated by Django 1.11.18 on 2019-10-15 06:17
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('stocks', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='BOSStock',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('role', models.IntegerField(choices=[(0, 'Buy'), (1, 'Sell')], default=0, verbose_name='角色')),
                ('price', models.DecimalField(decimal_places=2, max_digits=8, verbose_name='买卖价格')),
                ('amount', models.IntegerField(verbose_name='买卖数量')),
                ('datetime', models.DateTimeField(auto_now_add=True, verbose_name='挂单日期')),
            ],
            options={
                'verbose_name': '买卖挂单',
                'verbose_name_plural': '买卖挂单',
                'db_table': 'BOSStock',
                'ordering': ['-datetime'],
            },
        ),
        migrations.CreateModel(
            name='DealStock',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price', models.DecimalField(decimal_places=2, max_digits=8, verbose_name='成交价格')),
                ('amount', models.IntegerField(verbose_name='成交数量')),
                ('datetime', models.DateTimeField(auto_now_add=True, verbose_name='成交日期')),
                ('stock', models.CharField(max_length=400, verbose_name='股票信息')),
            ],
            options={
                'verbose_name': '买卖成交',
                'verbose_name_plural': '买卖成交',
                'db_table': 'DealStock',
                'ordering': ['-datetime'],
            },
        ),
        migrations.CreateModel(
            name='SelfStock',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('stock', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='stocks.Stock', verbose_name='股票')),
            ],
            options={
                'verbose_name': '自选股',
                'verbose_name_plural': '自选股',
                'db_table': 'SelfStock',
            },
        ),
    ]
