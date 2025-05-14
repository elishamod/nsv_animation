from manim import *
import numpy as np


class DualEllipticOrbits(ThreeDScene):
    def construct(self):
        self.set_camera_orientation(phi=75 * DEGREES, theta=30 * DEGREES)

        # Axes
        axes = ThreeDAxes()
        self.add(axes)

        # First ellipse: XY-plane, focus at origin
        a1, b1 = 2.5, 2
        c1 = np.sqrt(a1**2 - b1**2)

        def ellipse1_func(t):
            theta = 2 * PI * t
            x = a1 * np.cos(theta) + c1  # center at (c1, 0)
            y = b1 * np.sin(theta)
            return np.array([x, y, 0])

        ellipse1 = ParametricFunction(ellipse1_func, t_range=[0, 1], color=BLUE)
        dot1 = Dot(ellipse1_func(0), color=RED)
        focus1 = Dot(ORIGIN, color=WHITE)

        # Second ellipse: YZ-plane, focus at origin
        a2, b2 = 2.5, 1.5
        c2 = np.sqrt(a2**2 - b2**2)

        def ellipse2_func(t):
            theta = 2 * PI * t
            y = a2 * np.cos(theta) + c2  # center at (0, c2)
            z = b2 * np.sin(theta)
            return np.array([0, y, z])

        ellipse2 = ParametricFunction(ellipse2_func, t_range=[0, 1], color=BLUE)
        dot2 = Dot(ellipse2_func(0), color=RED)

        # Track time
        time_tracker = ValueTracker(0)

        # Add updaters
        dot1.add_updater(lambda m: m.move_to(ellipse1_func(time_tracker.get_value() % 1)))
        dot2.add_updater(lambda m: m.move_to(ellipse2_func(time_tracker.get_value() % 1)))

        # Display ellipses
        self.play(Create(ellipse1), FadeIn(focus1), run_time=2)
        self.play(FadeIn(dot1), run_time=0.5)
        self.wait(0.5)
        self.play(Create(ellipse2), run_time=2)
        self.play(FadeIn(dot2), run_time=0.5)
        self.wait(0.5)

        # Animate motion and grow second ellipse mid-way

        self.play(time_tracker.animate.increment_value(5), run_time=15, rate_func=linear)

