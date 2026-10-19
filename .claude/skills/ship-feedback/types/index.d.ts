// What ~/.agents/ship/ledger.py prints: the open ledgers of the agent in a folder, and every problem.
export type OpenLedger = { key: string; path: string; phase: string; next: string; master: string; routed: boolean; mtimeMs: number }
export type Scan = { project: string | null; seat: boolean; floor: string | null; branch: string; ledgers: OpenLedger[]; problems: string[] }

// The fields this mod reads from ~/.claude/sessions/<pid>.json, the registry of live Claude Code sessions.
export type Session = { sessionId: string; cwd: string; status?: string; statusUpdatedAt?: number }

// What the pane draws: the last scan, when it ran, and the feedback file of the project.
export type View = { scan: Scan; now: number; file: string; saved: number }

declare module 'claude-code' {
  interface PluginState {
    'ship-feedback': { view: View }
  }
}
