from django.contrib import admin

from .models import (
    Achievement,
    CachedPlatformStats,
    ContactMessage,
    Education,
    Experience,
    Profile,
    Project,
    Skill,
)


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "location")


@admin.register(Education)
class EducationAdmin(admin.ModelAdmin):
    list_display = ("institution", "degree", "start_year", "end_year", "order")
    list_editable = ("order",)


@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = ("name", "category", "order")
    list_filter = ("category",)
    list_editable = ("order",)


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ("title", "date_range", "is_research", "order")
    list_filter = ("is_research",)
    filter_horizontal = ("technologies",)
    list_editable = ("order",)


@admin.register(Experience)
class ExperienceAdmin(admin.ModelAdmin):
    list_display = ("organization", "role", "start_label", "end_label", "order")
    list_editable = ("order",)


@admin.register(Achievement)
class AchievementAdmin(admin.ModelAdmin):
    list_display = ("platform", "handle", "current_rating", "max_rating", "rank_text")
    list_editable = ("handle", "current_rating", "max_rating", "rank_text")


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "created_at")
    readonly_fields = ("created_at",)


@admin.register(CachedPlatformStats)
class CachedPlatformStatsAdmin(admin.ModelAdmin):
    list_display = ("platform", "handle", "fetched_at")
    readonly_fields = ("fetched_at",)
