#!/usr/bin/env python3
"""Build the experimental 3D, per-glyph lyric scene used by blender_comp.py.

The ordinary lyric renderer uses VSE text strips.  This module deliberately
uses actual Blender font objects converted to meshes: each glyph can move in
camera depth, rotate on all three axes, squash, and bend through a
SimpleDeform modifier.  The resulting transparent scene is composited as a
scene strip over the shot edit.
"""
from __future__ import annotations

import json
import math
import pathlib


def _key(owner, path, frame, value):
    setattr(owner, path, value)
    owner.keyframe_insert(data_path=path, frame=frame)


def _material(bpy, name, metallic, roughness):
    mat = bpy.data.materials.new(name)
    mat.use_nodes = True
    nodes = mat.node_tree.nodes
    links = mat.node_tree.links
    principled = nodes.get("Principled BSDF")
    object_info = nodes.new("ShaderNodeObjectInfo")
    links.new(object_info.outputs["Color"], principled.inputs["Base Color"])
    emission = principled.inputs.get("Emission Color") or principled.inputs.get("Emission")
    if emission:
        links.new(object_info.outputs["Color"], emission)
    strength = principled.inputs.get("Emission Strength")
    if strength:
        strength.default_value = 0.22
    principled.inputs["Metallic"].default_value = metallic
    principled.inputs["Roughness"].default_value = roughness
    return mat


def _add_area_light(bpy, scene, name, location, energy, color, size):
    data = bpy.data.lights.new(name=name, type="AREA")
    data.energy = energy
    data.color = color
    data.shape = "DISK"
    data.size = size
    obj = bpy.data.objects.new(name, data)
    scene.collection.objects.link(obj)
    obj.location = location
    obj.rotation_euler = (0.0, 0.0, 0.0)
    return obj


def _iter_fcurves(action):
    if not action:
        return
    if hasattr(action, "fcurves"):
        yield from action.fcurves
        return
    for layer in action.layers:
        for strip in layer.strips:
            for bag in strip.channelbags:
                yield from bag.fcurves


def build_lyric_scene(root, motion_path, width, height, fps, total_frames):
    import bpy

    root = pathlib.Path(root)
    path = pathlib.Path(motion_path)
    if not path.is_absolute():
        path = root / path
    motion = json.loads(path.read_text(encoding="utf-8"))
    font_path = pathlib.Path(motion.get(
        "font_file", "assets/fonts/fredoka/Fredoka[wdth,wght].ttf"))
    if not font_path.is_absolute():
        font_path = root / font_path
    if not font_path.exists():
        raise FileNotFoundError(f"3D lyric font not found: {font_path}")

    scene = bpy.data.scenes.new("LyricGeometry")
    previous_scene = bpy.context.window.scene
    bpy.context.window.scene = scene
    scene.frame_start = 1
    scene.frame_end = total_frames
    scene.render.fps = int(round(fps))
    scene.render.fps_base = 1.0
    scene.render.resolution_x = width
    scene.render.resolution_y = height
    scene.render.resolution_percentage = 100
    scene.render.engine = "BLENDER_EEVEE"
    scene.render.film_transparent = True
    scene.render.image_settings.file_format = "PNG"
    scene.render.image_settings.color_mode = "RGBA"
    scene.world = bpy.data.worlds.new("LyricTransparentWorld")
    scene.world.use_nodes = True
    scene.world.node_tree.nodes["Background"].inputs["Color"].default_value = (0.008, 0.010, 0.016, 1.0)
    scene.world.node_tree.nodes["Background"].inputs["Strength"].default_value = 0.12

    # A perspective camera makes actual Z movement readable as both size and
    # foreshortening, with enough horizontal room for loose tracking.
    cam_data = bpy.data.cameras.new("LyricCamera")
    camera = bpy.data.objects.new("LyricCamera", cam_data)
    scene.collection.objects.link(camera)
    camera.location = (0.0, 0.0, 14.0)
    camera.rotation_euler = (0.0, 0.0, 0.0)
    cam_data.lens = float(motion.get("camera_lens_mm", 42.0))
    cam_data.sensor_width = 36.0
    scene.camera = camera

    _add_area_light(bpy, scene, "LyricKey", (-4.0, 3.0, 8.0), 900.0,
                    (1.0, 0.68, 0.30), 5.0)
    _add_area_light(bpy, scene, "LyricFill", (4.0, -1.0, 6.0), 650.0,
                    (0.34, 0.72, 1.0), 4.0)
    _add_area_light(bpy, scene, "LyricRim", (0.0, 4.0, 2.0), 500.0,
                    (1.0, 0.28, 0.10), 3.0)

    font = bpy.data.fonts.load(str(font_path))
    rubber_mat = _material(bpy, "LyricRubber", metallic=0.0, roughness=0.36)
    steel_mat = _material(bpy, "LyricSteel", metallic=0.62, roughness=0.24)

    scale_720 = height / 720.0
    font_size = float(motion.get("font_size_720", 44)) / 74.0 * scale_720
    baseline_px = float(motion.get("baseline_px_720", 64)) * scale_720
    tracking = float(motion.get("tracking_px_720", 8)) / 74.0 * scale_720
    word_gap = float(motion.get("word_gap_px_720", 24)) / 74.0 * scale_720
    # Camera field height at z=0.  Convert a lower-edge pixel baseline to world Y.
    field_h = 2.0 * camera.location.z * math.tan(
        0.5 * 2.0 * math.atan(cam_data.sensor_width / (2.0 * cam_data.lens))
        / (width / height))
    baseline_y = -field_h / 2.0 + baseline_px / height * field_h

    gold = (1.0, 0.62, 0.16, 1.0)
    cyan = (0.30, 0.88, 1.0, 1.0)
    dim_gold = (0.20, 0.085, 0.018, 1.0)
    dim_cyan = (0.018, 0.13, 0.18, 1.0)

    def create_glyph(name, char, rigidity):
        curve = bpy.data.curves.new(name + "Curve", type="FONT")
        curve.body = char
        curve.font = font
        curve.size = font_size
        curve.align_x = "CENTER"
        curve.align_y = "CENTER"
        curve.resolution_u = 8
        curve.extrude = 0.060 + 0.045 * rigidity
        curve.bevel_depth = 0.022 + 0.010 * (1.0 - rigidity)
        curve.bevel_resolution = 3
        obj = bpy.data.objects.new(name, curve)
        scene.collection.objects.link(obj)
        obj.data.materials.append(steel_mat if rigidity >= 0.65 else rubber_mat)
        # Conversion is the point of this renderer: after it, the glyph is
        # genuine geometry and the bend modifier deforms its outline and depth.
        for selected in bpy.context.selected_objects:
            selected.select_set(False)
        obj.select_set(True)
        bpy.context.view_layer.objects.active = obj
        bpy.ops.object.convert(target="MESH")
        basis = obj.shape_key_add(name="Basis")
        flex = obj.shape_key_add(name="RubberFlex")
        flex.slider_min = -1.5
        flex.slider_max = 1.5
        ys = [point.co.y for point in basis.data]
        ymin, ymax = min(ys), max(ys)
        span = max(0.01, ymax - ymin)
        # Bow the centre of the outline sideways and toward camera.  Animating
        # one signed value now produces a real contour deformation, without
        # SimpleDeform's singularities on narrow rounded glyphs.
        for source, target in zip(basis.data, flex.data):
            u = (source.co.y - ymin) / span
            bell = math.sin(math.pi * u)
            target.co.x += span * 0.13 * bell
            target.co.z += span * 0.11 * bell
        return obj, flex

    glyph_count = 0
    for phrase in motion["phrases"]:
        speaker = phrase.get("speaker", "Them 1")
        active = cyan if speaker == "Them 2" else gold
        dim = dim_cyan if speaker == "Them 2" else dim_gold
        phrase_on = int(phrase["on"])
        phrase_off = int(phrase["off"])
        line_start = max(0, phrase_on - 4)
        line_end = min(total_frames - 1, phrase_off + 6)

        made = []
        for wi, word in enumerate(phrase["words"]):
            rigidity = float(word.get("rigidity", 0.5))
            for gi, char in enumerate(word["text"]):
                obj, flex = create_glyph(
                    f"lyric_{phrase['id']}_{wi:02d}_{gi:02d}", char, rigidity)
                made.append((obj, flex, word, wi, gi, len(word["text"])))
                glyph_count += 1

        # Layout is measured from the chosen font geometry, with deliberately
        # roomy tracking so glyph silhouettes have space to dance independently.
        widths = [max(0.08, obj.dimensions.x) for obj, *_ in made]
        total_w = sum(widths) + tracking * max(0, len(widths) - 1)
        total_w += word_gap * max(0, len(phrase["words"]) - 1)
        cursor = -total_w / 2.0
        last_word = -1

        for glyph_index, ((obj, flex, word, wi, gi, count), glyph_w) in enumerate(zip(made, widths)):
            if last_word >= 0 and wi != last_word:
                cursor += word_gap
            base_x = cursor + glyph_w / 2.0
            cursor += glyph_w + tracking
            last_word = wi

            rigidity = float(word.get("rigidity", 0.5))
            rubber = 1.0 - rigidity
            rel = (gi - (count - 1) / 2.0) / max(1.0, (count - 1) / 2.0)
            word_on = int(word["on"])
            word_off = int(word["off"])
            lag = round(rubber * gi / max(1, count - 1) * min(6, max(0, (word_off - word_on) // 2)))
            anticipate = max(line_start, word_on - 2 + lag)
            hit = min(word_off - 1, word_on + 2 + lag)
            rebound = min(word_off - 1, hit + 4 + round(4 * rubber))
            settle = min(word_off, rebound + 5 + round(3 * rubber))

            dx = float(word.get("dx", 0.0)) / 74.0 * scale_720
            dy = float(word.get("dy", 0.0)) / 74.0 * scale_720
            dx += rel * float(word.get("spread", 0.0)) * count / 148.0 * scale_720
            split = float(word.get("split", 0.0)) / 74.0 * scale_720
            if split and abs(rel) > 0.12:
                dx += math.copysign(split, rel)
            curve_y = float(word.get("curve", 0.0)) / 74.0 * scale_720 * (1.0 - rel * rel)
            wave = float(word.get("wave", 0.0)) / 74.0 * scale_720
            wave_y = wave * math.sin(gi * 1.25)
            scatter = float(word.get("scatter", 0.0)) / 74.0 * scale_720
            cluster = (-0.8, 0.15, 0.9)[gi % 3]
            dx += cluster * scatter
            dy += (0.35 if gi % 2 else -0.2) * scatter

            base = (base_x, baseline_y, 0.0)
            obj.location = base
            obj.rotation_mode = "XYZ"
            obj.color = dim
            obj.hide_render = True
            obj.keyframe_insert(data_path="hide_render", frame=line_start)
            obj.hide_render = False
            obj.keyframe_insert(data_path="hide_render", frame=line_start + 1)
            obj.hide_render = True
            obj.keyframe_insert(data_path="hide_render", frame=line_end + 1)

            _key(obj, "color", line_start + 1, dim)
            _key(obj, "color", word_on - 1, dim)
            _key(obj, "color", hit, active)
            _key(obj, "color", word_off, tuple(v * 0.72 if i < 3 else v for i, v in enumerate(active)))

            # Anticipation retreats from camera and compresses; the syllable
            # then arrives in depth. Rubber letters overshoot individually,
            # while high-rigidity words move as a tighter block.
            _key(obj, "location", line_start + 1, base)
            _key(obj, "scale", line_start + 1, (1.0, 1.0, 1.0))
            _key(obj, "rotation_euler", line_start + 1, (0.0, 0.0, 0.0))
            _key(flex, "value", line_start + 1, 0.0)

            _key(obj, "location", anticipate,
                 (base_x - dx * 0.3, baseline_y - 0.12 - dy * 0.2, -0.35 - 0.25 * rubber))
            _key(obj, "scale", anticipate,
                 (1.08 + 0.10 * rubber, 0.78 - 0.08 * rubber, 0.82))
            _key(obj, "rotation_euler", anticipate,
                 (math.radians(-8.0 * rubber), math.radians(9.0 * rel * rubber),
                  math.radians(-2.0 * rel * rubber)))
            _key(flex, "value", anticipate, -0.35 * rel * rubber)

            sx = float(word.get("sx", 1.0))
            sy = float(word.get("sy", 1.0))
            z_hit = 0.68 + 0.95 * rubber + 0.26 * math.sin(gi * 1.7)
            _key(obj, "location", hit,
                 (base_x + dx * 1.55, baseline_y + (dy + curve_y + wave_y) * 1.45, z_hit))
            _key(obj, "scale", hit,
                 (sx * (0.90 - 0.10 * rubber), sy * (1.20 + 0.30 * rubber), 1.0 + 0.45 * rubber))
            _key(obj, "rotation_euler", hit,
                 (math.radians((13.0 + 19.0 * rubber) * math.sin(gi * 1.3)),
                  math.radians((8.0 + 24.0 * rubber) * rel),
                  math.radians(float(word.get("rotation", 0.0)) * 1.8 +
                               float(word.get("bend", 0.0)) * rel * rubber)))
            bend_amount = float(word.get("bend", 5.0 if rubber > 0.55 else 1.5))
            _key(flex, "value", hit,
                 max(-1.35, min(1.35, bend_amount / 10.0 * (0.55 + 0.85 * rubber))))

            _key(obj, "location", rebound,
                 (base_x - dx * 0.45, baseline_y - dy * 0.35 - wave_y * 0.5,
                  -0.18 - 0.30 * rubber))
            _key(obj, "scale", rebound,
                 (1.08 + 0.10 * rubber, 0.88 - 0.06 * rubber, 0.92))
            _key(obj, "rotation_euler", rebound,
                 (math.radians(-9.0 * rubber * math.sin(gi * 1.3)),
                  math.radians(-8.0 * rel * rubber), 0.0))
            _key(flex, "value", rebound, -0.45 * bend_amount / 10.0 * rubber)

            recoil_x = float(word.get("recoil_x", 0.0)) / 74.0 * scale_720
            recoil_y = float(word.get("recoil_y", 0.0)) / 74.0 * scale_720
            _key(obj, "location", settle,
                 (base_x + recoil_x, baseline_y + recoil_y, 0.0))
            _key(obj, "scale", settle, (1.0, 1.0, 1.0))
            _key(obj, "rotation_euler", settle, (0.0, 0.0, 0.0))
            _key(flex, "value", settle, 0.0)

    # Rubber movement should have organic easing; visibility must remain a cut.
    for obj in scene.objects:
        action = obj.animation_data.action if obj.animation_data else None
        for curve in _iter_fcurves(action):
            for point in curve.keyframe_points:
                if curve.data_path == "hide_render":
                    point.interpolation = "CONSTANT"
                else:
                    point.interpolation = "BEZIER"
                    point.handle_left_type = "AUTO_CLAMPED"
                    point.handle_right_type = "AUTO_CLAMPED"
    bpy.context.window.scene = previous_scene
    return scene, glyph_count
