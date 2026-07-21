import { describe, it, expect } from "vitest";
import { spansToBoxes, collectLeafSpans } from "./span-bridge";
import type { ParseBlock } from "./types";

const rect = (l: number, t: number, r: number, b: number) => ({ l, t, r, b });

const blocks: ParseBlock[] = [
  {
    id: "1",
    type: "text",
    page: 1,
    rect: rect(0.05, 0.1, 0.9, 0.2),
    parts: [
      { span: [0, 40], rect: rect(0.05, 0.1, 0.9, 0.13) },
      { span: [40, 80], rect: rect(0.05, 0.13, 0.9, 0.16) },
      { span: [80, 120], rect: rect(0.05, 0.16, 0.9, 0.19) },
    ],
  },
  {
    id: "2",
    type: "text",
    page: 2,
    rect: rect(0.05, 0.3, 0.9, 0.4),
    parts: [{ span: [200, 260], rect: rect(0.05, 0.3, 0.9, 0.33) }],
  },
];

describe("span bridge", () => {
  it("maps a field span to the overlapping line part box", () => {
    // A field span [45,70] overlaps only the second line of block 1.
    const boxes = spansToBoxes([[45, 70]], "doc1", blocks);
    expect(boxes).toHaveLength(1);
    expect(boxes[0]).toMatchObject({ docId: "doc1", page: 1 });
    expect(boxes[0].rect.t).toBeCloseTo(0.13);
  });

  it("returns every line a multi-line span touches, page-ordered", () => {
    // [10,70] overlaps line 1 ([0,40)) and line 2 ([40,80)) but not line 3 ([80,120)).
    const boxes = spansToBoxes([[10, 70]], "doc1", blocks);
    expect(boxes).toHaveLength(2);
    expect(boxes[0].rect.t).toBeCloseTo(0.1);
    expect(boxes[1].rect.t).toBeCloseTo(0.13);
  });

  it("crosses blocks and pages when spans are disjoint", () => {
    const boxes = spansToBoxes([[0, 20], [210, 240]], "doc1", blocks);
    expect(boxes.map((b) => b.page)).toEqual([1, 2]);
  });

  it("uses half-open intervals — a span ending exactly at a boundary does not bleed", () => {
    // [0,40] touches only line 1 ([0,40)); it must NOT include line 2 ([40,80)).
    const boxes = spansToBoxes([[0, 40]], "doc1", blocks);
    expect(boxes).toHaveLength(1);
    expect(boxes[0].rect.t).toBeCloseTo(0.1);
  });

  it("returns nothing for an empty span set", () => {
    expect(spansToBoxes([], "doc1", blocks)).toEqual([]);
  });
});

describe("collectLeafSpans", () => {
  it("walks a nested extraction_metadata tree and keys leaves by path", () => {
    const meta = {
      benefits: [
        { name: { spans: [[0, 10]], value: "A" }, limit_amount: { spans: [[10, 20]], value: "$1" } },
      ],
      plan_name: { spans: [[100, 120]], value: "P" },
    };
    const leaves = collectLeafSpans(meta);
    expect(leaves["benefits.0.name"]).toEqual([[0, 10]]);
    expect(leaves["benefits.0.limit_amount"]).toEqual([[10, 20]]);
    expect(leaves["plan_name"]).toEqual([[100, 120]]);
  });
});
