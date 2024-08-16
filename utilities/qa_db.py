# import pyodbc
#
# class TestSqlQuery:
#     __test__ = False
#
#     def __init__(self, conn_str):
#         try:
#             self.conn = pyodbc.connect(conn_str)
#         except Exception as error:
#             print(error)
#
#     def delete(self, request):
#         cursor = self.conn.cursor()
#         sql = f"DELETE FROM Beneficiary WHERE bankAccountHolderEmail = '{request}'"
#         try:
#             cursor.execute(sql)
#             self.conn.commit()
#             status = f"Delete {request} executed"
#             return status
#         except pyodbc.Error as error:
#             return error
#         finally:
#             cursor.close()
#
#     def existUser(self,request):
#         cursor = self.conn.cursor()
#         sql = "select count(*) from Beneficiary where bankAccountHolderEmail = '" + str(request) + "'"
#         try:
#             rows = cursor.execute(sql)
#             return rows
#         except pyodbc as error:
#             return error
#         finally:
#             cursor.close()
