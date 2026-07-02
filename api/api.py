from ninja import NinjaAPI, Schema
from typing import List, Optional

from .models import (
    ContactMessage,
    Education,
    Experience,
    Profile,
    Project,
    Skill,
)
from .services.cp_stats import get_all_achievement_stats

api = NinjaAPI(title="Shivendu Portfolio API", version="1.0.0")


class ProfileSchema(Schema):
    name: str
    tagline: str
    phone: str
    email: str
    github_url: str
    linkedin_url: str
    location: str
    bio: str
    resume_url: str


class EducationSchema(Schema):
    id: int
    institution: str
    degree: str
    location: str
    start_year: int
    end_year: Optional[int]
    gpa_label: str
    gpa_value: str
    highlights: list


class SkillSchema(Schema):
    name: str
    category: str
    icon_key: str


class SkillsGroupedSchema(Schema):
    LANG: List[SkillSchema]
    FRAME: List[SkillSchema]
    TOOL: List[SkillSchema]
    COURSE: List[SkillSchema]


class ProjectSchema(Schema):
    id: int
    title: str
    subtitle: str
    date_range: str
    description: str
    highlights: list
    github_url: str
    live_url: str
    is_research: bool
    technologies: List[SkillSchema]


class ExperienceSchema(Schema):
    id: int
    organization: str
    role: str
    location: str
    start_label: str
    end_label: str
    bullets: list


class AchievementStatsSchema(Schema):
    platform: str
    handle: str
    profile_url: str
    current_rating: int
    max_rating: int
    rank_text: str
    problems_solved: int
    extra_stats: dict
    source: str
    avatar_url: str
    last_synced: Optional[str]


class ContactInSchema(Schema):
    name: str
    email: str
    message: str


class ContactOutSchema(Schema):
    success: bool
    id: int


@api.get("/health")
def health(request):
    return {"status": "ok"}


@api.get("/profile", response=ProfileSchema)
def get_profile(request):
    profile = Profile.objects.first()
    if not profile:
        from ninja.errors import HttpError
        raise HttpError(404, "Profile not found. Run: python manage.py seed_resume")
    return profile


@api.get("/education", response=List[EducationSchema])
def list_education(request):
    return Education.objects.all()


@api.get("/skills", response=SkillsGroupedSchema)
def list_skills(request):
    grouped = {"LANG": [], "FRAME": [], "TOOL": [], "COURSE": []}
    for skill in Skill.objects.all():
        grouped[skill.category].append(skill)
    return grouped


@api.get("/projects", response=List[ProjectSchema])
def list_projects(request):
    return Project.objects.prefetch_related("technologies").all()


@api.get("/experience", response=List[ExperienceSchema])
def list_experience(request):
    return Experience.objects.all()


@api.get("/achievements", response=List[AchievementStatsSchema])
def list_achievements(request, refresh: bool = False):
    return get_all_achievement_stats(force_refresh=refresh)


@api.post("/contact", response=ContactOutSchema)
def submit_contact(request, payload: ContactInSchema):
    msg = ContactMessage.objects.create(
        name=payload.name.strip(),
        email=payload.email.strip(),
        message=payload.message.strip(),
    )
    return {"success": True, "id": msg.id}
