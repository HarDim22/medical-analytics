from datetime import datetime, timedelta, timezone
import random

from app.database import SessionLocal
from app.models import Event


existing = db.query(Event).count()
if existing > 0:
    print(f"DB already has {existing} events. Skipping seed.")
    return

API_SEED = [
    # (flow) started -> completed -> analysis -> clinician review
    ("data_upload_started", "patient", {}),
    ("data_upload_completed", "patient", {"hb": 14.2, "wbc": 6.1, "glucose": 110}),
    ("analysis_completed", "system", {"engine": "rules-v1"}),
    ("clinician_review_completed", "clinician", {"decision": "ok"}),
]

QUALITY_SEED = [
    ("missing_required_field", "system", {"field": "wbc"}),
    ("out_of_range_value_detected", "system", {"field": "hb", "value": 8.4, "min": 9.0, "max": 18.0}),
]


def main():
    db = SessionLocal()
    try:
        now = datetime.now(timezone.utc)

        total_submissions = 60  # adjust if you want more/less
        created = 0

        for i in range(1, total_submissions + 1):
            entity_id = f"SUB-{i:03d}"
            t0 = now - timedelta(days=random.randint(0, 14), minutes=random.randint(0, 600))

            # Everyone starts upload
            db.add(Event(
                event_type="data_upload_started",
                entity_id=entity_id,
                timestamp=t0,
                actor_role="patient",
                event_data={"source": random.choice(["web", "mobile"])}
            ))
            created += 1

            # Some fail data quality before completion
            if random.random() < 0.20:
                ev = random.choice(QUALITY_SEED)
                db.add(Event(
                    event_type=ev[0],
                    entity_id=entity_id,
                    timestamp=t0 + timedelta(seconds=10),
                    actor_role=ev[1],
                    event_data=ev[2],
                ))
                created += 1
                continue

            # Many complete upload
            t1 = t0 + timedelta(minutes=random.randint(1, 6))
            db.add(Event(
                event_type="data_upload_completed",
                entity_id=entity_id,
                timestamp=t1,
                actor_role="patient",
                event_data={"hb": round(random.uniform(11.5, 16.5), 1),
                            "wbc": round(random.uniform(4.0, 10.0), 1),
                            "glucose": random.randint(75, 160)}
            ))
            created += 1

            # Some analysis fails
            if random.random() < 0.12:
                db.add(Event(
                    event_type="analysis_failed",
                    entity_id=entity_id,
                    timestamp=t1 + timedelta(minutes=random.randint(1, 4)),
                    actor_role="system",
                    event_data={"reason": "quality_gate_failed"},
                ))
                created += 1
                continue

            # Many analysis completes
            t2 = t1 + timedelta(minutes=random.randint(1, 10))
            db.add(Event(
                event_type="analysis_completed",
                entity_id=entity_id,
                timestamp=t2,
                actor_role="system",
                event_data={"engine": "rules-v1"},
            ))
            created += 1

            # Some clinician reviews complete
            if random.random() < 0.70:
                t3 = t2 + timedelta(minutes=random.randint(2, 30))
                db.add(Event(
                    event_type="clinician_review_completed",
                    entity_id=entity_id,
                    timestamp=t3,
                    actor_role="clinician",
                    event_data={"decision": random.choice(["ok", "followup", "retest"])},
                ))
                created += 1

        db.commit()
        print(f"Seed complete. Inserted {created} events for {total_submissions} submissions.")
    finally:
        db.close()


if __name__ == "__main__":
    main()
