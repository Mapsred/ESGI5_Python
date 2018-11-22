from accounts.models import ProfileAction


def log_profile_activity(profile, action, data=None):
    profile_action = ProfileAction(profile=profile, action=action, data=data)
    profile_action.save()

    return profile_action
