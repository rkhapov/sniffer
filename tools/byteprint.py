def get_bytes_str(bytes_, max_length=None):
    if isinstance(bytes_, int):
        return '0x' + hex(bytes_).lstrip('0x').upper()

    if max_length is None or len(bytes_) <= max_length:
        return ' '.join(map('{:02x}'.format, bytes_)).upper()

    return ' '.join(map('{:02x}'.format, bytes_[0:max_length])).upper() + '...'


def to_mac_address(bytes_):
    if len(bytes_) != 6:
        raise ValueError('Invalid bytes amount for mac')

    return ':'.join(map('{:02x}'.format, bytes_)).upper()


def to_hexed_int(val, length=None):
    if length is None:
        return '0x' + hex(val).lstrip('0x').upper()

    return '0x' + hex(val).lstrip('0x').zfill(length).upper()
