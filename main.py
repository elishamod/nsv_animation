from manim import *
import numpy as np

# Independent geometric parameters
a1, b1 = 2.5, 2.0   # ellipse 1 parameters
T1 = 3.0            # orbital period 1
a2, b2 = 2.0, 1.5   # ellipse 2 parameters
ball_radius = 0.2
precession_rate = 0.02  # rotations per second (i.e., per time unit)
# Animation parameters
loops = 2           # number of complete periods for particle 1
ball_resolution = (4, 8)
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


# Calculate distance between two points on the orbits at time t
def distance_at_time(t, precession=False):
    p1 = ellipse1_func(t)
    if precession:
        p2 = get_rotated_pos(t)
    else:
        p2 = ellipse2_func(t)
    return np.linalg.norm(p1 - p2)


def rotation_about_y(theta):
    return np.array([
        [np.cos(theta), 0, np.sin(theta)],
        [0, 1, 0],
        [-np.sin(theta), 0, np.cos(theta)],
    ])


def get_rotated_pos(t):
    angle = 2 * PI * precession_rate * t
    pos = ellipse2_func(t)
    rotation_matrix = rotation_about_y(angle)
    return rotation_matrix @ pos


class DualEllipticOrbitsWithLine(ThreeDScene):
    def construct(self):
        # 3D axes
        self.set_camera_orientation(phi=phi0, theta=theta0)
        axes = ThreeDAxes()
        self.add(axes)

        # Origin marker
        self.add(Dot(ORIGIN, color=WHITE))

        ellipse1 = ParametricFunction(ellipse1_func, t_range=(0.0, T1), color=BLUE)
        ellipse2 = ParametricFunction(ellipse2_func, t_range=(0.0, T2), color=GREEN)

        # Fast-rendering spheres: low resolution, solid color
        ball1 = Sphere(radius=ball_radius, resolution=ball_resolution).set_color(RED)
        ball2 = Sphere(radius=ball_radius, resolution=ball_resolution).set_color(ORANGE)
        ball1.move_to(ellipse1_func(0))
        ball2.move_to(ellipse2_func(0))

        # Create distance line connecting the balls
        line = Line3D(
            start=ball1.get_center(),
            end=ball2.get_center(),
            color=YELLOW,
            thickness=0.02
        )

        # Time tracker
        time = ValueTracker(0)
        
        # Add updaters to the balls and line
        ball1.add_updater(lambda m: m.move_to(ellipse1_func(time.get_value())))
        ball2.add_updater(lambda m: m.move_to(ellipse2_func(time.get_value())))
        
        # Connecting line
        def update_line(line):
            p1 = ellipse1_func(time.get_value())
            p2 = ellipse2_func(time.get_value())
            new_line = Line3D(start=p1, end=p2, color=YELLOW, thickness=0.02)
            line.become(new_line)
            return line
        
        # Calculate distance data for the entire animation in advance
        num_points = loops * 80  # Number of points to sample for the graph
        t_values = np.linspace(0, t_end, num_points)
        distances = [distance_at_time(t) for t in t_values]
        max_dist = max(distances) * 1.1  # Add 10% margin
        
        # Create the axes for the distance plot
        plot_width, plot_height = 4, 2.5
        distance_axes = Axes(
            x_range=[0, t_end, t_end/4],
            y_range=[0, max_dist, max_dist/4],
            x_length=plot_width,
            y_length=plot_height,
            axis_config={"include_tip": False, "color": WHITE},
        )
        
        # Add labels to the axes
        x_label = Text("Time", font_size=20).next_to(distance_axes.x_axis, DOWN, buff=0.2)
        y_label = Text("Distance", font_size=20).next_to(distance_axes.y_axis, LEFT, buff=-0.3).rotate(PI/2)
        
        # Position the plot in the upper left corner
        plot_group = VGroup(distance_axes, x_label, y_label)
        plot_group.to_corner(UL, buff=0.5)
        
        # Create a background for better visibility
        background = Rectangle(
            width=plot_width + 0.8,
            height=plot_height + 0.8,
            fill_color=BLACK,
            fill_opacity=0.7,
            stroke_width=1,
            stroke_color=WHITE
        )
        background.move_to(plot_group.get_center())
        
        # Add title to the plot
        title = Text("Distance vs Time", font_size=24)
        title.next_to(background, UP, buff=0.1)
        
        # Pre-create the full distance graph for efficiency
        graph_points = [distance_axes.coords_to_point(t, d) for t, d in zip(t_values, distances)]
        distance_graph = VMobject(color=YELLOW, stroke_width=2)
        distance_graph.set_points_as_corners(graph_points)
        
        # Create the tracking dot
        tracking_dot = Dot(color=RED)
        tracking_dot.move_to(graph_points[0])

        # Update function for the tracking dot
        def update_tracking_dot(mob, alpha):
            # Find the current time based on animation progress
            current_time = alpha * t_end
            # Find the closest point in our pre-computed values
            idx = int(alpha * (num_points - 1))
            # Update the tracking dot position
            tracking_dot.move_to(graph_points[idx])
        
        # Add all the fixed elements to the scene
        self.add_fixed_in_frame_mobjects(background, title, distance_axes, x_label, y_label)
        
        # Animate everything
        self.play(Create(ellipse1), run_time=1.5)
        self.play(FadeIn(ball1))
        self.wait(0.4)
        self.play(Create(ellipse2), run_time=1.5)
        self.play(FadeIn(ball2))
        self.wait(0.4)
        
        # Add and animate the connecting line
        self.play(FadeIn(line))
        self.wait(0.4)
        line.add_updater(update_line)
        
        # Add the distance plot elements and prepare for animation
        self.add_fixed_in_frame_mobjects(tracking_dot)
        
        # Start the main animation with the distance graph creation
        self.begin_ambient_camera_rotation(rate=camera_rotation_rate)
        
        # Create an animation for drawing the distance graph while moving the objects
        self.add_fixed_in_frame_mobjects(distance_graph)
        self.play(
            time.animate.increment_value(t_end),
            Create(distance_graph),
            UpdateFromAlphaFunc(tracking_dot, update_tracking_dot),
            run_time=t_end, 
            rate_func=linear
        )
        
        # Add the completed graph as a fixed element
        self.add_fixed_in_frame_mobjects(distance_graph)
        
        self.stop_ambient_camera_rotation()
        self.wait(0.6)


class DualEllipticOrbitsWithPrecession(ThreeDScene):
    def construct(self):
        self.set_camera_orientation(phi=phi0, theta=theta0)
        axes = ThreeDAxes()
        self.add(axes)
        self.add(Dot(ORIGIN, color=WHITE))

        # Time tracker
        time = ValueTracker(0)

        # First orbit: static
        ellipse1 = ParametricFunction(ellipse1_func, t_range=[0, T1], color=BLUE)
        ball1 = Sphere(radius=ball_radius, resolution=ball_resolution).set_color(RED)
        ball1.move_to(ellipse1_func(0))
        ball1.add_updater(lambda m: m.move_to(ellipse1_func(time.get_value())))

        # Second orbit: rotating ellipse
        base_orbit = ParametricFunction(ellipse2_func, t_range=[0, T2], color=GREEN)
        orbit_path = base_orbit.copy()

        def update_orbit_path(mob):
            angle = 2 * PI * precession_rate * time.get_value()
            rotated = base_orbit.copy()
            rotated.rotate(angle, axis=Y_AXIS, about_point=ORIGIN)
            mob.become(rotated)

        orbit_path.add_updater(update_orbit_path)


        # Moving ball on the rotating second orbit
        ball2 = Sphere(radius=ball_radius, resolution=ball_resolution).set_color(ORANGE)

        ball2.move_to(get_rotated_pos(0))
        ball2.add_updater(lambda m: m.move_to(get_rotated_pos(time.get_value())))

        # Connecting line
        line = Line3D(start=ball1.get_center(), end=ball2.get_center(), color=YELLOW, thickness=0.02)
        def update_line(line):
            p1 = ellipse1_func(time.get_value())
            p2 = get_rotated_pos(time.get_value())
            new_line = Line3D(start=p1, end=p2, color=YELLOW, thickness=0.02)
            line.become(new_line)
            return line

        # Calculate distance data for the entire animation in advance
        num_points = loops * 80  # Number of points to sample for the graph
        t_values = np.linspace(0, t_end, num_points)
        distances = [distance_at_time(t, precession=True) for t in t_values]
        max_dist = max(distances) * 1.1  # Add 10% margin
        
        # Create the axes for the distance plot
        plot_width, plot_height = 4, 2.5
        distance_axes = Axes(
            x_range=[0, t_end, t_end/4],
            y_range=[0, max_dist, max_dist/4],
            x_length=plot_width,
            y_length=plot_height,
            axis_config={"include_tip": False, "color": WHITE},
        )
        
        # Add labels to the axes
        x_label = Text("Time", font_size=20).next_to(distance_axes.x_axis, DOWN, buff=0.2)
        y_label = Text("Distance", font_size=20).next_to(distance_axes.y_axis, LEFT, buff=-0.3).rotate(PI/2)
        
        # Position the plot in the upper left corner
        plot_group = VGroup(distance_axes, x_label, y_label)
        plot_group.to_corner(UL, buff=0.5)
        
        # Create a background for better visibility
        background = Rectangle(
            width=plot_width + 0.8,
            height=plot_height + 0.8,
            fill_color=BLACK,
            fill_opacity=0.7,
            stroke_width=1,
            stroke_color=WHITE
        )
        background.move_to(plot_group.get_center())
        
        # Add title to the plot
        title = Text("Distance vs Time", font_size=24)
        title.next_to(background, UP, buff=0.1)
        
        # Pre-create the full distance graph for efficiency
        graph_points = [distance_axes.coords_to_point(t, d) for t, d in zip(t_values, distances)]
        distance_graph = VMobject(color=YELLOW, stroke_width=2)
        distance_graph.set_points_as_corners(graph_points)
        
        # Create the tracking dot
        tracking_dot = Dot(color=RED)
        tracking_dot.move_to(graph_points[0])

        # Update function for the tracking dot
        def update_tracking_dot(mob, alpha):
            # Find the current time based on animation progress
            current_time = alpha * t_end
            # Find the closest point in our pre-computed values
            idx = int(alpha * (num_points - 1))
            # Update the tracking dot position
            tracking_dot.move_to(graph_points[idx])
        
        # Add all the fixed elements to the scene
        self.add_fixed_in_frame_mobjects(background, title, distance_axes, x_label, y_label)

        self.add(ball1, ball2, ellipse1, orbit_path, line)
        self.wait(0.8)
        # self.play(FadeIn(line))
        line.add_updater(update_line)

        # Add the distance plot elements and prepare for animation
        self.add_fixed_in_frame_mobjects(tracking_dot)

        self.begin_ambient_camera_rotation(rate=camera_rotation_rate)
        
        # Create an animation for drawing the distance graph while moving the objects
        self.add_fixed_in_frame_mobjects(distance_graph)
        self.play(
            time.animate.increment_value(t_end),
            Create(distance_graph),
            UpdateFromAlphaFunc(tracking_dot, update_tracking_dot),
            run_time=t_end, 
            rate_func=linear
        )
        
        # Add the completed graph as a fixed element
        self.add_fixed_in_frame_mobjects(distance_graph)

        self.stop_ambient_camera_rotation()
        self.wait(0.6)

