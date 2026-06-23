from agent import LifeLogAgent
from memory.episodic import init_db
from memory.semantic import init_semantic_db
from memory.reflection import init_reflection_db

def main():

    # Initialize the database
    init_db()
    init_semantic_db()
    init_reflection_db()

    agent = LifeLogAgent()

    print("=" * 50)
    print("Life Log Agent")
    print("Type 'exit' to quit")
    print("=" * 50)

    while True:

        user_input = input("\nYou: ")

        if user_input.lower() == "exit":
            print("\nGoodbye!")
            break

        response = agent.chat(user_input)

        print(f"\nAssistant: {response}")
        print("----------------------------------------------------------------------------")


if __name__ == "__main__":
    main()