from ..compat import compat_urllib_parse
from ..compatpatch import ClientCompatPatch


class FeedEndpointsMixin(object):

    def feed_liked(self):
        """Get liked feed"""
        res = self._call_api('feed/liked/')
        if self.auto_patch and res.get('items'):
            [ClientCompatPatch.media(m, drop_incompat_keys=self.drop_incompat_keys)
             for m in res.get('items', [])]
        return res

    def feed_timeline(self, **kwargs):
        """
        Get timeline feed. To get a new timeline feed, you can mark a set of media
        as seen by setting seen_posts = comma-separated list of media IDs. Example:
        api.feed_timeline(seen_posts='123456789_12345,987654321_54321')
        """
        endpoint = 'feed/timeline/'
        params = {
            '_uuid': self.uuid,
            '_csrftoken': self.csrftoken,
            'is_prefetch': '0',
            'is_pull_to_refresh': '0',
            'phone_id': self.phone_id,
            'timezone_offset': self.timezone_offset,
        }
        if kwargs:
            params.update(kwargs)
        res = self._call_api(endpoint, params=params, unsigned=True)
        if self.auto_patch:
            [ClientCompatPatch.media(m['media_or_ad'], drop_incompat_keys=self.drop_incompat_keys)
             if m.get('media_or_ad') else m
             for m in res.get('feed_items', [])]
        return res

    def feed_popular(self, **kwargs):
        """Get popular feed"""
        query = {
            'people_teaser_supported': '1',
            'rank_token': self.rank_token,
            'ranked_content': 'true'
        }
        if kwargs:
            query.update(kwargs)
        endpoint = 'feed/popular/?' + compat_urllib_parse.urlencode(query)
        res = self._call_api(endpoint)
        if self.auto_patch:
            [ClientCompatPatch.media(m, drop_incompat_keys=self.drop_incompat_keys)
             for m in res.get('items', [])]
        return res

    def user_feed(self, user_id, **kwargs):
        """
        Get the feed for the specified user id

        :param user_id:
        :param kwargs:
            - **max_id**: For pagination
            - **min_timestamp**: For pagination
        :return:
        """
        endpoint = 'feed/user/%(user_id)s/?' % {'user_id': user_id}
        default_params = {'rank_token': self.rank_token, 'ranked_content': 'true'}
        params = default_params.copy()
        if kwargs:
            params.update(kwargs)
        endpoint += compat_urllib_parse.urlencode(params)
        res = self._call_api(endpoint)

        if self.auto_patch:
            [ClientCompatPatch.media(m, drop_incompat_keys=self.drop_incompat_keys)
             for m in res.get('items', [])]
        return res

    def self_feed(self):
        """Get authenticated user's own feed"""
        return self.user_feed(self.authenticated_user_id)

    def username_feed(self, user_name, **kwargs):
        """
        Get the feed for the specified user name

        :param user_name:
        :param kwargs:
            - **max_id**: For pagination
            - **min_timestamp**: For pagination
        :return:
        """
        endpoint = 'feed/user/%(user_name)s/username/' % {'user_name': user_name}
        if kwargs:
            endpoint += '?' + compat_urllib_parse.urlencode(kwargs)
        res = self._call_api(endpoint)
        if self.auto_patch:
            [ClientCompatPatch.media(m, drop_incompat_keys=self.drop_incompat_keys)
             for m in res.get('items', [])]
        return res

    def reels_tray(self, **kwargs):
        """Get story reels tray"""
        endpoint = 'feed/reels_tray/'
        params = {}
        if kwargs or params:
            params.update(kwargs)
            endpoint += '?' + compat_urllib_parse.urlencode(params)

        res = self._call_api(endpoint)
        if self.auto_patch:
            for u in res.get('tray', []):
                [ClientCompatPatch.media(m, drop_incompat_keys=self.drop_incompat_keys)
                 for m in u.get('items', [])]
        return res

    def user_reel_media(self, user_id, **kwargs):
        """
        Get user story/reel media

        :param user_id:
        :param kwargs:
        :return:
        """
        endpoint = 'feed/user/%(user_id)s/reel_media/' % {'user_id': user_id}
        params = {}
        if kwargs or params:
            params.update(kwargs)
            endpoint += '?' + compat_urllib_parse.urlencode(params)

        res = self._call_api(endpoint)
        if self.auto_patch:
            [ClientCompatPatch.media(m, drop_incompat_keys=self.drop_incompat_keys)
             for m in res.get('items', [])]
        return res

    def reels_media(self, user_ids, **kwargs):
        """
        Get multiple users' reel/story media

        :param user_ids: list of user IDs
        :param kwargs:
        :return:
        """
        endpoint = 'feed/reels_media/'
        user_ids = list(map(lambda x: str(x), user_ids))
        params = {'user_ids': user_ids}
        if kwargs:
            params.update(kwargs)

        res = self._call_api(endpoint, params=params)
        if self.auto_patch:
            for reel_media in res.get('reels_media', []):
                [ClientCompatPatch.media(m, drop_incompat_keys=self.drop_incompat_keys)
                 for m in reel_media.get('items', [])]
            for user_id, reel in list(res.get('reels', {}).items()):
                [ClientCompatPatch.media(m, drop_incompat_keys=self.drop_incompat_keys)
                 for m in reel.get('items', [])]
        return res

    def feed_tag(self, tag, **kwargs):
        """
        Get tag feed

        :param tag:
        :return:
        """
        endpoint = 'feed/tag/%(tag)s/' % {'tag': tag}
        if kwargs:
            endpoint += '?' + compat_urllib_parse.urlencode(kwargs)
        res = self._call_api(endpoint)
        if self.auto_patch:
            if res.get('items'):
                [ClientCompatPatch.media(m, drop_incompat_keys=self.drop_incompat_keys)
                 for m in res.get('items', [])]
            if res.get('ranked_items'):
                [ClientCompatPatch.media(m, drop_incompat_keys=self.drop_incompat_keys)
                 for m in res.get('ranked_items', [])]
        return res

    def user_story_feed(self, user_id):
        """
        Get a user's story feed and current broadcast (if currently live)

        :param user_id:
        :return:
        """
        endpoint = 'feed/user/%(user_id)s/story/' % {'user_id': user_id}
        res = self._call_api(endpoint)
        if self.auto_patch and res.get('reel'):
            [ClientCompatPatch.media(m, drop_incompat_keys=self.drop_incompat_keys)
             for m in res.get('reel', {}).get('items', [])]
        return res

    def feed_location(self, location_id, **kwargs):
        """
        Get a location feed

        :param location_id:
        :return:
        """
        endpoint = 'feed/location/%(location_id)s/' % {'location_id': location_id}
        if kwargs:
            endpoint += '?' + compat_urllib_parse.urlencode(kwargs)
        res = self._call_api(endpoint)
        if self.auto_patch:
            if res.get('items'):
                [ClientCompatPatch.media(m, drop_incompat_keys=self.drop_incompat_keys)
                 for m in res.get('items', [])]
            if res.get('ranked_items'):
                [ClientCompatPatch.media(m, drop_incompat_keys=self.drop_incompat_keys)
                 for m in res.get('ranked_items', [])]
        return res

    def saved_feed(self, **kwargs):
        """
        Get saved photo feed

        :return:
        """
        endpoint = 'feed/saved/'
        if kwargs:
            endpoint += '?' + compat_urllib_parse.urlencode(kwargs)
        res = self._call_api(endpoint)
        if self.auto_patch:
            [ClientCompatPatch.media(m['media'], drop_incompat_keys=self.drop_incompat_keys)
             for m in res.get('items', []) if m.get('media')]
        return res