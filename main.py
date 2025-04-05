# Example file showing a circle moving on screen
import math
import sys
import pygame
import utils
from random import randrange
from particle import Particle

if len(sys.argv) > 1:
    sim = sys.argv[1]

else:
    sim = 0

# pygame setup
pygame.init()
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
clock = pygame.time.Clock()
running = True
G = utils.G
gravity = utils.gravity_vector


def two_body_simulation():
    blue_particle = Particle(screen.get_width()/2, screen.get_height()/2, 0, 0, 1000000, math.log(1000000) * 8)

    orbital_radius = blue_particle.r * 3
    orbital_speed = math.sqrt(G * blue_particle.mass / blue_particle.r) * 0.07
    red_particle = Particle(screen.get_width()/2 + orbital_radius, screen.get_height()/2, 0, orbital_speed, 10, math.log(10) * 8, "red")

    orbital_radius += red_particle.r
    orbital_speed = math.sqrt(G * red_particle.mass / red_particle.r) * 0.5
    return [blue_particle, red_particle]


def particle_simulation(num_particles, m):
    m = .2
    r = math.sqrt(m) * 20
    blue_particles = [Particle(randrange(600, 1200), randrange(1, 300), -1, -3, m, r) for _ in range(num_particles//2)]
    red_particles = [Particle(randrange(600, 1200), randrange(1, 300), -1, -3, m, r, "red") for _ in range(num_particles//2)]
    return blue_particles + red_particles


particles = two_body_simulation() if sim else particle_simulation(100, 100)
orbit = []

while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False

    screen.fill("white")

    for i in range(len(particles)):
        for j in range(i + 1, len(particles)):
            p1 = particles[i] 
            p2 = particles[j]
            if p1.collide(p2):
                p1.resolve_collision(p2)
            if sim:
                p1.apply_newtonian_gravity(p2)

    for p in particles:
        p.update()
        p.edges()
        p.draw()
        if not sim:
            p.apply_force(gravity)

    if sim:
        pygame.draw.line(screen, "green", particles[0].position, particles[1].position, 2)
        if len(orbit) >= 2:
            pygame.draw.aalines(screen, "purple", False, orbit)
        orbit.append((particles[1].position.x, particles[1].position.y))


    # flip() the display to put your work on screen
    pygame.display.flip()
    # limits FPS to 60
    # dt is delta time in seconds since last frame, used for framerate-
    # independent physics.
    dt = clock.tick(60) / 1000


pygame.quit()