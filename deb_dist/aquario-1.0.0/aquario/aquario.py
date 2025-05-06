import os
import time
import random

# Configurações do aquário
WIDTH = 100
HEIGHT = 40
NUM_FISH = 12



# Cada shape é uma lista de linhas ASCII
FISH_SHAPES_RIGHT = [
    ["><>"],           # pequeno (1 linha)
    ["><>"],          # médio  (1 linha)
    [">((o>"],          # médio  (1 linha)
    [">((*>"],          # médio  (1 linha)
    [">(((o>"],          # médio  (1 linha)
    [">(((*>"],          # médio  (1 linha)
    ["><=>"],        # grande (1 linha)
    [                  # peixe custom (3 linhas)
        "|\\/-----\\",
        "|      o|",
        "|/\\_____/"
    ],
    ["𓆟"],
]

SCENERY = [
    {   # rocha simples
        "shape":[
            "  ___  ",
            " /   \\ ",
            "/_____\\"
        ],
        "x": 5, "y": HEIGHT - 6
    },
    {   # coral
        "shape":[
            "  |||  ",
            " {|||} ",
            "  |||  "
        ],
        "x": 30, "y": HEIGHT - 8
    },
    # ... mais objetos
]
# Gera versões espelhadas (nado para a esquerda), trocando >< e /\ 
def invert_shape(shape):
    tr = str.maketrans({'>':'<','<':'>','/':'\\','\\':'/'})
    return [line[::-1].translate(tr) for line in shape]

FISH_SHAPES_LEFT = [invert_shape(s) for s in FISH_SHAPES_RIGHT]
BUBBLE = "o"

# Inicializa peixes
fishes = []
for _ in range(NUM_FISH):
    idx = random.randrange(len(FISH_SHAPES_RIGHT))
    shape = FISH_SHAPES_RIGHT[idx]
    h = len(shape)
    w = max(len(line) for line in shape)
    fishes.append({
        "shape_idx": idx,
        "x": random.randint(1, WIDTH - w - 1),
        "y": random.randint(1, HEIGHT - h - 1),
        "dir": random.choice([-1, 1])
    })

bubbles = []

background = [[" "] * WIDTH for _ in range(HEIGHT)]
for obj in SCENERY:
    for i, line in enumerate(obj["shape"]):
        yy = obj["y"] + i
        if 0 <= yy < HEIGHT:
            for j, ch in enumerate(line):
                xx = obj["x"] + j
                if 0 <= xx < WIDTH:
                    background[yy][xx] = ch
def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")

while True:
    clear_screen()

    # Move peixes
    for f in fishes:
        shape_r = FISH_SHAPES_RIGHT[f["shape_idx"]]
        shape_l = FISH_SHAPES_LEFT[f["shape_idx"]]
        h = len(shape_r)
        w = max(len(line) for line in shape_r)

        f["x"] += f["dir"]
        if f["x"] <= 1 or f["x"] >= WIDTH - w - 1:
            f["dir"] *= -1

        if random.random() < 0.2:
            f["y"] += random.choice([-1, 1])
            f["y"] = max(1, min(HEIGHT - h - 1, f["y"]))

    # Gera bolhas
    if random.random() < 0.3:
        bubbles.append({"x": random.randint(1, WIDTH - 2), "y": HEIGHT - 2})

    # Move bolhas para cima
    bubbles = [
        {"x": b["x"], "y": b["y"] - 1}
        for b in bubbles
        if b["y"] > 1
    ]

    # Desenha aquário
    print("+" + "-" * WIDTH + "+")
    for y in range(HEIGHT):
        row = background[y].copy()

        # desenha peixes
        for f in fishes:
            shape = (FISH_SHAPES_RIGHT if f["dir"]>0 else FISH_SHAPES_LEFT)[f["shape_idx"]]
            for i, line in enumerate(shape):
                yy = f["y"] + i
                if yy == y:
                    for j, ch in enumerate(line):
                        xx = f["x"] + j
                        if 0 <= xx < WIDTH:
                            row[xx] = ch

        # desenha bolhas
        for b in bubbles:
            if b["y"] == y and 0 <= b["x"] < WIDTH:
                row[b["x"]] = BUBBLE

        print("|" + "".join(row) + "|")
    print("+" + "-" * WIDTH + "+")

    time.sleep(0.2)
