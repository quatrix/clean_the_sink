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
    "2d_2g_dl_0",
    "2d_2g_dl_1",
    "2d_2g_dl_2",
    "2d_2g_dl_3",
    "2d_2g_dl_4",
] + incrementaly_dirty_dl + incrementaly_dirty_ll

clean_sinks = [
    "clean_dl",
    "clean_ll",
    "clean2_ll",
    "clean2_dl",
]


def pairwise(iterable):
    "s -> (s0,s1), (s1,s2), (s2, s3), ..."
    a, b = tee(iterable)
    next(b, None)
    return izip(a, b)

def get_full_path(f):
    return 'tests/sample_files/' + f + '.jpg'

@pytest.fixture(scope="module")
def results():
    return {
        f: get_dirtiness(get_full_path(f))
        for f in clean_sinks + dirty_sinks
    } 


@pytest.mark.parametrize("clean_sink", clean_sinks)
@pytest.mark.parametrize("dirty_sink", dirty_sinks)
def test_clean_sinks(results, clean_sink, dirty_sink):
    e = 'clean sink {} ({}) should be cleaner than {} ({})'.format(
        clean_sink, results[clean_sink],
        dirty_sink, results[dirty_sink],
    )

    assert results[dirty_sink].score > results[clean_sink].score, e


incrementally_dirty_dishes = \
    list(pairwise(incrementaly_dirty_dl)) + \
    list(pairwise(incrementaly_dirty_ll))

@pytest.mark.parametrize("pair", incrementally_dirty_dishes)
def test_incremental_dirtiness(results, pair):
    e = '{} ({}) should be cleaner than {} ({})'.format(
        pair[0], results[pair[0]],
        pair[1], results[pair[1]],
    )

    assert results[pair[0]].score < results[pair[1]].score, e


sink_holes = [
    (87, 74, 11),
    (86, 76, 12),
    (86, 76, 13),
    (84, 78, 12),
    (84, 75, 12),
    (87, 80, 13),
    (83, 79, 8),
    (82, 80, 7),
    (84, 85, 12),
    (87, 74, 14),
    (88, 73, 15),
]

@pytest.mark.parametrize("sink_hole", sink_holes)
def test_is_sink_hole(sink_hole):
    assert is_sink_hole(*sink_hole)

sink_to_dishes = [
    ("4d_2g_dl_0", 5)
]

@pytest.mark.parametrize("expected", sink_to_dishes)
def test_expected_number_of_dishes(results, expected):
    sink, dishes = expected
    assert results[sink].dishes == dishes, sink
