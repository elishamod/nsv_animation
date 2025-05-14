from manim import *
import numpy as np

class DualEllipticOrbits(ThreeDScene):
    def construct(self):
        # Independent parameters
        a1, b1 = 2.5, 2     # ellipse 1 parameters
        T1 = 2.5            # orbital period 1
        a2, b2 = 2.0, 1.5   # ellipse 1 parameters
        loops1 = 4          # number of complete periods for particle 1
        ball_radius = 0.2
        # ball_resolution = (12, 24)
        ball_resolution = (6, 12)

        # Dependent parameters
        c1 = np.sqrt(a1**2 - b1**2)
        c2 = np.sqrt(a2**2 - b2**2)
        e1 = c1 / a1
        e2 = c2 / a2
        T2 = T1 * (a2 / a1) ** 1.5

        # 3D axes
        self.set_camera_orientation(phi=75 * DEGREES, theta=20 * DEGREES)
        self.add(ThreeDAxes())

        # Origin marker
        self.add(Dot(ORIGIN, color=WHITE))

        # Approximate solution of the Kepler equation (for small eccentricity)
        def E_from_x(x, e):
            E = x - e * np.sin(x) + e ** 2 * 0.5 * np.sin(2 * x)
            return E

        # First ellipse (XY plane)
        def ellipse1_func(t):
            x = 2 * PI * t / T1
            E = E_from_x(x, e1)
            return np.array([a1 * np.cos(E) + c1, b1 * np.sin(E), 0])

        ellipse1 = ParametricFunction(ellipse1_func, t_range=[0, T1], color=BLUE)

        # Second ellipse (YZ plane)
        def ellipse2_func(t):
            x = 2 * PI * t / T2
            E = E_from_x(x, e2)
            return np.array([0, a2 * np.cos(E) + c2, b2 * np.sin(E)])

        ellipse2 = ParametricFunction(ellipse2_func, t_range=[0, T2], color=GREEN)

        # Fast-rendering spheres: low resolution, solid color
        ball1 = Sphere(radius=ball_radius, resolution=ball_resolution).set_color(RED)
        ball2 = Sphere(radius=ball_radius, resolution=ball_resolution).set_color(ORANGE)
        ball1.move_to(ellipse1_func(0))
        ball2.move_to(ellipse2_func(0))

        # Time tracker
        time = ValueTracker(0)
        ball1.add_updater(lambda m: m.move_to(ellipse1_func(time.get_value())))
        ball2.add_updater(lambda m: m.move_to(ellipse2_func(time.get_value())))

        # Animate everything
        self.play(Create(ellipse1), run_time=2)
        # self.add(ball1)
        self.play(FadeIn(ball1))
        self.wait(0.5)
        self.play(Create(ellipse2), run_time=2)
        self.play(FadeIn(ball2))
        self.wait(0.5)

        self.begin_ambient_camera_rotation(rate=0.05)
        t_end = loops1 * T1
        self.play(time.animate.increment_value(t_end), run_time=t_end, rate_func=linear)
        self.stop_ambient_camera_rotation()
        self.wait(0.5)

