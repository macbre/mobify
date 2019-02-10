from mobify.sources import WordpressSource


def test_is_my_url():
    assert WordpressSource.is_my_url('https://blogvigdis.wordpress.com/sitemap.xml')
    assert not WordpressSource.is_my_url('https://wordpress.com')
