// What ~/.agents/ship/ledger.py prints: the open ledgers of the agent in a folder, and every problem.
export type OpenLedger = { key: string; path: string; phase: string; next: string; master: string; routed: boolean; mtimeMs: number }
export type Scan = { project: string | null; seat: boolean; floor: string | null; branch: string; ledgers: OpenLedger[]; problems: string[] }

declare module 'claude-code' {
  interface PluginState {
    'ship-guard': { isLoaded: boolean; tried: boolean; scan: Scan }
  }
}
