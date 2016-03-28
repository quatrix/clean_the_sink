import pytest
from itertools import tee, izip
from pprint import pprint
from sink_inspector import *

incrementaly_dirty_dl = [
    "one_glass_dl",
    "2d_dl",
    "3d_dl",
    "4d_dl",
    "lots_dl",
]

incrementaly_dirty_ll = [
    "one_glass_ll",
    "half_dirty_partially_dark",
]

dirty_sinks = [
    "half_dirty",
    "washing_dishes",
    "watering_plants",
] + incrementaly_dirty_dl + incrementaly_dirty_ll

clean_sinks = [
    "clean_dl",
    "clean_ll",
]


def pairwise(iterable):
    "s -> (s0,s1), (s1,s2), (s2, s3), ..."
    a, b = tee(iterable)
    next(b, None)
    return izip(a, b)


@pytest.fixture(scope="module")
def results():
    res = {
        f: get_dirtiness('tests/sample_files/' + f + '.jpg')
        for f in clean_sinks + dirty_sinks
    } 
    
    pprint(res)

    return res


@pytest.mark.parametrize("clean_sink", clean_sinks)
@pytest.mark.parametrize("dirty_sink", dirty_sinks)
def test_clean_sinks(results, clean_sink, dirty_sink):
    e = 'clean sink {} ({}) should be cleaner than {} ({})'.format(
        clean_sink, results[clean_sink],
        dirty_sink, results[dirty_sink],
    )

    assert results[dirty_sink] > results[clean_sink], e


incrementally_dirty_dishes = \
    list(pairwise(incrementaly_dirty_dl)) + \
    list(pairwise(incrementaly_dirty_ll))

@pytest.mark.parametrize("pair", incrementally_dirty_dishes)
def test_incremental_dirtiness(results, pair):
    e = '{} ({}) should be cleaner than {} ({})'.format(
        pair[0], results[pair[0]],
        pair[1], results[pair[1]],
    )

    assert results[pair[0]] < results[pair[1]], e
