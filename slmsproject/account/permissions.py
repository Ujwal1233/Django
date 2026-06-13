from django.contrib.auth.models import User


def is_staff_user(user: User) -> bool:
    """Return True if user has a Profile with role == 'staff' (or 'admin')."""
    if not user or not getattr(user, "is_authenticated", False):
        return False

    # Local import to avoid circular import during app loading
    from account.models import Profile

    try:
        role = Profile.objects.get(user=user).role
    except Profile.DoesNotExist:
        return False

    return role in {"staff", "admin"}

