import sqlite3
from random import choice, randint

from constants import (
    claim_names,
    claim_status,
    random_date_last_90_days,
)
from constants import (
    table_name as table,
)

# Table Dropping Code


def drop_table():
    conn = sqlite3.connect("new_database/claims.db")
    cursor = conn.cursor()
    cursor.execute("drop table claims")
    conn.commit()
    conn.close()
    return "Table Dropped Successfully..."


class Database:
    def __init__(self):
        self.conn = sqlite3.connect("new_database/claims.db")
        self.cursor = self.conn.cursor()
        self.create_table("claims_basic")

    def create_table(self, table_name):
        """
        Creates a Table in Database if not Exists
        """
        create_table_query = f"""
        CREATE TABLE IF NOT EXISTS {table_name} (
            ClaimId INTEGER PRIMARY KEY AUTOINCREMENT,
            ClaimName TEXT NOT NULL,
            ClaimAmount REAL NOT NULL,
            ClaimStatus TEXT NOT NULL,
            ClaimDate DATE NOT NULL
        )
        """
        self.cursor.execute(create_table_query)
        self.conn.commit()

    def get_claims(self, claim_id):
        """
        Fetches Claim Data from Database based on ClaimId
        """
        query = "SELECT * FROM claims_basic WHERE ClaimId = ?"
        self.cursor.execute(query, (claim_id,))
        result = self.cursor.fetchone()
        return result

    def add_claim(self, claim_data):
        """
        Adds a New Claim Record to Database
        """
        insert_query = """
        INSERT INTO claims_basic (ClaimName, ClaimAmount, ClaimStatus, ClaimDate)
        VALUES (?, ?, ?, ?)
        """
        self.cursor.execute(
            insert_query,
            (
                claim_data.ClaimName,
                claim_data.ClaimAmount,
                claim_data.ClaimStatus.value,
                claim_data.ClaimDate.isoformat(),
            ),
        )
        self.conn.commit()
        return self.cursor.lastrowid

    def update_claim(self, claim_id, claim_status):
        """
        Updates the Claim status of Existing Claim Record in DB
        """
        update_query = """
        UPDATE claims_basic
        SET claimStatus = ?
        WHERE claimId = ?
        """
        self.cursor.execute(update_query, (claim_id, claim_status))
        self.conn.commit()

    def delete_claim(self, claim_id):
        """
        Deletes a Claim Record from the Database
        """
        delete_query = f"""
        DELETE FROM claims_basic
        where claimId = {claim_id}
        """
        self.cursor.execute(delete_query)
        self.conn.commit()

    def get_latest_claims(self):
        latest_claim = f"""
        SELECT * FROM {table} where ClaimID IN (
        SELECT MAX(ClaimID) from {table}
        )
        """
        result = self.cursor.execute(latest_claim)
        return result.fetchone()

    def get_latest_claims_updated(self):
        latest_claim = f"""
        SELECT * FROM {table} ORDER BY ClaimAuditTime DESC
        LIMIT 1
        """
        result = self.cursor.execute(latest_claim)
        return result.fetchone()

    def get_total_claims(self):
        total_claims = f"""
        SELECT COUNT(*) FROM {table}
        """
        total_sum_claims = f"""
        SELECT SUM(claimAmount) from {table}
        """
        total_claims = self.cursor.execute(total_claims)
        total_claims = total_claims.fetchone()
        total_sum_claims = self.cursor.execute(total_sum_claims)
        total_sum_claims = total_sum_claims.fetchone()
        return total_claims[0], total_sum_claims[0]

    def get_all_claimIds(self):
        all_claims = f"""
        SELECT claimId from {table}
        """
        all_claims = self.cursor.execute(all_claims)
        return all_claims.fetchall()

    def close_connection(self):
        self.conn.close()


def random_data_generator(n):
    # Creating Connection and Cursor
    conn = sqlite3.connect("database/claims.db")
    cursor = conn.cursor()

    create_table = """
    CREATE TABLE IF NOT EXISTS claims_basic (
        ClaimId INTEGER PRIMARY KEY AUTOINCREMENT,
        ClaimName TEXT NOT NULL,
        ClaimAmount REAL NOT NULL,
        ClaimStatus TEXT NOT NULL,
        ClaimDate DATE NOT NULL
    )
    """

    result = cursor.execute(create_table)  # Table Already Created so No Response

    # print(result.fetchall())

    for _ in range(n):
        insert_data = """
        INSERT INTO claims_basic (ClaimName, ClaimAmount, ClaimStatus, ClaimDate)
        VALUES (?, ?, ?, ?)
        """

        result = cursor.execute(
            insert_data,
            (
                choice(claim_names),
                randint(100, 599),
                choice(claim_status),
                random_date_last_90_days().isoformat(),
            ),
        )

        print(result.fetchall()) if result.fetchall() else print(
            "Data Inserted Successfully:"
        )
        conn.commit()

    conn.close()
    return "Connection Closed Successfully, Data Generated..!!"


if __name__ == "__main__":
    print(random_data_generator(10))
    # drop_table() - Uncomment this while Dropping a New Table
