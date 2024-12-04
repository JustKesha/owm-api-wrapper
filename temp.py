from utils import convert

for speed in range(0, 150, 5):
    print(speed, 'knots,', convert.knots_to_beaufort_scale_index(speed))