from DataBase.bloom import DatabaseEmailBloomFilter
from DataBase.database import get_db
from pybloom_live import ScalableBloomFilter


class DatabaseEmailBloomFilter: 
    def __init__(self):
        self._filter = ScalableBloomFilter(initial_capacity=1000, error_rate=0.001)

    def refresh(self):
        """Fetch all emails from DB and insert them."""
        inserted_count = 0
        with get_db() as (conn, cursor):
            cursor.execute("SELECT email FROM Users")
            for (email,) in cursor.fetchall():
                self._filter.add(email)
                inserted_count += 1
        return inserted_count

    def might_contain(self, email):
        return email in self._filter
    

def calculate_empirical_false_positive_rate(email):
    """Measure false positives using MySQL as the source of truth.

    ``candidate_emails`` should be emails that are expected not to exist.
    The database query is intentionally used here only for measurement.
    """

    email_filter = DatabaseEmailBloomFilter()
    inserted_count = email_filter.refresh()
    false_positives = 0
    confirmed_absent = 0

    with get_db() as (conn, cursor):

        cursor.execute(
            "SELECT 1 FROM Users WHERE email = %s LIMIT 1",
            (email,),
        )
        exists_in_database = cursor.fetchone() is not None

        if not exists_in_database:
            confirmed_absent += 1
            if email_filter.might_contain(email):
                false_positives += 1

    measured_rate = (
        false_positives / confirmed_absent if confirmed_absent else 0.0
    )
    expected_rate = email_filter._filter.false_positive_probability(inserted_count)
    return false_positives, confirmed_absent, measured_rate, expected_rate


def find_user_by_email(email):
    """Use Bloom for the fast miss path, then verify with the real DB query."""
    
    email_filter = DatabaseEmailBloomFilter()
    if not email_filter.might_contain(email):
        return None

    with get_db() as (conn, cursor):
        cursor.execute(
            "SELECT email, password FROM Users WHERE email = %s LIMIT 1",
            (email,),
        )
        return cursor.fetchone()