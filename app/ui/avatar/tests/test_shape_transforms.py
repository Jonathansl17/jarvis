"""Regression tests for the shared geometric transforms."""

import unittest

from app.ui.avatar.shape_transforms import scaled_ellipse, tilt_to_dx, translate_shapes
from app.ui.avatar.shapes import Ellipse, Line, Polygon


class ScaledEllipseTests(unittest.TestCase):
    def test_uniform_scale_keeps_the_center(self) -> None:
        base = Ellipse((0, 0, 100, 100))
        scaled = scaled_ellipse(base, 2.0)
        self.assertEqual(scaled.box, (-50, -50, 150, 150))

    def test_independent_axis_scale_only_stretches_that_axis(self) -> None:
        base = Ellipse((0, 0, 100, 200))
        scaled = scaled_ellipse(base, 1.0, 1.5)
        self.assertEqual(scaled.box, (0, -50, 100, 250))


class TranslateShapesTests(unittest.TestCase):
    def test_translates_every_shape_kind(self) -> None:
        shapes = (
            Ellipse((0, 0, 10, 10), fill="#fff"),
            Polygon(((0, 0), (10, 0), (5, 10)), fill="#fff"),
            Line(((0, 0), (10, 10)), fill="#fff"),
        )
        moved = translate_shapes(shapes, dy=5, dx=3)
        self.assertEqual(moved[0].box, (3, 5, 13, 15))
        self.assertEqual(moved[1].points, ((3, 5), (13, 5), (8, 15)))
        self.assertEqual(moved[2].points, ((3, 5), (13, 15)))


class TiltToDxTests(unittest.TestCase):
    def test_zero_tilt_is_zero_shift(self) -> None:
        self.assertEqual(tilt_to_dx(0), 0)

    def test_positive_tilt_shifts_right(self) -> None:
        self.assertGreater(tilt_to_dx(4), 0)

    def test_negative_tilt_shifts_left(self) -> None:
        self.assertLess(tilt_to_dx(-4), 0)


if __name__ == "__main__":
    unittest.main()
