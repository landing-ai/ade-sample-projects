import { z } from "zod";
import { GroundBoxSchema } from "./grounded";

// A citation references grounded field `refs` (stable ids from the extracted policy) and carries
// server-resolved `boxes` (normalized rects) for the document highlight. Claude fills
// role/label/text/refs; the server resolves refs → boxes after the model returns.
export const CitationSchema = z.object({
  role: z.enum(["supports", "limits", "excludes", "defines"]).default("supports"),
  label: z.string().default(""),
  text: z.string().default(""),
  refs: z.array(z.string()).default([]),
  boxes: z.array(GroundBoxSchema).default([]),
});
export type Citation = z.infer<typeof CitationSchema>;

export const VerdictSchema = z.object({
  verdict: z.enum(["likely_covered", "likely_not_covered", "it_depends", "need_more_info"]),
  benefit: z.string().nullish(),
  headline: z.string(),
  reasoning: z.string(),
  citations: z.array(CitationSchema).default([]),
  open_questions: z.array(z.string()).default([]),
  deadlines: z.array(z.string()).default([]),
  next_steps: z.array(z.string()).default([]),
  max_benefit: z.string().nullish(),
});
export type Verdict = z.infer<typeof VerdictSchema>;

// One hotline turn: the conversational line to speak, plus a full grounded verdict when the
// caller asked a coverage question (null for greetings / small-talk).
export const HotlineReplySchema = z.object({
  reply: z.string(),
  assessment: VerdictSchema.nullable(),
});
export type HotlineReply = z.infer<typeof HotlineReplySchema>;
