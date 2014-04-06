from django.conf import settings

from twython import Twython


def get_user_timeline(screen_name, **kwargs):
    """Returns ``Post`` dict list from the given ``screen_name``
    twitter public timeline."""
    twitter = Twython(
        settings.TWITTER_KEY, settings.TWITTER_SECRET, oauth_version=2)
    token = twitter.obtain_access_token()
    twitter = Twython(settings.TWITTER_KEY, access_token=token)
    timeline = twitter.get_user_timeline(screen_name=screen_name, **kwargs)
    return [i for i in timeline if not i['text'].startswith('@')]
