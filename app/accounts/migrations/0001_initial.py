# Generated by Django 3.2.1 on 2022-02-23 09:03

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(max_length=40, unique=True)),
                ('email', models.EmailField(max_length=255, verbose_name='Primary Email Address')),
                ('full_name', models.CharField(max_length=255)),
                ('date_joined', models.DateField(auto_now=True)),
                ('is_active', models.BooleanField(default=False)),
                ('is_staff', models.BooleanField(default=False)),
                ('age', models.CharField(choices=[('range_one', '20-29'), ('range_two', '30-39'), ('range_three', '40-49'), ('range_four', 'Above 50')], max_length=20, null=True)),
                ('gender', models.CharField(choices=[('male', 'Male'), ('female', 'Female'), ('undisclosed', 'Prefer not to say'), ('other', 'Other')], max_length=20)),
                ('preferred_language', models.CharField(choices=[('english', 'English'), ('french', 'French'), ('portuguese', 'Portuguese')], max_length=40)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
