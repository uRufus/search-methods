import scrapy
import re
from copy import deepcopy
from urllib.parse import urlencode
from scrapy.http import HtmlResponse
from instagram.items import InstagramItem


class InstaspiderSpider(scrapy.Spider):
    name = 'instagram'
    allowed_domains = ['instagram.com']
    start_urls = ['https://www.instagram.com/']
    inst_login_link = 'https://www.instagram.com/accounts/login/ajax/'
    inst_login = 'study.ai_172'
    inst_pwd = '#PWD_INSTAGRAM_BROWSER:10:1658511046:AUVQAKmTKwZDRyvkyEu7Pzo0PUO4aGfou9cyOyQRFwPtDlxIpuaYgYA6SXCYGmP/sQ3/+zkGNM7DM4kvVIknEFpUqfC7wPOap+q9qABUqZZXKB71M3wY7krQUzHYrkkPO2HilCUNCCGb4AwVeA=='
    user_for_parse = 'young_man'

    graphql_link = 'https://www.instagram.com/graphql/query/'
    posts_hash = '69cba40317214236af40e7efa697781d'

    def parse(self, response: HtmlResponse):
        csrf = self.fetch_csrf_token(response.text)
        yield scrapy.FormRequest(
            self.inst_login_link,
            method='POST',
            callback=self.login,
            formdata={'username': self.inst_login, 'enc_password': self.inst_pwd},
            headers={'X-CSRFToken': csrf}
        )

    def login(self, response:HtmlResponse):
        j_data = response.json()
        if j_data['authenticated']:
            yield response.follow(
                f'/{self.user_for_parse}',
                callback=self.user_parsing,
                cb_kwargs={'username': self.user_for_parse}
            )

    def user_parsing(self, response:HtmlResponse, username):
        user_id = 7709057810
        variables = {'first': 12,
                     'id': user_id}

        url_posts = f'{self.graphql_link}?query_hash={self.posts_hash}&{urlencode(variables)}'
        yield response.follow(url_posts,
                              callback=self.user_posts_parse,
                              cb_kwargs={'username': username,
                                         'user_id': user_id,
                                         'variables': deepcopy(variables)})

    def user_posts_parse(self, response: HtmlResponse, username, user_id, variables):
        j_data = response.json()
        page_info = j_data.get('data').get('user').get('edge_owner_to_timeline_media').get('page_info')
        if page_info.get('has_next_page'):
            variables['after'] = page_info.get('end_cursor')
            url_posts = f'{self.graphql_link}?query_hash={self.posts_hash}&{urlencode(variables)}'
            yield response.follow(url_posts,
                                  callback=self.user_posts_parse,
                                  cb_kwargs={'username': username,
                                             'user_id': user_id,
                                             'variables': deepcopy(variables)},
                                  headers={'User-Agent' : 'Instagram 155.0.0.37.107'})
        posts = j_data.get('data').get('user').get('edge_owner_to_timeline_media').get('edges')
        for post in posts:
            item = InstagramItem(
                user_id=user_id,
                username=username,
                photo=post.get('node').get('display_url'),
                likes=post.get('node').get('edge_media_preview_like').get('count'),
                post_data=post.get('node')
            )
            yield item

    def fetch_csrf_token(self, text):
        ''' Get csrf-token for auth '''
        matched = re.search('\"csrf_token\":\"\\w+\"', text).group()
        return matched.split(':').pop().replace(r'"', '')

