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
            x = a1 * np.cos(theta) + c1
            y = b1 * np.sin(theta)
            return np.array([x, y, 0])

        ellipse1 = ParametricFunction(ellipse1_func, t_range=[0, 1], color=BLUE)

        # Second ellipse: YZ-plane, focus at origin
        a2, b2 = 2.5, 1.5
        c2 = np.sqrt(a2**2 - b2**2)

        def ellipse2_func(t):
            theta = 2 * PI * t
            y = a2 * np.cos(theta) + c2
            z = b2 * np.sin(theta)
            return np.array([0, y, z])

        ellipse2 = ParametricFunction(ellipse2_func, t_range=[0, 1], color=BLUE)

        # Focus: white flat dot at origin
        focus = Dot(ORIGIN, color=WHITE)

        # Red shaded circles to simulate spheres
        red_ball_1 = Circle(radius=0.3, color=RED, fill_opacity=1).move_to(ellipse1_func(0))
        red_ball_1.set_shading(0.8)
        red_ball_2 = Circle(radius=0.3, color=RED, fill_opacity=1).move_to(ellipse2_func(0))
        red_ball_2.set_shading(0.8)

        # Time tracker
        time = ValueTracker(0)

        # Motion updaters
        red_ball_1.add_updater(lambda m: m.move_to(ellipse1_func(time.get_value() % 1)))
        red_ball_2.add_updater(lambda m: m.move_to(ellipse2_func(time.get_value() % 1)))

        # Build scene
        self.play(Create(ellipse1), FadeIn(focus), run_time=2)
        self.add(red_ball_1)
        self.wait(0.5)
        self.play(Create(ellipse2), run_time=2)
        self.add(red_ball_2)
        self.wait(0.5)

        # Animate movement + camera rotation
        self.begin_ambient_camera_rotation(rate=0.1)
        self.play(time.animate.increment_value(5), run_time=15, rate_func=linear)
        self.stop_ambient_camera_rotation()

        self.wait(1)

