import maya.cmds as cmds
import random
import maya.OpenMaya as om

class RandomNurbsCirclesUI:
    def __init__(self):
        self.window_name = "RandomOpenCirclesGenerator"
        self.num_circles = 10
        self.min_radius = 10
        self.max_radius = 100
        self.random_seed = 42
        self.delete_previous = True
        self.live_update = True
        self.previous_circles = []
        self.last_selected_mesh = None
        self.sections = 8

        self.create_ui()

    def create_ui(self):
        # Delete the existing window if already open
        if cmds.window(self.window_name, exists=True):
            cmds.deleteUI(self.window_name)

        # Create a new window
        self.window = cmds.window(self.window_name, title="Random Open Circles Generator", widthHeight=(300, 400))
        cmds.columnLayout(adjustableColumn=True)

        # Number of circles slider
        cmds.text(label="Number of Circles:")
        self.num_circles_slider = cmds.intSliderGrp(field=True, minValue=1, maxValue=100, value=self.num_circles, step=1, changeCommand=self.on_slider_change, dragCommand=self.on_slider_change)

        # Radius range sliders
        cmds.text(label="Minimum Radius:")
        self.min_radius_slider = cmds.floatSliderGrp(field=True, minValue=1, maxValue=1000, value=self.min_radius, step=1, changeCommand=self.on_slider_change, dragCommand=self.on_slider_change)
        cmds.text(label="Maximum Radius:")
        self.max_radius_slider = cmds.floatSliderGrp(field=True, minValue=1, maxValue=1000, value=self.max_radius, step=1, changeCommand=self.on_slider_change, dragCommand=self.on_slider_change)

        # Sections slider
        cmds.text(label="Sections:")
        self.sections_slider = cmds.intSliderGrp(field=True, minValue=4, maxValue=100, value=self.sections, step=1, changeCommand=self.on_slider_change, dragCommand=self.on_slider_change)

        # Random Seed
        cmds.text(label="Random Seed:")
        self.seed_field = cmds.intField(value=self.random_seed, changeCommand=self.on_seed_change)

        # Delete previous option
        self.delete_checkbox = cmds.checkBox(label="Delete Previous Circles", value=self.delete_previous, changeCommand=self.update_delete_option)

        # Live Update Mode Toggle
        self.live_update_checkbox = cmds.checkBox(label="Live Update Mode", value=self.live_update, changeCommand=self.update_live_mode)

        # Generate Button
        self.generate_button = cmds.button(label="Generate Circles", command=self.generate_circles)

        # Reverse Curve Button
        cmds.button(label="Reverse Curves", command=self.open_reverse_curve_options)

        # Attach Curves Button
        cmds.button(label="Attach Curves", command=self.open_attach_curves_options)

        # Curl Curves Button
        cmds.button(label="Curl Curves", command=self.open_curl_curves_options)

        # Smooth Curves Button
        cmds.button(label="Smooth Curves", command=self.open_smooth_curves_options)

        # Open/Close Curves Button
        cmds.button(label="Open/Close Curves", command=self.open_open_close_curve_options)

        # Reset Button
        cmds.button(label="Reset to Default", command=self.reset_defaults)

        # Show the UI
        cmds.showWindow(self.window)

    def open_reverse_curve_options(self, *args):
        """Open Maya's onboard Reverse Curve Options window."""
        cmds.ReverseCurveOptions()

    def open_attach_curves_options(self, *args):
        """Open Maya's onboard Attach Curves Options window."""
        cmds.AttachCurveOptions()

    def open_open_close_curve_options(self, *args):
        """Open Maya's onboard Open/Close Curve Options window."""
        cmds.evalDeferred(lambda: cmds.menu('CurvesMenu', edit=True, postMenuCommand=True))
        cmds.evalDeferred(lambda: cmds.OpenCloseCurveOptions())

    def delete_history(self, *args):
        """Delete history of the selected objects."""
        cmds.delete(ch=True)

    def open_curl_curves_options(self, *args):
        """Open Maya's onboard Curl Curves Options window."""
        cmds.CurlCurvesOptions()

    def open_smooth_curves_options(self, *args):
        """Open Maya's onboard Smooth Curves Options window."""
        cmds.SmoothCurveOptions()

    def update_delete_option(self, value):
        """Update whether previous circles should be deleted."""
        self.delete_previous = cmds.checkBox(self.delete_checkbox, query=True, value=True)

    def update_live_mode(self, value):
        """Enable or disable live update mode."""
        self.live_update = cmds.checkBox(self.live_update_checkbox, query=True, value=True)

    def reset_defaults(self, *args):
        """Reset all values to default."""
        self.num_circles = 10
        self.min_radius = 10
        self.max_radius = 100
        self.random_seed = 42
        self.delete_previous = True
        self.live_update = True
        self.sections = 8

        cmds.intSliderGrp(self.num_circles_slider, edit=True, value=self.num_circles)
        cmds.floatSliderGrp(self.min_radius_slider, edit=True, value=self.min_radius)
        cmds.floatSliderGrp(self.max_radius_slider, edit=True, value=self.max_radius)
        cmds.intSliderGrp(self.sections_slider, edit=True, value=self.sections)
        cmds.intField(self.seed_field, edit=True, value=self.random_seed)
        cmds.checkBox(self.delete_checkbox, edit=True, value=self.delete_previous)
        cmds.checkBox(self.live_update_checkbox, edit=True, value=self.live_update)

        self.generate_circles()

    def on_slider_change(self, *args):
        """Callback for sliders to handle live updates."""
        if self.live_update:
            self.generate_circles()

    def on_seed_change(self, *args):
        """Callback for the seed field to handle live updates."""
        self.random_seed = cmds.intField(self.seed_field, query=True, value=True)
        if self.live_update:
            self.generate_circles()

    def generate_circles(self, *args):
        """Generate multiple NURBS circles based on the UI settings."""
        selection = cmds.ls(selection=True, long=True)
        if not selection and not self.last_selected_mesh:
            cmds.warning("No mesh selected. Please select a mesh.")
            return

        mesh = selection[0] if selection else self.last_selected_mesh
        self.last_selected_mesh = mesh  # Store the last selected mesh

        # Ensure the selection is a mesh
        shape_node = cmds.listRelatives(mesh, shapes=True, fullPath=True)
        if not shape_node or cmds.nodeType(shape_node[0]) != "mesh":
            cmds.warning("Selected object is not a valid polygon mesh.")
            return

        # Get user parameters
        self.num_circles = cmds.intSliderGrp(self.num_circles_slider, query=True, value=True)
        self.min_radius = cmds.floatSliderGrp(self.min_radius_slider, query=True, value=True)
        self.max_radius = cmds.floatSliderGrp(self.max_radius_slider, query=True, value=True)
        self.sections = cmds.intSliderGrp(self.sections_slider, query=True, value=True)
        self.random_seed = cmds.intField(self.seed_field, query=True, value=True)
        self.delete_previous = cmds.checkBox(self.delete_checkbox, query=True, value=True)

        if self.delete_previous:
            cmds.delete(self.previous_circles)
            self.previous_circles = []

        random.seed(self.random_seed)  # Set the seed for reproducibility

        face_count = cmds.polyEvaluate(mesh, face=True)
        for _ in range(self.num_circles):
            random_face = random.randint(0, face_count - 1)
            point, normal = self.get_random_point_and_normal(mesh, random_face)
            if point is None:
                continue

            # Random radius within range
            radius = random.uniform(self.min_radius, self.max_radius)

            # Create a closed circle with specified sections
            circle = cmds.circle(normal=(0, 1, 0), radius=radius, degree=3, sections=self.sections, constructionHistory=False)[0]

            # Apply position transformation
            matrix = self.construct_rotation_matrix(normal, point)
            cmds.xform(circle, matrix=matrix, worldSpace=True)

            # Randomly rotate the circle around its local Y-axis
            random_rotation = random.uniform(0, 360)
            cmds.xform(circle, rotation=(0, random_rotation, 0), objectSpace=True, relative=True)

            # Open the circle using the closeCurve command
            cmds.closeCurve(circle, replaceOriginal=True, preserveShape=False, blendBias=0.5, constructionHistory=False)

            self.previous_circles.append(circle)

        print(f"✅ Created {self.num_circles} open NURBS circles with radius range {self.min_radius} - {self.max_radius} and {self.sections} sections each.")

    def get_random_point_and_normal(self, mesh, face_id):
        """Returns a random point on the given face and its normal."""
        sel = om.MSelectionList()
        sel.add(mesh)
        dag_path = om.MDagPath()
        sel.getDagPath(0, dag_path)
        mfn_mesh = om.MFnMesh(dag_path)
        normal = om.MVector()
        mfn_mesh.getPolygonNormal(face_id, normal, om.MSpace.kWorld)

        points = []
        face_vertices = om.MIntArray()
        mfn_mesh.getPolygonVertices(face_id, face_vertices)
        for i in range(3):  # Using a triangle for interpolation
            point = om.MPoint()
            mfn_mesh.getPoint(face_vertices[i], point, om.MSpace.kWorld)
            points.append(om.MVector(point))

        r1, r2 = random.random(), random.random()
        if r1 + r2 > 1:
            r1, r2 = 1 - r1, 1 - r2
        r3 = 1 - r1 - r2

        rand_point = (points[0] * r1) + (points[1] * r2) + (points[2] * r3)
        return rand_point, normal

    def construct_rotation_matrix(self, normal, position):
        """Returns a transformation matrix aligning Y-axis with the normal."""
        up_vector = om.MVector(0, 1, 0)
        tangent_x = (up_vector ^ normal).normal()
        tangent_y = normal.normal()
        tangent_z = (tangent_y ^ tangent_x).normal()
        return [tangent_x.x, tangent_x.y, tangent_x.z, 0, tangent_y.x, tangent_y.y, tangent_y.z, 0, tangent_z.x, tangent_z.y, tangent_z.z, 0, position.x, position.y, position.z, 1]

# Launch the UI
RandomNurbsCirclesUI()
