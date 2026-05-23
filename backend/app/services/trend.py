def calculate_trend_score(views: int, likes: int, comments: int, shares: int, followers: int) -> float:
    follower_base = max(followers, 1)
    view_velocity = views / follower_base
    engagement_ratio = (likes + comments + shares) / max(views, 1)
    comment_velocity = comments / follower_base
    return round((view_velocity * 0.5) + (engagement_ratio * 0.3) + (comment_velocity * 0.2), 4)
