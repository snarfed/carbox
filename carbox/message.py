import io
import cbor2
import dag_cbor


def read_event_pair(msg: bytes):
    with io.BytesIO(msg) as fp:
        header = cbor2.load(fp)
        event = dag_cbor.decode(fp.read())
    return header, event
