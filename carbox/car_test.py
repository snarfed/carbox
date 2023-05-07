from carbox.message import read_event_pair
from multiformats import CID
from base64 import b64decode
from carbox.car import read_car
from pathlib import Path


FIXTURES_DIR = Path(__file__).parent / "fixtures"

def test_read_car():
    fixture_path = FIXTURES_DIR / "donkeyballs.b64"
    post = b64decode(fixture_path.read_text())
    _, event = read_event_pair(post)
    blocks_raw = event["blocks"]
    roots, blocks = read_car(blocks_raw)

    assert [str(cid) for cid in roots] == [
        "zdpuArKcqh4Bfc5ufSWKTSS1jFRYJ47gpuxCEVXeWdMEjDpAM"
    ]
    assert len(blocks) == 10

    assert blocks[0].cid == CID.decode(
        "zdpuAx7GYAybGShxy9wvkK5eJt6a5G47tz5z5yeFcDqChfYE3"
    )
    assert blocks[0].decoded == {
        "$type": "app.bsky.feed.post",
        "createdAt": "2023-04-23T23:05:15.184Z",
        "text": "donkeyballs",
    }
