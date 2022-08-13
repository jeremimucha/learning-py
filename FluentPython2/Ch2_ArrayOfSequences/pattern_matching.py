#!/usr/bin/env python3

# Pattern matching requires python 3.10


def handle_command(message):
    match message:
        case ["BEEPER", frequency, times]:
            print(f"BEEP: {frequency} {times}")
        case ["NECK", angle]:
            print(f"Rotate neck by {angle}")
        case ["LED", ident, intensity]:
            print(f"Adjusting LED {ident} brightness to {intensity}")
        case _:
            raise RuntimeError(f"Invalid command {message}")



metro_areas = [
    ('Tokyo', 'JP', 36.933, (35.689722, 139.691667)),
    ('Delhi NCR', 'IN', 21.935, (28.613889, 77.208889)),
    ('Mexico City', 'MX', 20.142, (19.433333, -99.133333)),
    ('New York-Newark', 'US', 20.104, (40.808611, -74.020386)),
    ('São Paulo', 'BR', 19.649, (-23.547778, -46.635833)),
]


def main():
    print(f'{"":15} | {"lattitude":>9} | {"longitude":>9}')
    for record in metro_areas:
        match record:
            case [name, _, _, (lat, lon)] if lon <= 0:
                print(f'{name:15} | {lat:9.4f} | {lon:9.4f}')
            # Same, but more precise
            case [str(name), _, _, (float(lat), float(lon)) as coord] if lon > 0:
                print(f'{name:15} | {coord[0]:9.4f} | {coord[1]:9.4f}')


if __name__ == '__main__':
    main()
