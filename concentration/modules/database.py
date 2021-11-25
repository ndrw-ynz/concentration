import sqlite3
    
def insert_database(player_initials = str, player_score = int) -> None:
    # Connect to a database
    conn = sqlite3.connect("leaderboard.db")
    # Create a cursor
    c = conn.cursor()
    # Command for inserting value on database
    c.execute(f"INSERT INTO leaderboard VALUES ('{player_initials}', '{player_score}')")
    conn.commit()
    conn.close()
    

def query_database() -> list:
    # Command for gathering data on top 10 players on database
    # Format result
    # Connect to a database
    conn = sqlite3.connect("leaderboard.db")
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

# query_database()