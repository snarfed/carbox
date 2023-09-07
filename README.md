![Tests](https://github.com/jbn/car/actions/workflows/test.yaml/badge.svg)

![A Box](https://github.com/snarfed/carbox/raw/main/logo.png "A helmet for the psychonaut")

# What is this?

A basic [Content Addressable aRchive](https://ipld.io/specs/transport/car/) (CAR) v1 reader and writer. Enough to get you reading from the [ATProto](https://atproto.com/) firehose and emitting blocks from your own PDS. [More details on ATProto's CAR usage here.](https://atproto.com/specs/repository#car-file-serialization)

## Installation

```bash
pip install carbox
```

## Basic Usage

```python
from datetime import datetime
from carbox.car import Block, read_car, write_car
from carbox.message import read_event_pair
import dag_cbor

# Where websocket_msg is a message comes from the firehose.
header, event = read_event_pair(websocket_msg)
roots, blocks = read_car(event['blocks'])
records = [dag_cbor.decode(block) for block in blocks]

record = {
  '$type': 'app.bsky.feed.post',
  'text': 'Hello, world!',
  'createdAt': datetime.now().isoformat(),
}
block = Block(decoded=record)
car_bytes = write_car(block.cid, [block])
```


## Changelog

### 0.2 - 2023-09-07

Add write support via `car.write_car`. See usage example above for details.


### 0.0.1 - 2023-05-07

Initial release.


## Release instructions

Here's how to package, test, and ship a new release.

1. Run the unit tests.

    ```sh
    source [path_to_virtualenv]/bin/activate.csh
    pytest
    ```
1. Bump the version number in `pyproject.toml`. `git grep` the old version number to make sure it only appears in the changelog. Change the current changelog entry in `README.md` for this new version from _unreleased_ to the current date.
1. `git commit -am 'release vX.Y'`
1. Upload to [test.pypi.org](https://test.pypi.org/) for testing.

    ```sh
    poetry build
    setenv ver X.Y
    twine upload -r pypitest dist/carbox-$ver*
    ```
1. Install from test.pypi.org.

    ```sh
    cd /tmp
    python3 -m venv local
    source local/bin/activate.csh
    # make sure we force pip to use the uploaded version
    pip3 uninstall carbox
    pip3 install --upgrade pip
    pip3 install -i https://test.pypi.org/simple --extra-index-url https://pypi.org/simple carbox==$ver
    deactivate
    ```
1. Smoke test that the code trivially loads and runs:

    ```sh
    from carbox.car import Block, read_car, write_car

    block = Block(decoded={'foo': ['bar', 2, 3.14]})
    car_bytes = write_car([block.cid], [block])
    assert read_car(car_bytes) == ([block.cid], [block])
    ```
1. Tag the release in git. In the tag message editor, delete the generated comments at bottom, leave the first line blank (to omit the release "title" in github), put `### Notable changes` on the second line, then copy and paste this version's changelog contents below it.

    ```sh
    git tag -a v$ver --cleanup=verbatim
    git push && git push --tags
    ```
1. [Click here to draft a new release on GitHub.](https://github.com/snarfed/carbox/releases/new) Enter `vX.Y` in the _Tag version_ box. Leave _Release title_ empty. Copy `### Notable changes` and the changelog contents into the description text box.
1. Upload to [pypi.org](https://pypi.org/)!

    ```sh
    twine upload dist/carbox-$ver*
    ```
