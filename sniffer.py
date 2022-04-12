# https://oauth.vk.com/blank.html#access_token=72b04ff68dc24fcb49d7ec9eeecb12f7e1620a7d0db136ba1a694c57aa87e0c62ef847bea4275a750f304&expires_in=0&user_id=157817380

def get_link(link):
    return link.split('=')[1].split('&')[0]



