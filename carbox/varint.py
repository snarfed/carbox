"""IPLD CAR LEB128 varint decoding/encoding.

https://ipld.io/specs/transport/car/carv1/#format-description
https://en.wikipedia.org/wiki/LEB128
"""
import io
from typing import Tuple
from carbox.jit import jit


def read_varint_from_reader(reader: io.BufferedReader) -> int:
    shift = 0
    result = 0
    while True:
        b = reader.read(1)
        if not b:
            raise EOFError("Unexpected EOF")

        byte = b[0]
        result |= (byte & 0x7F) << shift
        if byte & 0x80 == 0:
            break
        shift += 7

    return result


def write_varint_to_writer(val: int, writer: io.BufferedWriter):
    while True:
        byte = val & 0x7f
        val = val >> 7
        if val != 0:
            byte |= 0x80
        writer.write(bytes([byte]))
        if val == 0:
            break


@jit(nopython=True)
def read_varint_from_bytes(data: bytes, offset: int = 0) -> Tuple[int, int]:
    result, offset = read_varint_from_bytes_no_throw(data, offset)
    if result == -1:
        raise EOFError("Unexpected EOF while reading uvarint")
    return result, offset


@jit(nopython=True, inline="always")
def read_varint_from_bytes_no_throw(data: bytes, offset: int = 0) -> Tuple[int, int]:
    # TODO: guard against BigInt?
    shift = 0
    result = 0
    while True:
        if offset >= len(data):
            return -1, offset

        byte = data[offset]
        result |= (byte & 0x7F) << shift
        offset += 1

        if byte & 0x80 == 0:
            break
        shift += 7

    return result, offset


@jit(nopython=True, inline="always")
def burn_varint_bytes(data: bytes, offset: int = 0) -> int:
    while True:
        if offset >= len(data):
            return -1

        byte = data[offset]
        offset += 1

        if byte & 0x80 == 0:
            break

    return offset
