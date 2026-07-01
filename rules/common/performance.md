# Performance

Always-on. About *working* efficiently, not micro-optimizing code.

## Model selection

- Match model to task. Reach for the cheapest one that clears the bar; escalate only when it visibly falls short.
- Heavy reasoning / architecture / tricky debugging → most capable model.
- Bulk search, mechanical edits, summarization → a lighter/faster model.
- Don't burn a frontier model on a task a small one does correctly.

## Context management

- Load what the task needs, not the whole repo. Read the specific lines, not the whole file, once you know where to look.
- Fan out broad searches to a subagent and take back the conclusion, not the file dumps.
- Prefer targeted tools (grep/glob/read-range) over dumping large outputs into context.
- Long-running work: checkpoint decisions in a file so a compaction doesn't lose them.
- Parallelize independent tool calls in one turn; serialize only real dependencies.
