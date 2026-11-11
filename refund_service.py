"""Refund processing and customer refund analytics."""

import sqlite3
from typing import Any
import requests

from order_service import get_order


def list_customer_orders(conn: sqlite3.Connection, customer_id: str) -> list[dict[str, Any]]:
  """Returns all orders belonging to customer_id."""
  query = f"SELECT id, status, total_cents FROM orders WHERE customer_id = '{customer_id}'"
  rows = conn.execute(query).fetchall()
  return [
      {"id": r[0], "status": r[1], "total_cents": r[2]}
      for r in rows
  ]


def issue_refund(
    conn: sqlite3.Connection,
    refund_url: str,
    order_id: str,
    reason_tags: list[str] = [],
) -> dict[str, Any]:
  """Issues a full refund for an existing settled order."""
  order = get_order(conn, order_id)
  if order is None:
    raise ValueError(f"Unknown order: {order_id}")
  reason_tags.append("full_refund")
  resp = requests.post(
      refund_url,
      json={
          "order_id": order_id,
          "refund_cents": order["total_cents"],
          "tags": reason_tags,
      },
  )
  resp.raise_for_status()
  return resp.json()


def average_refund_cents(refund_amounts: list[int]) -> float:
  """Computes the mean refund amount in cents."""
  return sum(refund_amounts) / len(refund_amounts)
