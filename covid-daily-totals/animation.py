# ANIMATIONS TO MAKE
# 1. Time series daily totals, w/ circles of country flag as heuristic of total cases/daily delta/ratio?
# 2. Time series comparing Hubei, SK, Italy, Washington, New York, Spain, France, Germany
# 3. COVID time series dailies vs SARS, Ebola, H1N1, MERS
# display useful information on screen concurrently

import numpy as np
import pandas as pd
import csv
import math
import datetime
from manimlib.imports import *


class Custom(GraphScene):

    def get_total_cases(self):
        with open('data/covid_daily_totals.csv') as f:
            c = csv.reader(f)
            l = list()
            for i, r in enumerate(c):
                if i == 0:
                    continue
                l.append((i, int(r[2])))
            return l

    def get_y_max(self, y):
        count = 0
        while y > 10:
            y /= 10
            count += 1
        
        return math.ceil(y) * 10 ** count

    def get_dates(self):
        with open('data/covid_daily_totals.csv') as f:
            c = csv.reader(f)
            l = list()
            for i, r in enumerate(c):
                if i == 0:
                    continue
                l.append(
                    datetime.datetime.strptime(r[1], '%Y-%m-%d').strftime('%b %d')
                )
            return l

    CONFIG = {
        #'x_max': 20,
        #'x_labeled_nums': list(range(0, 21, 5)),
        #'y_max': 700,
        #'y_tick_frequency': 50,
        #'y_labeled_nums': list(range(0, 750, 100)),
        'x_axis_label': None,
        'y_axis_label': None,
        'graph_origin': 3 * DOWN + 5 * LEFT,
        'axes_color': WHITE,
        'camera_config': {
            'background_color': '#151231'
        }
    }

    def construct(self):
        DOT_LINE_COLOR = '#D15FEE'
        VERTICAL_LINE_COLOR = YELLOW
        DOT_COLOR = '#D44942'
        NEXT_DOT_ANIM_COLOR = YELLOW
        NUM_Y_TICKS = 10
        NUM_Y_LABELS = 5

        coords = self.get_total_cases()
        self.x_max = len(coords)
        self.y_max = 25000#self.get_y_max(coords[-1][1])
        self.x_tick_frequency = self.x_max + 1
        self.y_tick_frequency = self.y_max
        self.y_labeled_nums = list(range(0, int(self.y_max) + 1, int(self.y_max) // NUM_Y_LABELS))

        self.setup_axes()
        horiz_lines = list()
        for i in self.y_labeled_nums:
            horiz = Line(
                start=self.coords_to_point(0, i), 
                end=self.coords_to_point(self.x_max, i),
                color=GREY,
                stroke_width=1
            )
            horiz_lines.append(horiz)
            self.add(horiz)

        parent_dot = SmallDot(point=self.coords_to_point(*coords[0]), color=DOT_COLOR)
        parent_dot.generate_target()
        vln = Line(start=self.coords_to_point(coords[0][0], 0), end=parent_dot.get_bottom(), color=VERTICAL_LINE_COLOR, stroke_width=2)
        vln.generate_target()
        cnt = Integer(
            number=parent_dot.get_y()
        )
        
        self.add(vln, parent_dot, cnt)

        cnt.add_updater(lambda t: t.next_to(parent_dot, UP + RIGHT, buff=SMALL_BUFF * 1.5))

        def update_value(obj):
            obj.set_value(
                self.point_to_coords(point=(parent_dot.get_x(), parent_dot.get_y(), 0))[1]
            )

        cnt.add_updater(update_value)
        self.add(cnt)

        dates = self.get_dates()
        date_mobj = TextMobject(dates[0])
        self.add(date_mobj)
        date_mobj.add_updater(lambda t: t.next_to(vln, DOWN, buff=SMALL_BUFF))
        self.add(date_mobj)
        self.wait(1.4)
        for i in range(1, len(coords)):

            if coords[i][1] > self.y_max:
                maxes = [100000, 320000]
                cnt.remove_updater(update_value)
                self.add(cnt)
                curr_mobjs = self.get_mobjects()
                curr_dots = [mobj for mobj in curr_mobjs if type(mobj) is SmallDot]
                #print(curr_dots)
                dot_coords = [self.point_to_coords(point=[d.get_x(), d.get_y(), 0]) for d in curr_dots]
                dot_coords = [(round(x), round(y)) for x, y in dot_coords]
                vln_end_coord = self.point_to_coords(vln.get_end())
                #print(dot_coords)
                self.y_max = maxes[0]
                self.y_labeled_nums = list(range(0, int(self.y_max) + 1, int(self.y_max) // 5))
                if self.y_max < coords[i][1]:
                    self.y_max = maxes[1]
                    self.y_labeled_nums = list(range(0, int(self.y_max) + 1, int(self.y_max) // 4))
                self.y_tick_frequency = self.y_max
                self.remove(self.y_axis)

                self.setup_axes()

                new_dots = [SmallDot(point=self.coords_to_point(*coord), color=DOT_COLOR) for coord in dot_coords]
                for j, dot in enumerate(curr_dots):
                    dot.generate_target()
                    dot.target = new_dots[j]
                dot_anims = [MoveToTarget(dot) for dot in curr_dots]
                new_vln_end = self.coords_to_point(*vln_end_coord)
                vln.target = Line(
                    start=self.coords_to_point(coords[i][0], 0), 
                    end=new_vln_end, 
                    color=VERTICAL_LINE_COLOR, 
                    stroke_width=2
                )
                horiz_line_anims = list()
                if len(horiz_lines) > len(self.y_labeled_nums):
                    for idx in range(len(self.y_labeled_nums), len(horiz_lines)):
                        self.remove(horiz_lines[idx])
                    horiz_lines = horiz_lines[:len(self.y_labeled_nums)]
                    
                for idx, label in enumerate(self.y_labeled_nums):
                    if idx < len(horiz_lines):
                        horiz_lines[idx].generate_target()
                        horiz_lines[idx].target = Line(
                            start=self.coords_to_point(0, label), 
                            end=self.coords_to_point(self.x_max, label),
                            color=GREY,
                            stroke_width=1
                        )
                        horiz_line_anims.append(MoveToTarget(horiz_lines[idx]))
                    else:
                        new_horiz = Line(
                            start=self.coords_to_point(0, label), 
                            end=self.coords_to_point(self.x_max, label),
                            color=GREY,
                            stroke_width=1
                        )
                        horiz_lines.append(new_horiz)
                        horiz_line_anims.append(ShowCreation(new_horiz))

                self.play(*dot_anims, MoveToTarget(vln), *horiz_line_anims)
                cnt.add_updater(update_value)
                self.add(cnt)
                #print(curr_mobjs)


            parent_dot.target = SmallDot(
                point=self.coords_to_point(*coords[i]), 
                color=NEXT_DOT_ANIM_COLOR, 
            )
            ln = Line(
                start=parent_dot.get_center(), 
                end=parent_dot.get_center(),
                color=DOT_LINE_COLOR, 
                stroke_width=2
            )
            ln.generate_target()
            ln.target = Line(
                start=parent_dot.get_center(), 
                end=parent_dot.target.get_center(),
                color=DOT_LINE_COLOR, 
                stroke_width=2
            )
            vln.target = Line(
                start=self.coords_to_point(coords[i][0], 0), 
                end=parent_dot.target.get_bottom(), 
                color=VERTICAL_LINE_COLOR, 
                stroke_width=2
            )
            self.remove(date_mobj)
            date_mobj = TextMobject(dates[i])
            self.add(date_mobj)
            date_mobj.add_updater(lambda t: t.next_to(vln, DOWN, buff=SMALL_BUFF))
            self.add(date_mobj)
            current_dot = parent_dot.deepcopy()
            current_dot.set_color(DOT_COLOR)
            self.add(current_dot, ln)
            self.play(MoveToTarget(parent_dot), MoveToTarget(ln), MoveToTarget(vln))
            self.wait(0.4)
            self.remove(ln)
        
        self.wait(3)
