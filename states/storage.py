# states/storage.py

"""
{
    user_id: {
        "state": UserState.ADD_FOR_FIRM,
        "data": {...},
        "messages": ["mid1", "mid2"],
        "expires_at": 1710000000
    }
}
"""

storage: dict[int, dict] = {}