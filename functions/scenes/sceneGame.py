import pygame as py

from functions.scenes.sceneBase import Scene
from functions.screen import Screen
from functions.player import Player
from functions.helper import match_case_character, get_skills
from components.skill_box import SkillBox
from components.health import Health
from constants.index import white, default_pos, chap


class GameScene(Scene):
    def __init__(self, manager):
        # Initialize clock and screen
        self.clock = py.time.Clock()
        self.screen = Screen(self.clock)
        py.display.set_caption("Game Scene")

        # Running
        self.running = True
        self._next_scene = self

        # Manager
        self.manager = manager
        self.player_picks = [self.manager.data["player1"], self.manager.data["player2"]]
        self.characters = [match_case_character(pick) for pick in self.player_picks]

        # Screen
        self.screen.fill(white)

        # Create Players
        controls = ["wasd", "arrow"]
        self.players = [
            Player(
                default_pos[i],
                (chap[char][0], chap[char][1]),
                chap[char][2],
                self.clock,
                controls[i],
                char,
            )
            for i, char in enumerate(self.characters)
        ]

        self.player_healths = [Health((50, 500)), Health((490, 500))]

        self.skill_boxes = []
        positions = [(50, 550), (190, 550), (490, 550), (630, 550)]
        keys = ["C", "V", "<", ">"]

        for i, player_pick in enumerate(self.player_picks):
            skills = get_skills(player_pick)
            for j, skill in enumerate(skills):
                self.skill_boxes.append(
                    SkillBox(positions[i * 2 + j], (keys[i * 2 + j], skill))
                )

    def handle_events(self, events):
        for e in events:
            if e.type == py.QUIT:
                self.running = False
            if e.type == py.KEYDOWN:
                if e.key == py.K_ESCAPE:
                    self.running = False
        for player in self.players:
            if player.health <= 0:
                self.running = False

    def update(self):
        dt = self.clock.tick(120) / 1000

        # Update screen
        self.screen.fill(white)

        # Update players and skill boxes
        for i, player in enumerate(self.players):
            player.action(self.screen.screen, dt)
            for j in range(2):
                self.skill_boxes[i * 2 + j].draw(
                    self.screen.screen, player.cooldown_percent[j]
                )

        # Update afterburner
        self.screen.get_AfterBurner()

        # Update health
        for health, player in zip(self.player_healths, self.players):
            health.draw(self.screen.screen, player.health)

        # Check for collisions
        for attacker_i, defender_i in [(0, 1), (1, 0)]:
            attacker = self.players[attacker_i]
            defender = self.players[defender_i]
            defender_hurt_box = defender.hurt_box()

            for i, skill in enumerate([attacker.skill1, attacker.skill2]):
                hit_box = skill.hit_box(attacker.x, attacker.y)
                if (
                    hit_box.colliderect(defender_hurt_box)
                    and skill.skill_activate
                    and not (
                        defender.skill1.skill_activate or defender.skill2.skill_activate
                    )
                ):
                    defender.lose_health(skill.hit_damage())

    def render(self):
        self.screen.flip()

    def next_scene(self):
        return self._next_scene


# player_1_1_hit_box: py.Rect = self.players[0].skill1.hit_box(
#     self.players[0].x, self.players[0].y
# )
# player_1_2_hit_box: py.Rect = self.players[0].skill2.hit_box(
#     self.players[0].x, self.players[0].y
# )
# player_2_1_hit_box: py.Rect = self.players[1].skill1.hit_box(
#     self.players[1].x, self.players[1].y
# )
# player_2_2_hit_box: py.Rect = self.players[1].skill2.hit_box(
#     self.players[1].x, self.players[1].y
# )

# if (
#     player_1_1_hit_box.colliderect(self.players[1].hurt_box())
#     and self.players[0].skill1.skill_activate
#     and not (
#         self.players[1].skill1.skill_activate
#         or self.players[1].skill2.skill_activate
#     )
# ):
#     print("Player 1 hit Player 2 with skill 1")
# if (
#     player_1_2_hit_box.colliderect(self.players[1].hurt_box())
#     and self.players[0].skill2.skill_activate
#     and not (
#         self.players[1].skill1.skill_activate
#         or self.players[1].skill2.skill_activate
#     )
# ):
#     print("Player 1 hit Player 2 with skill 2")
# if (
#     player_2_1_hit_box.colliderect(self.players[0].hurt_box())
#     and self.players[1].skill1.skill_activate
#     and not (
#         self.players[0].skill1.skill_activate
#         or self.players[0].skill1.skill_activate
#     )
# ):
#     print("Player 2 hit Player 1 with skill 1")
# if (
#     player_2_2_hit_box.colliderect(self.players[0].hurt_box())
#     and self.players[1].skill2.skill_activate
#     and not (
#         self.players[0].skill1.skill_activate
#         or self.players[0].skill1.skill_activate
#     )
# ):
#     print("Player 2 hit Player 1 with skill 2")
