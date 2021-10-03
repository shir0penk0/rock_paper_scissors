import pyxel


def define_sound_and_music():
    """Define sound and music."""

    # Sound effects
    pyxel.sound(0).set(
        note="c3e3g3c4c4", tone="s", volume="4", effect=("n" * 4 + "f"), speed=7
    )
    pyxel.sound(1).set(
        note="f3 b2 f2 b1  f1 f1 f1 f1",
        tone="p",
        volume=("4" * 4 + "4321"),
        effect=("n" * 7 + "f"),
        speed=9,
    )

    melody1 = (
        "c3 c3 c3 d3 e3 r e3 r"
        + ("r" * 8)
        + "e3 e3 e3 f3 d3 r c3 r"
        + ("r" * 8)
        + "c3 c3 c3 d3 e3 r e3 r"
        + ("r" * 8)
        + "b2 b2 b2 f3 d3 r c3 r"
        + ("r" * 8)
    )

    melody2 = (
        "rrrr e3e3e3e3 d3d3c3c3 b2b2c3c3"
        + "a2a2a2a2 c3c3c3c3 d3d3d3d3 e3e3e3e3"
        + "rrrr e3e3e3e3 d3d3c3c3 b2b2c3c3"
        + "a2a2a2a2 g2g2g2g2 c3c3c3c3 g2g2a2a2"
        + "rrrr e3e3e3e3 d3d3c3c3 b2b2c3c3"
        + "a2a2a2a2 c3c3c3c3 d3d3d3d3 e3e3e3e3"
        + "f3f3f3a3 a3a3a3a3 g3g3g3b3 b3b3b3b3"
        + "b3b3b3b4 rrrr e3d3c3g3 a2g2e2d2"
    )

    # Music
    pyxel.sound(2).set(
        note=melody1 * 2 + melody2 * 2,
        tone="s",
        volume=("3"),
        effect=("nnnsffff"),
        speed=20,
    )

    harmony1 = (
        "a1 a1 a1 b1  f1 f1 c2 c2"
        "c2 c2 c2 c2  g1 g1 b1 b1" * 3
        + "f1 f1 f1 f1 f1 f1 f1 f1 g1 g1 g1 g1 g1 g1 g1 g1"
    )
    harmony2 = (
        ("f1" * 8 + "g1" * 8 + "a1" * 8 + ("c2" * 7 + "d2")) * 3 + "f1" * 16 + "g1" * 16
    )

    pyxel.sound(3).set(
        note=harmony1 * 2 + harmony2 * 2, tone="t", volume="5", effect="f", speed=20
    )
    pyxel.sound(4).set(
        note=("f0 r a4 r  f0 f0 a4 r" "f0 r a4 r   f0 f0 a4 f0"),
        tone="n",
        volume="6622 6622 6622 6426",
        effect="f",
        speed=20,
    )

    pyxel.music(0).set([], [2], [3], [4])
