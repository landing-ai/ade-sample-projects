"""
metrics.py
----------
Thread-safe throughput metrics + a live one-line display.

The demo's whole point is showing extracted results landing in Snowflake at a
high rate, so this tracks documents/sec and rows/sec and renders a status line
that updates in place while the pipeline streams.
"""

from __future__ import annotations

import sys
import time
import threading
from dataclasses import dataclass, field


@dataclass
class Metrics:
    total_docs: int
    _lock: threading.Lock = field(default_factory=threading.Lock, repr=False)

    docs_ok: int = 0
    docs_fail: int = 0
    pages: int = 0
    rows_landed: int = 0          # main + line + block + markdown rows sent to Snowflake
    parse_sec_sum: float = 0.0    # summed per-doc parse+extract latency (overlaps in wall time)

    wall_start: float = 0.0
    wall_end: float = 0.0

    def start(self):
        self.wall_start = time.perf_counter()

    def stop(self):
        self.wall_end = time.perf_counter()

    def record(self, ok: bool, pages: int, parse_sec: float, rows: int):
        with self._lock:
            if ok:
                self.docs_ok += 1
                self.pages += pages
                self.parse_sec_sum += parse_sec
                self.rows_landed += rows
            else:
                self.docs_fail += 1

    @property
    def wall(self) -> float:
        end = self.wall_end or time.perf_counter()
        return max(1e-9, end - self.wall_start)

    @property
    def docs_done(self) -> int:
        return self.docs_ok + self.docs_fail

    def render_line(self) -> str:
        w = self.wall
        dps = self.docs_ok / w
        rps = self.rows_landed / w
        pps = self.pages / w
        return (
            f"\r  {self.docs_done}/{self.total_docs} docs "
            f"| {dps:5.1f} docs/s | {pps:5.1f} pages/s "
            f"| {self.rows_landed:>7,} rows -> Snowflake ({rps:6.0f} rows/s) "
            f"| ok={self.docs_ok} fail={self.docs_fail} "
            f"| {w:5.1f}s"
        )

    def print_live(self):
        sys.stdout.write(self.render_line())
        sys.stdout.flush()

    def summary(self) -> str:
        w = self.wall
        avg_doc = (self.parse_sec_sum / self.docs_ok) if self.docs_ok else 0.0
        return (
            "\n"
            "==================== Run summary ====================\n"
            f"  Documents:        {self.docs_ok} ok, {self.docs_fail} failed "
            f"({self.total_docs} submitted)\n"
            f"  Pages:            {self.pages}\n"
            f"  Rows -> Snowflake:{self.rows_landed:,}\n"
            f"  Wall time:        {w:.1f}s\n"
            f"  Throughput:       {self.docs_ok / w:.1f} docs/s, "
            f"{self.pages / w:.1f} pages/s, {self.rows_landed / w:.0f} rows/s\n"
            f"  Avg parse+extract:{avg_doc:.2f}s/doc (overlapped across workers)\n"
            "====================================================="
        )
