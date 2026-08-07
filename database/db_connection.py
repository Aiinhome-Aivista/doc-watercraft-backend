import os
import mysql.connector
from dotenv import load_dotenv

load_dotenv()


def get_db_connection():
    """Create and return a fresh MySQL connection.
    Caller must close the connection when done.
    """
    return mysql.connector.connect(
        host=os.getenv("MYSQL_HOST"),
        port=int(os.getenv("MYSQL_PORT", 3306)),
        user=os.getenv("MYSQL_USERNAME"),
        password=os.getenv("MYSQL_PASSWORD"),
        database=os.getenv("MYSQL_NAME")
    )

# def fix_mysql_definers():
#     try:
#         conn = get_db_connection()
#         cursor = conn.cursor()
#
#         # 1. Create missing 'aiinhome'@'%' definer user in MySQL if possible
#         try:
#             cursor.execute("CREATE USER IF NOT EXISTS 'aiinhome'@'%' IDENTIFIED BY ''")
#             cursor.execute("GRANT ALL PRIVILEGES ON *.* TO 'aiinhome'@'%'")
#             cursor.execute("FLUSH PRIVILEGES")
#         except Exception:
#             pass
#
#         # 2. Re-create v_vessel_billing view with CURRENT_USER as definer
#         try:
#             view_sql = """
#             CREATE OR REPLACE DEFINER = CURRENT_USER VIEW `v_vessel_billing` AS 
#             SELECT 
#                 `v`.`id` AS `vessel_id`,
#                 `v`.`vessel_auto_id` AS `vessel_auto_id`,
#                 `v`.`vessel_name` AS `vessel_name`,
#                 `v`.`party_id` AS `party_id`,
#                 `pm`.`party_name` AS `party_name`,
#                 `v`.`cargo_type` AS `cargo_type`,
#                 `v`.`quantity` AS `quantity`,
#                 `v`.`direction` AS `direction`,
#                 `v`.`status` AS `status`,
#                 `v`.`expected_date` AS `expected_date`,
#                 `v`.`berthing_datetime` AS `berthing_datetime`,
#                 `v`.`mooring_datetime` AS `mooring_datetime`,
#                 `v`.`survey_quantity` AS `survey_quantity`,
#                 `v`.`survey_datetime` AS `survey_datetime`,
#                 `v`.`sailing_datetime` AS `sailing_datetime`,
#                 coalesce(sum(`bd`.`amount`),0) AS `total_base_amount`,
#                 coalesce(sum(`bd`.`gst_amount`),0) AS `total_gst_amount`,
#                 coalesce(sum((`bd`.`amount` + `bd`.`gst_amount`)),0) AS `grand_total_amount`,
#                 (case when (sum(`bd`.`amount`) > 0) then 'BILLED' else 'PENDING' end) AS `billing_status` 
#             FROM ((`vessels` `v` LEFT JOIN `party_masters` `pm` ON ((`v`.`party_id` = `pm`.`id`)))
#             LEFT JOIN `bill_details` `bd` ON ((`v`.`id` = `bd`.`vessel_id`)))
#             GROUP BY `v`.`id`,`pm`.`party_name`;
#             """
#             cursor.execute(view_sql)
#             conn.commit()
#         except Exception:
#             pass
#         cursor.close()
#         conn.close()
#     except Exception as e:
#         print("[Auto-Fix MySQL Definers] Note:", e)

# Run auto-fix on startup
# try:
#     fix_mysql_definers()
# except Exception:
#     pass