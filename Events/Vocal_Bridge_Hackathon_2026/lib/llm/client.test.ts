import { describe, it, expect, vi } from "vitest";
import { z } from "zod";
import { parseJsonReply, chatJSONWith } from "./client";

describe("parseJsonReply", () => {
  it("strips fences and extracts outermost object", () => {
    expect(parseJsonReply('```json\n{"a":1}\n```')).toEqual({ a: 1 });
    expect(parseJsonReply('noise {"a":{"b":2}} trailing')).toEqual({ a: { b: 2 } });
  });
  it("throws when no JSON present", () => {
    expect(() => parseJsonReply("no json here")).toThrow();
  });
});

describe("chatJSONWith", () => {
  const schema = z.object({ verdict: z.string() });
  it("returns validated object on first try", async () => {
    const transport = { chat: vi.fn().mockResolvedValue('{"verdict":"ok"}') };
    const out = await chatJSONWith(transport, { system: "s", messages: [{ role: "user", content: "q" }], schema });
    expect(out.verdict).toBe("ok");
    expect(transport.chat).toHaveBeenCalledTimes(1);
  });
  it("retries once with validation error appended", async () => {
    const transport = {
      chat: vi.fn()
        .mockResolvedValueOnce('{"wrong":true}')
        .mockResolvedValueOnce('{"verdict":"fixed"}'),
    };
    const out = await chatJSONWith(transport, { system: "s", messages: [{ role: "user", content: "q" }], schema });
    expect(out.verdict).toBe("fixed");
    expect(transport.chat).toHaveBeenCalledTimes(2);
    const retryMessages = transport.chat.mock.calls[1][0].messages;
    expect(retryMessages.at(-1)!.content).toContain("verdict");
  });
  it("throws after second failure", async () => {
    const transport = { chat: vi.fn().mockResolvedValue("garbage") };
    await expect(
      chatJSONWith(transport, { system: "s", messages: [{ role: "user", content: "q" }], schema })
    ).rejects.toThrow();
  });
});
