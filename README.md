![Tests](https://github.com/jbn/car/actions/workflows/test.yaml/badge.svg)

![A Box](./logo.png "A helmet for the psychonaut")

# What is this?

A primative [Content Addressable aRchive](https://ipld.io/specs/transport/car/)
reader. Enough to get you reading from the [ATP](https://atproto.com/) firehose.

## Installation

```bash
pip install carbox
```

## Basic Usage

```python
import carbox


# Where websocket_msg is a message comes from the firehose.
header, event = car.read_event_pair(websocket_msg)
roots, blocks = car.read_car(event['blocks']
```

