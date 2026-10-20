"""Run: python -m manim -pql rank_animation.py Rank2D

The final video is saved beside this script.
"""
from pathlib import Path

import numpy as np
from manim import (
    BLUE, DOWN, GREEN, ORANGE, ORIGIN, RED, RIGHT, UP, WHITE, YELLOW,
    ApplyMatrix, Create, Dot, FadeIn, FadeOut, NumberPlane, Polygon,
    Scene, Text, VGroup, Vector, config,
)


config.video_dir = str(Path(__file__).resolve().parent)


class Rank2D(Scene):
    def construct(self):
        title = Text("Geometric Meaning of Matrix Rank (2D)", font_size=32)
        title.to_edge(UP)
        self.play(FadeIn(title))

        examples = [
            (np.array([[1, 0.6], [0.2, 1]]), 2, GREEN, "plane"),
            (np.array([[1, 1.5], [0.5, 0.75]]), 1, ORANGE, "line"),
            (np.zeros((2, 2)), 0, RED, "point (origin)"),
        ]

        for matrix, rank, color, image in examples:
            # Rebuild the original objects so transformations never accumulate.
            plane = NumberPlane(
                x_range=[-3, 3, 1], y_range=[-2, 2, 1],
                x_length=6, y_length=4,
                background_line_style={"stroke_width": 1, "stroke_opacity": 0.5},
            )
            square = Polygon(
                ORIGIN, RIGHT, RIGHT + UP, UP,
                color=WHITE, fill_opacity=0.25,
            )
            basis = VGroup(
                Vector(RIGHT, color=YELLOW), Vector(UP, color=BLUE),
            )
            objects = VGroup(plane, square, basis)
            caption = Text(
                f"Rank {rank}: image = {image}", font_size=28, color=color,
            ).to_edge(DOWN)
            matrix_label = Text(
                f"A = {matrix.tolist()}", font_size=22,
            ).next_to(title, DOWN)

            self.play(Create(plane), FadeIn(square), FadeIn(basis))
            self.play(FadeIn(caption), FadeIn(matrix_label))
            self.wait(0.5)
            self.play(ApplyMatrix(matrix, objects), run_time=3)

            # A collapsed object may be invisible; mark the rank-zero image.
            marker = VGroup()
            if rank == 0:
                marker.add(Dot(ORIGIN, color=RED))
                self.play(FadeIn(marker))

            self.wait(2)
            self.play(
                FadeOut(objects), FadeOut(marker),
                FadeOut(caption), FadeOut(matrix_label),
            )

        takeaway = Text("Rank = dimension of the image", font_size=34)
        self.play(FadeIn(takeaway))
        self.wait(2)
