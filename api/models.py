from django.db import models


class Profile(models.Model):
    name = models.CharField(max_length=120)
    tagline = models.CharField(max_length=255, blank=True)
    phone = models.CharField(max_length=20, blank=True)
    email = models.EmailField(blank=True)
    github_url = models.URLField(blank=True)
    linkedin_url = models.URLField(blank=True)
    location = models.CharField(max_length=120, blank=True)
    bio = models.TextField(blank=True)
    resume_url = models.URLField(blank=True)

    def __str__(self):
        return self.name


class Education(models.Model):
    institution = models.CharField(max_length=200)
    degree = models.CharField(max_length=200)
    location = models.CharField(max_length=120, blank=True)
    start_year = models.PositiveIntegerField()
    end_year = models.PositiveIntegerField(null=True, blank=True)
    gpa_label = models.CharField(max_length=50, blank=True)
    gpa_value = models.CharField(max_length=20, blank=True)
    highlights = models.JSONField(default=list, blank=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order", "-start_year"]

    def __str__(self):
        return f"{self.institution} — {self.degree}"


class Skill(models.Model):
    CATEGORY_CHOICES = (
        ("LANG", "Language"),
        ("FRAME", "Framework"),
        ("TOOL", "Tool"),
        ("COURSE", "Coursework"),
    )

    name = models.CharField(max_length=80, unique=True)
    category = models.CharField(max_length=6, choices=CATEGORY_CHOICES, db_index=True)
    icon_key = models.CharField(max_length=40, blank=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["category", "order", "name"]

    def __str__(self):
        return self.name


class Project(models.Model):
    title = models.CharField(max_length=150)
    subtitle = models.CharField(max_length=150, blank=True)
    date_range = models.CharField(max_length=80, blank=True)
    description = models.TextField(blank=True)
    highlights = models.JSONField(default=list, blank=True)
    github_url = models.URLField(blank=True)
    live_url = models.URLField(blank=True)
    is_research = models.BooleanField(default=False)
    technologies = models.ManyToManyField(Skill, related_name="projects", blank=True)
    order = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["order", "-created_at"]

    def __str__(self):
        return self.title


class Experience(models.Model):
    organization = models.CharField(max_length=200)
    role = models.CharField(max_length=150)
    location = models.CharField(max_length=120, blank=True)
    start_label = models.CharField(max_length=40)
    end_label = models.CharField(max_length=40, blank=True)
    bullets = models.JSONField(default=list, blank=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order", "-start_label"]

    def __str__(self):
        return f"{self.role} @ {self.organization}"


class Achievement(models.Model):
    PLATFORM_CHOICES = (
        ("codeforces", "Codeforces"),
        ("codechef", "CodeChef"),
        ("leetcode", "LeetCode"),
    )

    platform = models.CharField(max_length=20, choices=PLATFORM_CHOICES, unique=True)
    handle = models.CharField(max_length=80)
    profile_url = models.URLField()
    max_rating = models.IntegerField(default=0)
    current_rating = models.IntegerField(default=0)
    rank_text = models.CharField(max_length=120, blank=True)
    problems_solved = models.IntegerField(default=0)
    extra_stats = models.JSONField(default=dict, blank=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order"]

    def __str__(self):
        return f"{self.platform} — {self.handle}"


class ContactMessage(models.Model):
    name = models.CharField(max_length=120)
    email = models.EmailField()
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.name} — {self.email}"


class CachedPlatformStats(models.Model):
    platform = models.CharField(max_length=20, unique=True)
    handle = models.CharField(max_length=80)
    payload = models.JSONField(default=dict)
    fetched_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.platform} cache ({self.handle})"
