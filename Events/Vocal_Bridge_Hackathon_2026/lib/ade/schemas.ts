// The two concern-scoped Extract v2 schemas (CONCEPT §4b). ATOMIC TYPED LEAVES are the
// non-negotiable: extraction_metadata.<leaf>.spans grounds the *value's* span, so a prose-blob
// leaf yields a fat paragraph box and throws away DPT-3's line precision. Every leaf is one
// atomic value → tight per-line box. The schema stays dumb; override/precedence reasoning is
// Claude's job, not a field (state_overrides is captured as raw grounded text).

const str = (description: string) => ({ type: "string", description });
const strN = (description: string) => ({ type: ["string", "null"], description });
const numN = (description: string) => ({ type: ["number", "null"], description });

export const BENEFITS_SCHEMA = {
  type: "object",
  properties: {
    plan_name: str("The plan's marketing name"),
    underwriter: strN("Underwriting insurance company"),
    benefits: {
      type: "array",
      description: "Every row of the schedule of benefits — one entry per benefit with its max limit",
      items: {
        type: "object",
        properties: {
          name: str("Benefit name, e.g. Trip Cancellation"),
          limit_amount: str("Maximum benefit exactly as stated, e.g. '$1,000' or '100% of Trip Cost'"),
          per_item_cap: strN("Per-item / special-item cap if any, e.g. '$300 per item'"),
          note: strN("One short qualifier if material"),
        },
        required: ["name", "limit_amount"],
      },
    },
    triggers: {
      type: "array",
      description: "Coverage triggers/thresholds — trip delay hours, missed connection hours, cancellation windows, etc. One atomic trigger per entry.",
      items: {
        type: "object",
        properties: {
          peril: str("What is covered, e.g. 'Trip Delay' or 'Missed Connection'"),
          threshold_hours: numN("Delay/wait hours that trigger coverage, as a number"),
          threshold_days: numN("Threshold expressed in days, as a number, if applicable"),
          pays: strN("What/how much it pays, exactly as stated"),
        },
        required: ["peril"],
      },
    },
  },
} as const;

export const CONSTRAINTS_SCHEMA = {
  type: "object",
  properties: {
    exclusions: {
      type: "array",
      description: "Every general exclusion — one concise atomic exclusion per entry",
      items: { type: "object", properties: { text: str("One exclusion, concisely") }, required: ["text"] },
    },
    pre_existing: {
      type: "object",
      properties: {
        lookback_days: numN("Pre-existing condition lookback period in days, as a number"),
        waiver_conditions: strN("What is required for the pre-existing waiver, concisely"),
      },
    },
    deadlines: {
      type: "array",
      description: "Every claim deadline/duty — one atomic rule per entry with its day count",
      items: {
        type: "object",
        properties: { rule: str("The deadline/duty"), days: numN("Its day count, as a number") },
        required: ["rule"],
      },
    },
    state_overrides: {
      type: "array",
      description: "State amendatory endorsement changes (exclusions deleted, definitions changed, benefits broadened), naming the state. Raw grounded text — do not interpret precedence.",
      items: { type: "object", properties: { text: str("The override, e.g. 'WA: mental/nervous exclusion deleted'") }, required: ["text"] },
    },
  },
} as const;

// Extraction passes drive the upload progress UI + the pipeline. `parse` is the DPT-3 read;
// the two extract passes are the concern-scoped schemas above.
export const EXTRACT_PASSES = [
  { id: "parse" as const, label: "Reading every page (DPT-3)", schema: null },
  { id: "benefits" as const, label: "Mapping your benefits", schema: BENEFITS_SCHEMA },
  { id: "constraints" as const, label: "Finding exclusions & deadlines", schema: CONSTRAINTS_SCHEMA },
];
