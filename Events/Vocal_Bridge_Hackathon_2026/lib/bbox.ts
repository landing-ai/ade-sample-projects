// Node-free bbox math, safe to import from client components.
export type Bbox = { l: number; t: number; r: number; b: number };

function pct(v: number): string {
  return `${+(v * 100).toFixed(4)}%`;
}

// Convert a normalized 0..1 bbox into absolute-positioning CSS percentages.
export function bboxToStyle(box: Bbox): { left: string; top: string; width: string; height: string } {
  return {
    left: pct(box.l),
    top: pct(box.t),
    width: pct(box.r - box.l),
    height: pct(box.b - box.t),
  };
}
