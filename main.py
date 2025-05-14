from manim import *
import numpy as np

class DualEllipticOrbits(ThreeDScene):
    def construct(self):
        self.set_camera_orientation(phi=75 * DEGREES, theta=30 * DEGREES)

        # Axes
        axes = ThreeDAxes()
        self.add(axes)

        # Focus at origin: flat white dot
        focus = Dot(ORIGIN, color=WHITE)
        self.add(focus)

        # First ellipse (XY plane)
        a1, b1 = 2.5, 2
        c1 = np.sqrt(a1**2 - b1**2)

        def ellipse1_func(t):
            theta = 2 * PI * t
            x = a1 * np.cos(theta) + c1
            y = b1 * np.sin(theta)
            return np.array([x, y, 0])

        ellipse1 = ParametricFunction(ellipse1_func, t_range=[0, 1], color=BLUE)

        # Second ellipse (YZ plane)
        a2, b2 = 2.5, 1.5
        c2 = np.sqrt(a2**2 - b2**2)

        def ellipse2_func(t):
            theta = 2 * PI * t
            y = a2 * np.cos(theta) + c2
            z = b2 * np.sin(theta)
            return np.array([0, y, z])

        ellipse2 = ParametricFunction(ellipse2_func, t_range=[0, 1], color=BLUE)

        # Create smooth red spheres (higher resolution)
        ball1 = Sphere(radius=0.3, resolution=(64, 64)).set_color(RED)
        ball2 = Sphere(radius=0.3, resolution=(64, 64)).set_color(RED)

        ball1.move_to(ellipse1_func(0))
        ball2.move_to(ellipse2_func(0))

        # Time tracker
        time = ValueTracker(0)

        # Add updaters for motion
        ball1.add_updater(lambda m: m.move_to(ellipse1_func(time.get_value() % 1)))
        ball2.add_updater(lambda m: m.move_to(ellipse2_func(time.get_value() % 1)))

        # Animate
        self.play(Create(ellipse1), run_time=2)
        self.add(ball1)
        self.wait(0.5)

        self.play(Create(ellipse2), run_time=2)
        self.add(ball2)
        self.wait(0.5)

        self.begin_ambient_camera_rotation(rate=0.1)
        self.play(time.animate.increment_value(5), run_time=15, rate_func=linear)
        self.stop_ambient_camera_rotation()

        self.wait(1)

