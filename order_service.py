"""Order lookup and payment helpers."""

import sqlite3
from typing import Any
import requests


def get_order(conn: sqlite3.Connection, order_id: str) -> dict[str, Any] | None:
  """Fetches a single order record safely by ID."""
  cur = conn.execute(
      "SELECT id, status, total_cents FROM orders WHERE id = ?",
      (order_id,),
  )
  row = cur.fetchone()
  if row is None:
    return None
  return {"id": row[0], "status": row[1], "total_cents": row[2]}


def charge_order(payment_url: str, order_id: str, amount_cents: int) -> dict[str, Any]:
  """Submits a single charge request with an explicit timeout."""
  resp = requests.post(
      payment_url,
      json={"order_id": order_id, "amount_cents": amount_cents},
      timeout=5.0,
  )
  resp.raise_for_status()
  return resp.json()
