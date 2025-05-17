from manim import *
import numpy as np
# Independent geometric parameters
a1, b1 = 2.5, 2.0   # ellipse 1 parameters
T1 = 3.0            # orbital period 1
a2, b2 = 2.0, 1.5   # ellipse 1 parameters
ball_radius = 0.2
# Animation parameters
loops = 5           # number of complete periods for particle 1
ball_resolution = (6, 12)
phi0, theta0 = 75 * DEGREES, 20 * DEGREES
camera_rotation_rate = 0.1
# Dependent parameters
c1 = np.sqrt(a1**2 - b1**2)
c2 = np.sqrt(a2**2 - b2**2)
e1 = c1 / a1
e2 = c2 / a2
T2 = T1 * (a2 / a1) ** 1.5
t_end = loops * T1
theta_f = theta0 + camera_rotation_rate * t_end * DEGREES


# Solution of the Kepler equation M = E - e * sin(E)
def E_from_M(M, e, prec=1e-6):
    E = M + e * np.sin(M)
    while abs(E - e * np.sin(E) - M) > prec:
        E = M + e * np.sin(E)
    return E


# General ellipse function
def ellipse_func(t, a, b, e, T):
    M = 2 * PI * t / T - PI
    E = E_from_M(M, e)
    return a * (e - np.cos(E)), b * np.sin(E)


# First ellipse (XY plane)
def ellipse1_func(t):
    x, y = ellipse_func(t, a1, b1, e1, T1)
    return np.array([x, y, 0])


# Second ellipse (YZ plane)
def ellipse2_func(t):
    x, y = ellipse_func(t, a2, b2, e2, T2)
    return np.array([0, x, y])


class DualEllipticOrbits(ThreeDScene):
    def construct(self):
        # 3D axes
        self.set_camera_orientation(phi=phi0, theta=theta0)
        self.add(ThreeDAxes())

        # Origin marker
        self.add(Dot(ORIGIN, color=WHITE))


        ellipse1 = ParametricFunction(ellipse1_func, t_range=[0, T1], color=BLUE)
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
        self.play(FadeIn(ball1))
        self.wait(0.5)
        self.play(Create(ellipse2), run_time=2)
        self.play(FadeIn(ball2))
        self.wait(0.5)

        self.begin_ambient_camera_rotation(rate=camera_rotation_rate)
        self.play(time.animate.increment_value(t_end), run_time=t_end, rate_func=linear)
        self.stop_ambient_camera_rotation()
        self.wait(0.5)


class DualEllipticOrbits(ThreeDScene):
    def construct(self):
        # 3D axes
        self.set_camera_orientation(phi=phi0, theta=theta0)
        self.add(ThreeDAxes())

        # Origin marker
        self.add(Dot(ORIGIN, color=WHITE))


        ellipse1 = ParametricFunction(ellipse1_func, t_range=[0, T1], color=BLUE)
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
        self.play(FadeIn(ball1))
        self.wait(0.5)
        self.play(Create(ellipse2), run_time=2)
        self.play(FadeIn(ball2))
        self.wait(0.5)

        self.begin_ambient_camera_rotation(rate=camera_rotation_rate)
        self.play(time.animate.increment_value(t_end), run_time=t_end, rate_func=linear)
        self.stop_ambient_camera_rotation()
        self.wait(0.5)

