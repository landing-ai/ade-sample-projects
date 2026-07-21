import path from "node:path";
import fs from "node:fs";
import { execFile } from "node:child_process";
import { promisify } from "node:util";

// Re-exported so existing importers/tests can pull it from here; the implementation
// lives in the node-free ./bbox module so client components can use it too.
export { bboxToStyle } from "./bbox";

const execFileAsync = promisify(execFile);

export const PAGE_CACHE_DIR = path.join(process.cwd(), "uploads", "page-cache");

export function pageCachePath(docId: string, page: number): string {
  return path.join(PAGE_CACHE_DIR, `${docId}-${page}.png`);
}

// Render one PDF page to PNG at ~150 DPI via poppler's pdftoppm. Throws a clear
// error if pdftoppm isn't installed (no pdfjs fallback is bundled — this host has poppler).
export async function renderPdfPageToPng(pdfPath: string, page1: number, outPath: string): Promise<void> {
  fs.mkdirSync(path.dirname(outPath), { recursive: true });
  const prefix = outPath.replace(/\.png$/, "");
  try {
    await execFileAsync("pdftoppm", [
      "-f", String(page1),
      "-l", String(page1),
      "-r", "150",
      "-png",
      "-singlefile",
      pdfPath,
      prefix,
    ]);
  } catch (e) {
    const err = e as NodeJS.ErrnoException;
    if (err.code === "ENOENT") {
      throw new Error("pdftoppm not found — install poppler (brew install poppler) to render page images.");
    }
    throw new Error(`pdftoppm failed rendering page ${page1}: ${String(e).slice(0, 200)}`);
  }
}
