import { describe, it, expect } from "vitest";
import { pageCachePath, bboxToStyle } from "./pdf-render";

describe("pdf-render helpers", () => {
  it("builds deterministic cache paths", () => {
    expect(pageCachePath("doc1", 3)).toMatch(/uploads[\\/]page-cache[\\/]doc1-3\.png$/);
  });
  it("converts normalized bbox to css percentages", () => {
    expect(bboxToStyle({ l: 0.1, t: 0.2, r: 0.5, b: 0.4 })).toEqual({
      left: "10%",
      top: "20%",
      width: "40%",
      height: "20%",
    });
  });
});
