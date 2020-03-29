from PIL import Image, ImageDraw


def get_color(i):
    if i % 3 == 0:
        return (0, 255, 0)
    elif i % 3 == 1:
        return (255, 0, 255)
    elif i % 3 == 2:
        return (0, 0, 255)


def project_pts(pts, lambdaf):
    new_pts = []
    for pt in pts:
        new_pt = (lambdaf(pt[0], pt[2]), lambdaf(pt[1], pt[2]), pt[2])
        new_pts.append(new_pt)
    return new_pts


def draw_line_projection(line, fill, width):
    devidel = lambda x,y: x / y
    new_line = project_pts(line, devidel)
    proj = [new_line[i][0:2] for i in range(len(new_line))]
    draw.line(proj, fill=fill, width=width)


def de_boor(k: int, x: int, t, c, p: int, draw):
    """Evaluates S(x).
    Arguments
    ---------
    k: Index of knot interval that contains x.
    x: Position.
    t: Array of knot positions, needs to be padded as described above.
    c: Array of control points.
    p: Degree of B-spline.
    """
    c = list(map(list, c))
    d = [c[j + k - p] for j in range(0, p+1)]

    add = lambda x,y: x + y

    line = []
    for r in range(1, p+1):
        if len(line) > 1:
            draw_line_projection(tuple(line), fill=get_color(r), width=2)
            line = []
        for j in range(p, r-1, -1):
            alpha = (x - t[j+k-p]) / (t[j+1+k-r] - t[j+k-p])
            a = list(map(lambda x: x * (1.0 - alpha), d[j-1]))
            b = list(map(lambda x: x * alpha, d[j]))
            d[j] = list(map(add, a, b))
            line.append(tuple(d[j]))
    assert (len(line) == 1)
    curve.append(tuple(line[0]))
    return d[p]


if __name__ == '__main__':
    #x, y, weight
    width = 500
    height = 500

    curve = []

    control_points = (
        (50,  150,  1/10),
        (150, 400, 1/10),
        (350, 450, 1/10),
        (450, 150, 7/10),
        (250, 100, 7/10),
    )

    p = 4
    knot_vector = [0, 0, 0, 0, 0, 1, 1, 1, 1, 1]
    knot_vector_cropped = [knot_vector[j] for j in range(p, len(knot_vector) - p)]

    steps_count = 100

    x_start = 0
    x_end = 1
    step_len = (x_end - x_start) / steps_count

    images = []

    for step_num in range(steps_count):
        im = Image.new('RGB', (width, height), (128, 128, 128))
        draw = ImageDraw.Draw(im)

        proj_control_points = [control_points[i][0:2] for i in range(len(control_points))]
        draw.line(proj_control_points, fill=(255, 255, 0), width=2)

        x_cur = x_start + step_num * step_len
        k = p - 1

        for knot_point in knot_vector_cropped[1:len(knot_vector_cropped)]:
            k += 1
            if knot_point >= x_cur:
                break
            debug_line = 1

        mull = lambda x, y: x * y
        new_control_points = project_pts(control_points, mull)
        de_boor(k, x_cur, knot_vector, new_control_points, p, draw)
        draw_line_projection(tuple(curve), fill=(255, 0, 0), width=2)

        print(step_num)
        images.append(im)

    images[0].save('de_boor.gif', save_all=True, append_images=images, optimize=False, duration=50, loop=0)
