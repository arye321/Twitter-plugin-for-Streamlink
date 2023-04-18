from streamlink.plugin import Plugin
from streamlink.plugin.api import validate
from streamlink.stream import HLSStream
import re
from random import randint


class Twitter(Plugin):
    url_re = re.compile(r"https?://twitter\.com/i/broadcasts/\w+")

    @classmethod
    def can_handle_url(cls, url):
        return cls.url_re.match(url) is not None

    def _get_streams(self):
        liveID = self.url.rstrip("/").rsplit("/", 1)[-1]
        headers = {
            "authorization": "Bearer AAAAAAAAAAAAAAAAAAAAANRILgAAAAAAnNwIzUejRCOuH5E6I8xnZz4puTs%3D1Zv7ttfk8LF81IUq16cHjhLTvJu4FA33AGWWjCpTnA",
            "x-guest-token": str(randint(1, 99999999)),
        }
        params = {
            "include_events": "true",
            "ids": liveID,
            "broadcastVersionMap": "",
        }
        res = self.session.http.get(
            "https://twitter.com/i/api/1.1/broadcasts/show.json",
            headers=headers,
            params=params,
        )
        jsonres = self.session.http.json(res)
        media_key = jsonres["broadcasts"][liveID]["media_key"]

        res = self.session.http.get(
            f"https://twitter.com/i/api/1.1/live_video_stream/status/{media_key}",
            headers=headers,
        )
        jsonres = self.session.http.json(res)
        m3u8 = jsonres["source"]["location"]

        # video_url = self.session.http.json(res)["data"]["video_url"]
        return HLSStream.parse_variant_playlist(self.session, m3u8)


__plugin__ = Twitter
