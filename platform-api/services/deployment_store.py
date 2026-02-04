from db.database import get_connection

def save(deployment):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO deployments (id, cloud, environment, application, status, created_at)
        VALUES (%s, %s, %s, %s, %s, %s)
    """, (
        deployment.id,
        deployment.cloud,
        deployment.environment,
        deployment.application,
        deployment.status.value,
        deployment.created_at
    ))

    for evt in deployment.events:
        cur.execute("""
            INSERT INTO deployment_events (deployment_id, status, time)
            VALUES (%s, %s, %s)
        """, (
            deployment.id,
            evt["status"],
            evt["time"]
        ))

    conn.commit()
    cur.close()
    conn.close()


def get_all():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT * FROM deployments
        ORDER BY created_at DESC
    """)
    deployments = cur.fetchall()

    result = []
    for d in deployments:
        cur.execute("""
            SELECT status, time
            FROM deployment_events
            WHERE deployment_id = %s
            ORDER BY time
        """, (d["id"],))

        events = cur.fetchall()
        result.append({**d, "events": events})

    cur.close()
    conn.close()
    return result


def get_by_id(deployment_id):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT * FROM deployments WHERE id = %s
    """, (deployment_id,))
    deployment = cur.fetchone()

    if not deployment:
        cur.close()
        conn.close()
        return None

    cur.execute("""
        SELECT status, time
        FROM deployment_events
        WHERE deployment_id = %s
        ORDER BY time
    """, (deployment_id,))
    events = cur.fetchall()

    cur.close()
    conn.close()

    return {**deployment, "events": events}

def update_status(deployment_id, status, event):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        UPDATE deployments
        SET status = %s
        WHERE id = %s
    """, (status, deployment_id))

    cur.execute("""
        INSERT INTO deployment_events (deployment_id, status, time)
        VALUES (%s, %s, %s)
    """, (
        deployment_id,
        event["status"],
        event["time"]
    ))

    conn.commit()
    cur.close()
    conn.close()