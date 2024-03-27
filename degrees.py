import csv
import sys
from util import QueueFrontier, Node

# Define dictionaries to store data
names = {}  # Maps names to corresponding person_ids
people = {}  # Maps person_ids to person data
movies = {}  # Maps movie_ids to movie data

# Function to load data from CSV files into memory


def load_data(directory):
    """
    Load data from CSV files into memory.
    """
    # Load people data
    with open(f"{directory}/people.csv", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            people[row["id"]] = {
                "name": row["name"],
                "birth": row["birth"],
                "movies": set()
            }
            names[row["name"].lower()] = row["id"]

    # Load movies data
    with open(f"{directory}/movies.csv", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            movies[row["id"]] = {
                "title": row["title"],
                "year": row["year"],
                "stars": set()
            }

    # Load stars data
    with open(f"{directory}/stars.csv", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            people[row["person_id"]]["movies"].add(row["movie_id"])
            movies[row["movie_id"]]["stars"].add(row["person_id"])


def main():
    # Check command-line arguments
    if len(sys.argv) != 2:
        sys.exit("Usage: python degrees.py [directory]")
    directory = sys.argv[1]

    # Load data from files into memory
    print("Loading data...")
    load_data(directory)
    print("Data loaded.")

    # Get source and target person_ids
    source = person_id_for_name(input("Name: "))
    if source is None:
        sys.exit("Person not found.")
    target = person_id_for_name(input("Name: "))
    if target is None:
        sys.exit("Person not found.")

    # Find shortest path between source and target
    path = shortest_path(source, target)

    # Print the result
    if path is None:
        print("Not connected.")
    else:
        degrees = len(path) - 1
        print(f"{degrees} degrees of separation.")
        for i in range(degrees):
            person1 = people[path[i][1]]["name"]
            person2 = people[path[i + 1][1]]["name"]
            movie = movies[path[i + 1][0]]["title"]
            print(f"{i + 1}: {person1} and {person2} starred in {movie}")


def shortest_path(source, target):
    """
    Returns the shortest list of tuples (movie_id, person_id) that connect the source to the target.
    If no possible path, returns None.
    """
    # Implement breadth-first search to find shortest path
    frontier = QueueFrontier()
    frontier.add(Node(source, None, None))

    explored = set()

    while True:
        # If frontier is empty, no path exists
        if frontier.empty():
            return None

        node = frontier.remove()
        if node.state == target:
            path = []
            while node.parent is not None:
                # Append tuple (movie_id, person_id) to the path
                path.append((node.action, node.state))
                node = node.parent
            path.reverse()
            return path

        explored.add(node.state)

        # Add neighbors to frontier
        for movie_id, person_id in neighbors_for_person(node.state):
            if not frontier.contains_state(person_id) and person_id not in explored:
                child = Node(person_id, node, movie_id)
                frontier.add(child)


def person_id_for_name(name):
    """
    Returns the person_id for a given name.
    If name is ambiguous or not found, returns None.
    """
    return names.get(name.lower())


def neighbors_for_person(person_id):
    """
    Returns (movie_id, person_id) pairs for people who starred with a given person.
    """
    movie_ids = people[person_id]["movies"]
    neighbors = set()
    for movie_id in movie_ids:
        for co_star_id in movies[movie_id]["stars"]:
            neighbors.add((movie_id, co_star_id))
    return neighbors


if __name__ == "__main__":
    main()
