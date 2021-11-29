import sqlite3, os
print(os.listdir())

def create_database() -> None:
    """ Function for creating leaderboard.db if it doesn't exist """
    # Connect to a database
    conn = sqlite3.connect("data/leaderboard.db")
    # Create a cursor
    c = conn.cursor()
    # Command for creating leaderboard table
    c.execute("CREATE TABLE leaderboard (player_initials TEXT, player_score INTEGER)")
    conn.commit()
    conn.close()


def insert_database(player_initials = str, player_score = int) -> None:
    """ Function for inserting player's data on leaderboard.db """
    # Connect to a database
    conn = sqlite3.connect("data/leaderboard.db")
    # Create a cursor
    c = conn.cursor()
    # Command for inserting value on database
    c.execute(f"INSERT INTO leaderboard VALUES ('{player_initials}', '{player_score}')")
    conn.commit()
    conn.close()


def query_database() -> list:
    """ Function for gathering data on top 10 players on leaderboard.db """
    # Connect to a database
    conn = sqlite3.connect("data/leaderboard.db")
    # Create a cursor
    c = conn.cursor()
    c.execute("SELECT * FROM leaderboard ORDER BY player_score DESC LIMIT 10")
    players = c.fetchall()
    # print("PLAYER \t SCORE")
    # for initials, score in players:
    #     print(f"{initials} \t {score}")
    conn.commit()
    conn.close()
    return players
