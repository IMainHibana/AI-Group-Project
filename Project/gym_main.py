from contextlib import closing
from io import StringIO
from os import path
from typing import Optional
import numpy as np
import pygame

from gym import Env, spaces, utils
from gym.envs.toy_text.utils import categorical_sample

GRID = [
    "|D| |F| |D|",
    "| | | | | |",
    "| | |D| |P|",
    "| |P| | | |",
    "| | |M| |D|",
]

WINDOW_SIZE = (800, 800)


class DPEnv(Env):
    """
    Actions:
    0: south
    1: north
    2: east
    3: west
    4: pick up
    5: drop off

    2 pick up locations
    4 drop off locations

    Each state space is represented by the tuple:
    (row, col, pickup, destination)

    An observation is an integer that encodes the corresponding state
    The state tuple can then be decoded with the decode method

    Pick up locations: 0,1
    Drop off locations: 0,1,2,3

    Rewards:
    -1 per step unless other reward is triggered
    +13 for pick up
    +13 for drop off
    """

    metadata = {"render_modes": ["human", "ansi", "rgb_array"], "render_fps": 4}

    def __init__(self):
        self.desc = np.asarray(GRID, dtype="c")
        self.locs = locs = [(1, 3), (4, 2)]
        self.locs_colors = [(255, 0, 0), (0, 255, 0), (255, 255, 0), (0, 0, 255)]

        num_states = 1600
        num_rows = 5
        num_cols = 5
        max_row = num_rows-1
        max_col = num_cols-1
        self.initial_state_distrib = np.zeros(num_states)
        num_actions = 6
        self.P = {
            state: {action: [] for action in range(num_actions)}
            for state in range(num_states)
        }
        for row in range(num_rows-1):
            for col in range(num_cols-1):
                for pickup_idx in range(len(locs) + 1): # +1 for package being carried by agent
                    for dest_idx in range(len(locs)):
                        state = self.encode(row, col, pickup_idx, dest_idx)
                        if pickup_idx < 4 and pickup_idx != dest_idx:
                            self.initial_state_distrib[state] += 1
                        for action in range(num_actions):
                            # defaults
                            new_row, new_col, new_pickup_idx = row, col, pickup_idx
                            reward = (
                                -1
                            )   # default reward when there is no pickup/drop off
                            done = False
                            agent_loc = (row, col)

                            if action == 0:
                                new_row = min(row + 1, max_row)
                            elif action == 1:
                                new_row = max(row-1, 0)
                            if action == 2 and self.desc[1 + row, 2 * col + 2] == b"|":
                                new_col = min(col + 1, max_col)
                            elif action == 3 and self.desc[1 + row, 2 * col] == b"|":
                                new_col = max(col - 1, 0)
                            elif action == 4:   # pick up
                                if pickup_idx < 2 and agent_loc == locs[pickup_idx]:
                                    new_pickup_idx = 2
                            elif action == 5:   # drop off
                                if (agent_loc == locs[dest_idx]) and pickup_idx == 2:
                                    new_pickup_idx = dest_idx
                                    done = True
                                    reward = 13
                                elif (agent_loc in locs) and pickup_idx == 2:
                                    new_pickup_idx = locs.index(agent_loc)
                            new_state = self.encode(
                                new_row, new_col, new_pickup_idx, dest_idx
                            )
                            self.P[state][action].append((1.0, new_state, reward, done))
        self.initial_state_distrib /= self.initial_state_distrib.sum()
        self.action_space = spaces.Discrete(num_actions)
        self.observation_space = spaces.Discrete(num_states)

        # pygame
        self.window = None
        self.clock = None
        self.cell_size = (
            WINDOW_SIZE[0] / self.desc.shape[1],
            WINDOW_SIZE[1] / self.desc.shape[0],
        )
        self.agent_img = pygame.image.load("female.png")
        self.agent_orientation = 0
        self.package_img = pygame.image.load("package.png")
        self.dropoff_img = pygame.image.load("drop_off.jpeg")
        self.median_horiz = [pygame.image.load("gridworld_median_horiz.png"), pygame.image.load("gridworld_median_horiz.png"), pygame.image.load("gridworld_median_horiz.png")]
        self.median_vert = [pygame.image.load("gridworld_median_vert.png"), pygame.image.load("gridworld_median_vert.png"), pygame.image.load("gridworld_median_vert.png")]
        self.background_img = pygame.image.load("background.jpeg")

    def encode(self, agent_row, agent_col, package_loc, dest_idx):
        # (5) 5, 5, 4
        i = agent_row
        i *= 5
        i += agent_col
        i *= 5
        i += package_loc
        i *= 4
        i += dest_idx
        return i

    def decode(self, i):
        out = []
        out.append(i % 4)
        i = i // 4
        out.append(i % 5)
        i = i // 5
        out.append(i % 5)
        i = i // 5
        out.append(i)
        assert 0 <= i < 5
        return reversed(out)

    def step(self, a):
        transitions = self.P[self.s][a]
        i = categorical_sample([t[0] for t in transitions], self.np_random)
        p, s, r, d = transitions[i]
        self.s = s
        self.lastaction = a
        return (int(s), r, d, {"prob": p})

    def reset(
        self,
        *,
        seed: Optional[int] = None,
        return_info: bool = False,
        options: Optional[dict] = None,
    ):
        super().reset(seed=seed)
        self.s = categorical_sample(self.initial_state_distrib, self.np_random)
        self.lastaction = None
        self.agent_orientation = 0
        if not return_info:
            return int(self.s)
        else:
            return int(self.s), {"prob": 1}

    def render(self, mode="human"):
        if mode == "ansi":
            return self._render_text()
        else:
            return self._render_gui(mode)

    def _render_gui(self, mode):
        if self.window is None:
            pygame.init()
            pygame.display.set_caption("DP World")
            if mode == "human":
                self.window = pygame.display.set_mode(WINDOW_SIZE)
            else:  # "rgb_array"
                self.window = pygame.Surface(WINDOW_SIZE)
        if self.clock is None:
            self.clock = pygame.time.Clock()

        desc = self.desc

        for y in range(0, desc.shape[0]):
            for x in range(0, desc.shape[1]):
                cell = (x * self.cell_size[0], y * self.cell_size[1])
                self.window.blit(self.background_img, cell)
                if desc[y][x] == b"|" and (y == 0 or desc[y - 1][x] != b"|"):
                    self.window.blit(self.median_vert[0], cell)
                elif desc[y][x] == b"|" and (
                        y == desc.shape[0] - 1 or desc[y + 1][x] != b"|"
                ):
                    self.window.blit(self.median_vert[2], cell)
                elif desc[y][x] == b"|":
                    self.window.blit(self.median_vert[1], cell)
                elif desc[y][x] == b"-" and (x == 0 or desc[y][x - 1] != b"-"):
                    self.window.blit(self.median_horiz[0], cell)
                elif desc[y][x] == b"-" and (
                        x == desc.shape[1] - 1 or desc[y][x + 1] != b"-"
                ):
                    self.window.blit(self.median_horiz[2], cell)
                elif desc[y][x] == b"-":
                    self.window.blit(self.median_horiz[1], cell)

        for cell, color in zip(self.locs, self.locs_colors):
            color_cell = pygame.Surface(self.cell_size)
            color_cell.set_alpha(128)
            color_cell.fill(color)
            loc = self.get_surf_loc(cell)
            self.window.blit(color_cell, (loc[0], loc[1] + 10))

        agent_row, agent_col, package_idx, dest_idx = self.decode(self.s)

        if package_idx < 4:
            self.window.blit(self.package_img, self.get_surf_loc(self.locs[package_idx]))

        if self.lastaction in [0, 1, 2, 3]:
            self.agent_orientation = self.lastaction
        dest_loc = self.get_surf_loc(self.locs[dest_idx])
        agent_location = self.get_surf_loc((agent_row, agent_col))

        if dest_loc[1] <= agent_location[1]:
            self.window.blit(
                self.destination_img,
                (dest_loc[0], dest_loc[1] - self.cell_size[1] // 2),
            )
            self.window.blit(self.agent_img[self.agent_orientation], agent_location)
        else:  # change blit order for overlapping appearance
            self.window.blit(self.agent_img[self.agent_orientation], agent_location)
            self.window.blit(
                self.destination_img,
                (dest_loc[0], dest_loc[1] - self.cell_size[1] // 2),
            )

        if mode == "human":
            pygame.display.update()
            self.clock.tick(self.metadata["render_fps"])
        else:  # rgb_array
            return np.transpose(
                np.array(pygame.surfarray.pixels3d(self.window)), axes=(1, 0, 2)
            )

    def get_surf_loc(self, map_loc):
        return (map_loc[1] * 2 + 1) * self.cell_size[0], (
                map_loc[0] + 1
        ) * self.cell_size[1]

    def _render_text(self):
        desc = self.desc.copy().tolist()
        outfile = StringIO()

        out = [[c.decode("utf-8") for c in line] for line in desc]
        agent_row, agent_col, package_idx, dest_idx = self.decode(self.s)

        def ul(x):
            return "_" if x == " " else x

        if package_idx < 4:
            out[1 + agent_row][2 * agent_col + 1] = utils.colorize(
                out[1 + agent_row][2 * agent_col + 1], "yellow", highlight=True
            )
            pi, pj = self.locs[package_idx]
            out[1 + pi][2 * pj + 1] = utils.colorize(
                out[1 + pi][2 * pj + 1], "blue", bold=True
            )
        else:  # package on agent
            out[1 + agent_row][2 * agent_col + 1] = utils.colorize(
                ul(out[1 + agent_row][2 * agent_col + 1]), "green", highlight=True
            )

        di, dj = self.locs[dest_idx]
        out[1 + di][2 * dj + 1] = utils.colorize(out[1 + di][2 * dj + 1], "magenta")
        outfile.write("\n".join(["".join(row) for row in out]) + "\n")
        if self.lastaction is not None:
            outfile.write(
                f"  ({['South', 'North', 'East', 'West', 'Pickup', 'Dropoff'][self.lastaction]})\n"
            )
        else:
            outfile.write("\n")

        with closing(outfile):
            return outfile.getvalue()

    def close(self):
        if self.window is not None:
            pygame.display.quit()
            pygame.quit()


agent = DPEnv()
agent.render()



