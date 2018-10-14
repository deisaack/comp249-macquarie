"""
Database Model interface for the COMP249 Web Application assignment

@author: steve cassidy
"""


def position_list(db, limit=10):
    """Return a list of positions ordered by date
    db is a database connection
    return at most limit positions (default 10)

    Returns a list of tuples  (id, timestamp, owner, title, location, company, description)
    """

    row = db.execute('SELECT * from positions').fetchall()
    posts = []
    for post in row:
        obj = (post[0], post[1], post[2], post[3], post[4], post[5], post[6])
        posts.append(obj)
    return posts



def position_get(db, id):
    """Return the details of the position with the given id
    or None if there is no position with this id

    Returns a tuple (id, timestamp, owner, title, location, company, description)

    """
    post = db.execute("SELECT * FROM positions WHERE id="+id).fetchone()

    return (post[0], post[1], post[2], post[3], post[4], post[5], post[6])




def position_add(db, usernick, title, location, company, description):
    """Add a new post to the database.
    The date of the post will be the current time and date.
    Only add the record if usernick matches an existing user

    Return True if the record was added, False if not."""
