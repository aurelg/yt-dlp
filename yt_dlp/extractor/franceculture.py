from .common import InfoExtractor
from ..utils import int_or_none, parse_duration, unified_strdate


class FranceCultureIE(InfoExtractor):
    _VALID_URL = r'https?://(?:www\.)?radiofrance\.fr/franceculture/podcasts/(?:[^?#]+/)?(?P<display_id>[^?#]+)-(?P<id>\d+)($|[?#])'
    _TESTS = [
        {
            'url': 'https://www.radiofrance.fr/franceculture/podcasts/science-en-questions/la-physique-d-einstein-aiderait-elle-a-comprendre-le-cerveau-8440487',
            'info_dict': {
                'id': '8440487',
                'display_id': 'la-physique-d-einstein-aiderait-elle-a-comprendre-le-cerveau',
                'ext': 'mp3',
                'title': 'La physique d’Einstein aiderait-elle à comprendre le cerveau ?',
                'description': 'Existerait-il un pont conceptuel entre la physique de l’espace-temps et les neurosciences ?',
                'thumbnail': 'https://cdn.radiofrance.fr/s3/cruiser-production/2022/05/d184e7a3-4827-4494-bf94-04ed7b120db4/1200x630_gettyimages-200171095-001.jpg',
                'upload_date': '20220514',
                'duration': 2750,
            },
        },
    ]

    def _real_extract(self, url):
        video_id, display_id = self._match_valid_url(url).group('id', 'display_id')
        webpage = self._download_webpage(url, display_id)

        # _search_json_ld doesn't correctly handle this. See https://github.com/yt-dlp/yt-dlp/pull/3874#discussion_r891903846
        video_data = self._search_json('', webpage, 'audio data', display_id, contains_pattern=r'\s*"@type"\s*:\s*"AudioObject"\s*.+')

        return {
            'id': video_id,
            'display_id': display_id,
            'url': video_data['contentUrl'],
            'ext': video_data.get('encodingFormat'),
            'vcodec': 'none' if video_data.get('encodingFormat') == 'mp3' else None,
            'duration': parse_duration(video_data.get('duration')),
            'title': self._html_search_regex(r'(?s)<h1[^>]*itemprop="[^"]*name[^"]*"[^>]*>(.+?)</h1>',
                                             webpage, 'title', default=self._og_search_title(webpage)),
            'description': self._html_search_regex(
                r'(?s)<meta name="description"\s*content="([^"]+)', webpage, 'description', default=None),
            'thumbnail': self._og_search_thumbnail(webpage),
            'uploader': self._html_search_regex(
                r'(?s)<span class="author">(.*?)</span>', webpage, 'uploader', default=None),
            'upload_date': unified_strdate(self._search_regex(
                r'"datePublished"\s*:\s*"([^"]+)', webpage, 'timestamp', fatal=False))
        }
