import { describe, it, expect } from "vitest";
import { env } from "./env";

describe("env", () => {
  it("defaults LLM provider to ollama", () => {
    delete process.env.LLM_PROVIDER;
    expect(env().llmProvider).toBe("ollama");
  });
  it("parses privacy toggle", () => {
    process.env.DELETE_RAW_PDFS_AFTER_EXTRACTION = "true";
    expect(env().deleteRawPdfs).toBe(true);
  });
});
