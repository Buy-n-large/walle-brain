"""Point d'entrée CLI — test interactif du cerveau WALL-E."""
from .llm import WalleBrain


def main():
    brain = WalleBrain()
    print("WALL-E Brain — tape 'quit' pour quitter, 'reset' pour effacer la mémoire\n")

    while True:
        try:
            user = input("Toi : ").strip()
        except (EOFError, KeyboardInterrupt):
            break

        if not user:
            continue
        if user.lower() == "quit":
            break
        if user.lower() == "reset":
            brain.reset()
            print("(mémoire effacée)")
            continue

        reply, commands = brain.think(user)
        print(f"WALL-E : {reply}")
        if commands:
            print(f"  → commandes : {commands}")
        print()
