from datetime import timedelta, datetime, timezone
import struct

def read_byte(db):
    return int.from_bytes(db.read(1), "little")


def read_short(db):
    return int.from_bytes(db.read(2), "little")


def read_int(db):
    data = db.read(4)
    return int.from_bytes(data, "little")


def read_long(db):
    return int.from_bytes(db.read(8), "little")


def read_single(db):
    return struct.unpack("<f", db.read(4))[0]


def read_double(db):
    return struct.unpack("<d", db.read(8))[0]


def read_bool(db):
    return struct.unpack("?", db.read(1))[0]


def read_leb128(db):
    result = 0
    shift = 0
    while True:
        byte = read_byte(db)
        result |= (byte & 0x7F) << shift
        if (byte & 0x80) == 0:
            break
        shift += 7
    return result


def read_string(db):
    present = db.read(1)
    if present == b"\x00":
        return None

    size = read_leb128(db)
    string = db.read(size)
    try:
        ret = string.decode("utf-8")
    except ValueError:
        ret = string.decode("ISO-8859-1")
    return ret


def read_int_double(db):
    fst = read_byte(db)
    item_1 = read_int(db)
    snd = read_byte(db)
    item_2 = read_double(db)
    return item_1, item_2


def read_timing(db):
    bpm = read_double(db)
    offset = read_double(db)
    inherited = read_bool(db)
    return bpm, offset, inherited


def read_datetime(db):
    ticks = read_long(db)
    start = datetime(year=1, month=1, day=1, tzinfo=timezone.utc)
    return start + timedelta(microseconds=ticks * 0.1)
