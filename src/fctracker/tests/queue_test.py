from fctracker.domain import QuantifiedQueue
import queue
import pytest


def test_get_full():
    qq = QuantifiedQueue()

    qq.put(5, 1)
    assert qq.get(5) == [(5, 1)]

    qq.put(6, 2)
    qq.put(7, 3)
    assert qq.get(6) == [(6, 2)]
    qq.put(8, 4)
    assert qq.get(7) == [(7, 3)]
    assert qq.get(8) == [(8, 4)]


def test_get_partial():
    qq = QuantifiedQueue()

    qq.put(10.42, 24.4988)
    qq.put(207.63, 24.5847)
    assert qq.get(207.63) == [(10.42, 24.4988), (197.21, 24.5847)]
    assert qq.get(10.42) == [(10.42, 24.5847)]
    assert qq.empty() is True


def test_get_more_than_available():
    qq = QuantifiedQueue()

    qq.put(207.63, 24.5847)

    with pytest.raises(queue.Empty) as e:
        qq.get(207.64)

    assert e.errisinstance(queue.Empty) is True


def test_print():
    qq = QuantifiedQueue()

    qq.put(10.42, 24.4988)
    qq.put(207.63, 24.5847)
    qq.get(200)
    assert f"{qq}" == "[(18.05, 24.5847)]"
    qq.put(18.05, 24.6368)
    assert f"{qq}" == "[(18.05, 24.5847), (18.05, 24.6368)]"
