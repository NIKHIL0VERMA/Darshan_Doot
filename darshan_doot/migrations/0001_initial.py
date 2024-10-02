# Generated by Django 5.1 on 2024-10-02 15:10

import django.db.models.deletion
import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('date', models.DateTimeField()),
                ('description', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Museum',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, unique=True)),
                ('location', models.CharField(max_length=255)),
                ('indian_adult_fee', models.DecimalField(decimal_places=2, max_digits=10)),
                ('indian_child_fee', models.DecimalField(decimal_places=2, max_digits=10)),
                ('free_for_students', models.BooleanField(default=False)),
                ('camera_fee', models.DecimalField(decimal_places=2, max_digits=10)),
                ('international_citizen_fee', models.DecimalField(decimal_places=2, max_digits=10)),
                ('timings', models.CharField(max_length=255)),
                ('closed_on', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('status', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Ticket',
            fields=[
                ('ticket_id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('user_phone', models.CharField(max_length=15)),
                ('user_email', models.EmailField(max_length=254)),
                ('booking_date', models.DateTimeField(auto_now_add=True)),
                ('visiting_date', models.DateField()),
                ('payment_status', models.CharField(default='pending', max_length=20)),
                ('adults', models.PositiveIntegerField()),
                ('children', models.PositiveIntegerField()),
                ('total_amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('verification_code', models.CharField(blank=True, max_length=20, null=True)),
                ('transaction_id', models.CharField(blank=True, max_length=255, null=True)),
                ('stripe_payment_intent_id', models.CharField(blank=True, max_length=255, null=True)),
                ('nationality', models.CharField(max_length=100)),
                ('museum', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='darshan_doot.museum')),
            ],
        ),
        migrations.CreateModel(
            name='Person',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nationality', models.CharField(max_length=100)),
                ('gender', models.CharField(max_length=10)),
                ('is_indian', models.BooleanField()),
                ('ticket', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='people', to='darshan_doot.ticket')),
            ],
        ),
    ]
