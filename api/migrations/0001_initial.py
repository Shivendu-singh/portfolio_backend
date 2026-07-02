from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Achievement",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("platform", models.CharField(choices=[("codeforces", "Codeforces"), ("codechef", "CodeChef"), ("leetcode", "LeetCode")], max_length=20, unique=True)),
                ("handle", models.CharField(max_length=80)),
                ("profile_url", models.URLField()),
                ("max_rating", models.IntegerField(default=0)),
                ("current_rating", models.IntegerField(default=0)),
                ("rank_text", models.CharField(blank=True, max_length=120)),
                ("problems_solved", models.IntegerField(default=0)),
                ("extra_stats", models.JSONField(blank=True, default=dict)),
                ("order", models.PositiveIntegerField(default=0)),
            ],
            options={"ordering": ["order"]},
        ),
        migrations.CreateModel(
            name="CachedPlatformStats",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("platform", models.CharField(max_length=20, unique=True)),
                ("handle", models.CharField(max_length=80)),
                ("payload", models.JSONField(default=dict)),
                ("fetched_at", models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name="ContactMessage",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=120)),
                ("email", models.EmailField(max_length=254)),
                ("message", models.TextField()),
                ("created_at", models.DateTimeField(auto_now_add=True)),
            ],
            options={"ordering": ["-created_at"]},
        ),
        migrations.CreateModel(
            name="Education",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("institution", models.CharField(max_length=200)),
                ("degree", models.CharField(max_length=200)),
                ("location", models.CharField(blank=True, max_length=120)),
                ("start_year", models.PositiveIntegerField()),
                ("end_year", models.PositiveIntegerField(blank=True, null=True)),
                ("gpa_label", models.CharField(blank=True, max_length=50)),
                ("gpa_value", models.CharField(blank=True, max_length=20)),
                ("highlights", models.JSONField(blank=True, default=list)),
                ("order", models.PositiveIntegerField(default=0)),
            ],
            options={"ordering": ["order", "-start_year"]},
        ),
        migrations.CreateModel(
            name="Experience",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("organization", models.CharField(max_length=200)),
                ("role", models.CharField(max_length=150)),
                ("location", models.CharField(blank=True, max_length=120)),
                ("start_label", models.CharField(max_length=40)),
                ("end_label", models.CharField(blank=True, max_length=40)),
                ("bullets", models.JSONField(blank=True, default=list)),
                ("order", models.PositiveIntegerField(default=0)),
            ],
            options={"ordering": ["order", "-start_label"]},
        ),
        migrations.CreateModel(
            name="Profile",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=120)),
                ("tagline", models.CharField(blank=True, max_length=255)),
                ("phone", models.CharField(blank=True, max_length=20)),
                ("email", models.EmailField(blank=True, max_length=254)),
                ("github_url", models.URLField(blank=True)),
                ("linkedin_url", models.URLField(blank=True)),
                ("location", models.CharField(blank=True, max_length=120)),
                ("bio", models.TextField(blank=True)),
                ("resume_url", models.URLField(blank=True)),
            ],
        ),
        migrations.CreateModel(
            name="Skill",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=80, unique=True)),
                ("category", models.CharField(choices=[("LANG", "Language"), ("FRAME", "Framework"), ("TOOL", "Tool"), ("COURSE", "Coursework")], db_index=True, max_length=6)),
                ("icon_key", models.CharField(blank=True, max_length=40)),
                ("order", models.PositiveIntegerField(default=0)),
            ],
            options={"ordering": ["category", "order", "name"]},
        ),
        migrations.CreateModel(
            name="Project",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("title", models.CharField(max_length=150)),
                ("subtitle", models.CharField(blank=True, max_length=150)),
                ("date_range", models.CharField(blank=True, max_length=80)),
                ("description", models.TextField(blank=True)),
                ("highlights", models.JSONField(blank=True, default=list)),
                ("github_url", models.URLField(blank=True)),
                ("live_url", models.URLField(blank=True)),
                ("is_research", models.BooleanField(default=False)),
                ("order", models.PositiveIntegerField(default=0)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("technologies", models.ManyToManyField(blank=True, related_name="projects", to="api.skill")),
            ],
            options={"ordering": ["order", "-created_at"]},
        ),
    ]
