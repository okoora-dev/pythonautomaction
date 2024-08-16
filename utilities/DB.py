import time

import pyodbc

class TestSqlQuery:
    __test__ = False

    def __init__(self, conn_str):
        try:
            self.conn = pyodbc.connect(conn_str)
        except Exception as error:
            print(error)

    def delete(self, request):
        cursor = self.conn.cursor()
        sql = f"DELETE FROM Beneficiary WHERE bankAccountHolderEmail = '{request}'"
        try:
            cursor.execute(sql)
            self.conn.commit()  # commit on connection
            status = f"Delete {request} executed"
            return status
        except pyodbc.Error as error:
            return error
        finally:
            cursor.close()

    def existUser(self, request):
        cursor = self.conn.cursor()
        sql = f"SELECT COUNT(*) FROM Beneficiary WHERE bankAccountHolderEmail = '{request}'"
        try:
            rows = cursor.execute(sql).fetchone()
            return rows
        except pyodbc.Error as error:
            return error
        finally:
            cursor.close()

    def deletePayer(self, request):
        cursor = self.conn.cursor()
        sql = f"DELETE FROM Payers WHERE SetupProfileId = '{request}'"
        try:
            cursor.execute(sql)
            self.conn.commit()  # commit on connection
            status = f"Delete Payer {request} executed"
            return status
        except pyodbc.Error as error:
            return error
        finally:
            cursor.close()

    def existPayer(self, request):
        cursor = self.conn.cursor()
        sql = f"SELECT COUNT(*) FROM Payers WHERE SetupProfileId = '{request}'"
        try:
            rows = cursor.execute(sql).fetchone()
            return rows
        except pyodbc.Error as error:
            return error
        finally:
            cursor.close()

    def check_status(self, request):
        cursor = self.conn.cursor()
        sql = "SELECT COUNT(*) FROM Exposures WHERE ExposureID = ? AND status = 1"
        try:
            cursor.execute(sql, (request,))
            result = cursor.fetchone()
            print(result)
            return result[0] if result else 0
        except pyodbc.Error as error:
            return error
        finally:
            cursor.close()
    def check_row_trans(self, request):
        cursor = self.conn.cursor()
        sql = f"""
            SELECT COUNT(*)
            FROM BalanceTransfers
            WHERE LastTransaction = ?
            AND (comment NOT LIKE '' OR comment IS NOT NULL)
        """
        try:
            result = cursor.execute(sql,request,).fetchone()
            return result[0] if result else 0
        except pyodbc.Error as error:
            return error
        finally:
            cursor.close()

    def approve_deposit(self, request):
        cursor = self.conn.cursor()
        sql = f"""
            UPDATE BalanceTransfers 
            SET ClearingApprove = 1, AccountingApprove = 1
            WHERE LastTransaction = '{request}'
        """
        try:
            cursor.execute(sql)
            self.conn.commit()  # commit on connection
            status = f"Approve deposit {request} executed"
            return status
        except pyodbc.Error as error:
            return error
        finally:
            cursor.close()

    def add_free_fee(self, request):
        cursor = self.conn.cursor()
        sql = f"""
            UPDATE AccountPackage 
            SET OutgoingPayments = 1
            WHERE userid = '{request}' AND status = 1
        """
        try:
            cursor.execute(sql)
            self.conn.commit()  # commit on connection
            status = f"Add free fee for {request} executed"
            return status
        except pyodbc.Error as error:
            return error
        finally:
            cursor.close()

    def change_outgoing_payments(self, request):
        cursor = self.conn.cursor()
        sql = f"""
            UPDATE AccountPackageusage
            SET OutgoingPayments = 0
            WHERE userid = '{request}'
            AND currentmonth = (
                SELECT MAX(currentmonth)
                FROM AccountPackageusage
                WHERE userid = '{request}'
            )
        """
        try:
            cursor.execute(sql)
            self.conn.commit()  # commit on connection
            status = f"Change outgoing payments for {request} executed"
            return status
        except pyodbc.Error as error:
            return error
        finally:
            cursor.close()

    def reset_outgoing_payments(self, request):
        cursor = self.conn.cursor()
        sql = f"UPDATE AccountPackageusage SET OutgoingPayments = 0 WHERE userid = '{request}'"
        try:
            cursor.execute(sql)
            self.conn.commit()  # commit on connection
            status = f"Reset outgoing payments for {request} executed"
            return status
        except pyodbc.Error as error:
            return error
        finally:
            cursor.close()

    def find_quote(self, request):
        cursor = self.conn.cursor()
        sql = """
            SELECT COUNT(*)
            FROM Quote q
            JOIN PaymentRequestApi pri ON q.id = pri.quoteid
            WHERE pri.RequestId = ? AND q.Cost IS NOT NULL AND q.costType IS NOT NULL
        """
        try:
            result = cursor.execute(sql, request).fetchone()
            return result[0] if result else 0
        except pyodbc.ProgrammingError as error:
            return error
        finally:
            cursor.close()

    def get_fee_payed(self, request):
        cursor = self.conn.cursor()
        sql = """
            SELECT TOP 1 Amount
            FROM BalanceInOut
            WHERE UserId = ? AND InsertType = 31
            ORDER BY InsertDate DESC
        """
        try:
            result = cursor.execute(sql, request).fetchone()
            return result[0] if result else 0
        except pyodbc.ProgrammingError as error:
            return error
        finally:
            cursor.close()

    def delete_from_webhookoutlogs(self,request):
        cursor = self.conn.cursor()
        sql = """delete from WebhookOutLogs where ProfileId = ?"""
        try:
            cursor.execute(sql,request)
            self.conn.commit()  # commit on connection
            status = f"Deleted from log"
            return status
        except pyodbc.Error as error:
            return error
        finally:
            cursor.close()

    def get_from_webhookoutlogs(self, request):
        time.sleep(5)
        cursor = self.conn.cursor()
        sql = """
             SELECT TOP 1 ProfileId from WebhookOutLogs where ProfileId = ?
        """
        try:
            result = cursor.execute(sql, request).fetchone()
            return result[0] if result else 0
        except pyodbc.ProgrammingError as error:
            return error
        finally:
            cursor.close()
