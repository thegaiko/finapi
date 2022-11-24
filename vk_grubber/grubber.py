from auth import token

import json
import os
import requests


def get_posts(domain, posts_number):
    """
    Returns last X posts in current group

        Params:
            domain (str): domain of group
            posts_number (int): number of last posts that we want to grub

        Returns:
            result (dict): dict with name of the group and posts list
    """

    url = f'https://api.vk.com/method/wall.get?domain={domain}&count={posts_number}&access_token={token}&v=5.131'
    request = requests.get(url=url)

    if request.status_code == 200:
        result = request.json()['response']
        result['domain'] = domain

        return result


def save_posts(posts):
    """
    Saves posts to a folder

        Params:
            posts (dict): dictionary with group name and list of posts

        Returns:
            True
    """

    domain = posts['domain']

    if not os.path.exists('groups'):
        os.mkdir('groups')

    if not os.path.exists(f'groups/{domain}'):
        os.mkdir(f'groups/{domain}')

    for post in posts['items']:
        post_id = post['id']

        with open(f'groups/{domain}/{post_id}.json', 'w', encoding='utf-8') as fp:
            json.dump(post, fp)

    return True


def update():
    posts = get_posts('rhymes', 5)
    save_posts(posts)


if __name__ == '__main__':
    update()
