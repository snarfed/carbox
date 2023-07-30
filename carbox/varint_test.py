import io
import carbox.varint as varint


def test_read_uvarint():
    test_data = b"\x8E\x02\x03"  # Represents the uvarint values 270, 3

    buf = io.BufferedReader(io.BytesIO(test_data))

    buf_res_1 = varint.read_varint_from_reader(buf)
    assert buf_res_1 == 270

    buf_res_2 = varint.read_varint_from_reader(buf)
    assert buf_res_2 == 3

    bytes_res_1, offset1 = varint.read_varint_from_bytes(test_data)
    assert bytes_res_1 == buf_res_1

    bytes_res_2, offset2 = varint.read_varint_from_bytes(test_data, offset1)
    assert bytes_res_2 == buf_res_2
    assert offset2 == len(test_data)

    offset1 = varint.burn_varint_bytes(test_data, 0)
    offset2 = varint.burn_varint_bytes(test_data, offset1)
    assert offset2 == len(test_data)


def test_write_uvarint():
    writer = io.BufferedWriter(io.BytesIO())
    varint.write_varint_to_writer(270, writer)
    varint.write_varint_to_writer(3, writer)
    writer.flush()
    assert writer.raw.getvalue() == b"\x8E\x02\x03"  # uvarint values 270, 3
