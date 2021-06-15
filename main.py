import os
import sys

import pyodbc
import toml

import notification_telegram


def create_connection(server_name):
    conn = pyodbc.connect(
        "DRIVER={ODBC Driver 17 for SQL Server};"
        f"SERVER={server_name};"
        "DATABASE=master;"
        "Trusted_Connection=yes;"
    )
    return conn


def sql_select(conn, sql):
    rows = conn.cursor().execute(sql).fetchall()
    return rows


def main():
    # Load Config
    config = toml.load(os.path.join(sys.path[0], "config.toml"))
    config_alert = config.get("alert")
    tg_chat = notification_telegram.get_telegram_chat(config.get("telegram"))
    # Process all servers
    for server in config.get("servers"):
        host_name = server.get("host_name")
        conn = create_connection(host_name)
        sql = """
            select distinct
                volst.volume_mount_point as drive
                ,cast(volst.total_bytes / 1048576. as bigint) as total_space_mb
                ,cast(volst.available_bytes / 1048576. as bigint) as free_space_mb
            from
                sys.master_files as mf
                cross apply sys.dm_os_volume_stats(mf.database_id, mf.[file_id]) as volst;
        """
        rows = sql_select(conn, sql)
        for row in rows:
            free_space_percent = row.free_space_mb / row.total_space_mb
            if row.free_space_mb < config_alert.get(
                "disk_free_space_mb"
            ) or free_space_percent < config_alert.get("disk_free_space_percent"):
                message_header = (
                    f"*Disk Alert! Server: `{host_name}` Drive `{row.drive}\\ `*"
                )
                message = (
                    message_header
                    + f"\nFree space: {row.free_space_mb / 1024:.2f} GB ({free_space_percent:.2%})"
                )
                notification_telegram.send_text_message(tg_chat, message)


if __name__ == "__main__":
    main()
