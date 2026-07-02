from __future__ import annotations

from datetime import timedelta
from typing import Any

import httpx
from django.conf import settings
from django.utils import timezone

from api.models import Achievement, CachedPlatformStats


def _cache_is_fresh(cache: CachedPlatformStats | None) -> bool:
    if not cache:
        return False
    ttl = getattr(settings, "CP_CACHE_TTL_SECONDS", 3600)
    return timezone.now() - cache.fetched_at < timedelta(seconds=ttl)


def _save_cache(platform: str, handle: str, payload: dict[str, Any]) -> dict[str, Any]:
    CachedPlatformStats.objects.update_or_create(
        platform=platform,
        defaults={"handle": handle, "payload": payload},
    )
    return payload


def _fallback_payload(achievement: Achievement, source: str = "static") -> dict[str, Any]:
    return {
        "platform": achievement.platform,
        "handle": achievement.handle,
        "profile_url": achievement.profile_url,
        "current_rating": achievement.current_rating,
        "max_rating": achievement.max_rating,
        "rank_text": achievement.rank_text,
        "problems_solved": achievement.problems_solved,
        "extra_stats": achievement.extra_stats,
        "source": source,
        "avatar_url": "",
        "last_synced": "",
    }


def fetch_codeforces_stats(achievement: Achievement) -> dict[str, Any]:
    handle = achievement.handle
    url = f"https://codeforces.com/api/user.info?handles={handle}"

    try:
        response = httpx.get(url, timeout=10.0)
        response.raise_for_status()
        data = response.json()
        if data.get("status") != "OK" or not data.get("result"):
            raise ValueError(data.get("comment", "Codeforces API error"))

        user = data["result"][0]
        payload = {
            "platform": "codeforces",
            "handle": user.get("handle", handle),
            "profile_url": achievement.profile_url,
            "current_rating": user.get("rating") or achievement.current_rating,
            "max_rating": user.get("maxRating") or achievement.max_rating,
            "rank_text": (user.get("rank") or achievement.rank_text or "").replace("_", " ").title(),
            "problems_solved": achievement.problems_solved,
            "extra_stats": {
                "max_rank": (user.get("maxRank") or "").replace("_", " ").title(),
                "contribution": user.get("contribution", 0),
                "friend_of_count": user.get("friendOfCount", 0),
            },
            "source": "live",
            "avatar_url": f"https:{user['avatar']}" if user.get("avatar", "").startswith("//") else user.get("avatar", ""),
            "last_synced": timezone.now().isoformat(),
        }
        return _save_cache("codeforces", handle, payload)
    except Exception:
        cache = CachedPlatformStats.objects.filter(platform="codeforces").first()
        if cache:
            stale = dict(cache.payload)
            stale["source"] = "stale_cache"
            stale["last_synced"] = cache.fetched_at.isoformat()
            return stale
        return _fallback_payload(achievement)


LEETCODE_GRAPHQL = """
query userPublicProfile($username: String!) {
  matchedUser(username: $username) {
    username
    profile {
      ranking
      userAvatar
      realName
    }
    submitStats: submitStatsGlobal {
      acSubmissionNum {
        difficulty
        count
      }
    }
  }
}
query userContestRankingInfo($username: String!) {
  userContestRanking(username: $username) {
    rating
    globalRanking
    topPercentage
    attendedContestsCount
  }
}
"""


def fetch_leetcode_stats(achievement: Achievement) -> dict[str, Any]:
    handle = achievement.handle
    query = """
    query userStats($username: String!) {
      matchedUser(username: $username) {
        username
        profile { ranking userAvatar }
        submitStats: submitStatsGlobal {
          acSubmissionNum { difficulty count }
        }
      }
      userContestRanking(username: $username) {
        rating
        globalRanking
        topPercentage
        attendedContestsCount
      }
    }
    """

    try:
        response = httpx.post(
            "https://leetcode.com/graphql",
            json={"query": query, "variables": {"username": handle}},
            headers={"Content-Type": "application/json"},
            timeout=12.0,
        )
        response.raise_for_status()
        body = response.json()
        matched = (body.get("data") or {}).get("matchedUser") or {}
        contest = (body.get("data") or {}).get("userContestRanking") or {}

        solved = 0
        for item in (matched.get("submitStats") or {}).get("acSubmissionNum") or []:
            if item.get("difficulty") == "All":
                solved = item.get("count", 0)
                break
        if not solved:
            nums = (matched.get("submitStats") or {}).get("acSubmissionNum") or []
            solved = sum(item.get("count", 0) for item in nums)

        payload = {
            "platform": "leetcode",
            "handle": matched.get("username") or handle,
            "profile_url": achievement.profile_url,
            "current_rating": int(contest.get("rating")) if contest.get("rating") is not None else achievement.current_rating,
            "max_rating": achievement.max_rating,
            "rank_text": achievement.rank_text or f"Top {contest.get('topPercentage', '—')}% globally",
            "problems_solved": solved or achievement.problems_solved,
            "extra_stats": {
                "global_ranking": contest.get("globalRanking"),
                "contests_attended": contest.get("attendedContestsCount"),
                "profile_ranking": (matched.get("profile") or {}).get("ranking"),
            },
            "source": "live",
            "avatar_url": (matched.get("profile") or {}).get("userAvatar", ""),
            "last_synced": timezone.now().isoformat(),
        }
        return _save_cache("leetcode", handle, payload)
    except Exception:
        cache = CachedPlatformStats.objects.filter(platform="leetcode").first()
        if cache:
            stale = dict(cache.payload)
            stale["source"] = "stale_cache"
            stale["last_synced"] = cache.fetched_at.isoformat()
            return stale
        return _fallback_payload(achievement)


def fetch_codechef_stats(achievement: Achievement) -> dict[str, Any]:
    handle = achievement.handle
    url = f"https://www.codechef.com/users/{handle}"

    try:
        response = httpx.get(
            url,
            timeout=12.0,
            headers={"User-Agent": "Mozilla/5.0 (compatible; PortfolioBot/1.0)"},
            follow_redirects=True,
        )
        response.raise_for_status()
        html = response.text

        rating = achievement.current_rating
        max_rating = achievement.max_rating
        rank_text = achievement.rank_text

        if "rating-number" in html:
            import re

            match = re.search(r'<div class="rating-number[^"]*">\s*(\d+)\s*</div>', html)
            if match:
                rating = int(match.group(1))
        if "rating-header" in html and "★" in html:
            import re

            star = re.search(r"(\d)\s*★", html)
            if star:
                rank_text = f"{star.group(1)}-Star"

        payload = {
            "platform": "codechef",
            "handle": handle,
            "profile_url": achievement.profile_url,
            "current_rating": rating,
            "max_rating": max_rating,
            "rank_text": rank_text,
            "problems_solved": achievement.problems_solved,
            "extra_stats": achievement.extra_stats,
            "source": "live",
            "avatar_url": "",
            "last_synced": timezone.now().isoformat(),
        }
        return _save_cache("codechef", handle, payload)
    except Exception:
        cache = CachedPlatformStats.objects.filter(platform="codechef").first()
        if cache:
            stale = dict(cache.payload)
            stale["source"] = "stale_cache"
            stale["last_synced"] = cache.fetched_at.isoformat()
            return stale
        fallback = _fallback_payload(achievement, source="static")
        fallback["last_synced"] = None
        return fallback


FETCHERS = {
    "codeforces": fetch_codeforces_stats,
    "leetcode": fetch_leetcode_stats,
    "codechef": fetch_codechef_stats,
}


def get_platform_stats(achievement: Achievement, force_refresh: bool = False) -> dict[str, Any]:
    cache = CachedPlatformStats.objects.filter(platform=achievement.platform).first()
    if not force_refresh and _cache_is_fresh(cache):
        payload = dict(cache.payload)
        payload["source"] = payload.get("source", "cache")
        payload["last_synced"] = cache.fetched_at.isoformat()
        return payload

    fetcher = FETCHERS.get(achievement.platform)
    if not fetcher:
        return _fallback_payload(achievement)

    return fetcher(achievement)


def get_all_achievement_stats(force_refresh: bool = False) -> list[dict[str, Any]]:
    achievements = Achievement.objects.all()
    return [get_platform_stats(a, force_refresh=force_refresh) for a in achievements]
