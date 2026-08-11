from app.algorithms.bloom_filter import DatabaseEmailBloomFilter
from app.database.connection import get_db
from pybloom_live import ScalableBloomFilter


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
