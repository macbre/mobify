from . import MobifyTestCase
from mobify.sources import TrapFoMainSource
from mobify.sources.trap_fo import TrapFoSource


def test_is_my_url():
    assert TrapFoMainSource.is_my_url('https://trap.fo/en/the-islands-towns-and-settlements/mykines/')


class TrapFoSourceTest(MobifyTestCase):

    def test_parsing(self):
        source = TrapFoSource(
            url='https://trap.fo/en/the-islands-towns-and-settlements/mykines/',
            content=self.get_fixture('trap_fo.html')
        )

        assert source.get_title() == 'Mykines (Island)'
        assert source.get_author() == 'trap.fo'
        assert source.get_language() == 'en'

        html = source.get_html()
        print(html)  # failed assert will print the raw HTML

        assert '<h1>Mykines' in html
        assert '<p>Mykines has 16 inhabitants' in html, "Basic HTML formatting should be kept"

        assert '>church</a>' not in html, "Internal links should be removed"
        assert 'church was built in 1879' in html, "Internal links should be removed, but their content kept"
