---
name: elixir
description: Write, review, or refactor Elixir, Phoenix, and Ecto code. Use for Elixir projects, including their migrations, queries, concurrency, and tests.
---

# Elixir and Phoenix

## The Iron Law

```
DATA IN, DATA OUT. NO PROCESS, NO MACRO, NO ABSTRACTION UNTIL THE
PLAIN FUNCTION FAILS. THE BOUNDARY VALIDATES. THE CORE IS PURE.
```

Elixir code is a pipeline of pure functions over immutable data. A process is a
tool for state, concurrency, or failure isolation. A process is not a tool for
code structure. A macro is not a tool for code reuse.

## Before you write code

1. Read the surrounding modules. Match their naming, error style, and layout.
2. Check `mix.exs` for the Elixir, Phoenix, and Ecto versions. Do not assume.
3. Read `deps/<dep>/usage-rules.md` for any dependency you are new to. Many
   packages ship one. It states the current API.
4. Never guess an API. Use context7 or hexdocs to verify.
5. Load the reference file for the layer you touch. See the routing table.

## Routing table

Read the matching reference file BEFORE you write the code. Read only what you
need.

| You are working on | Read |
| --- | --- |
| Any Elixir module, function, pipeline, control flow | `references/core-idioms.md` |
| GenServer, Task, Agent, Supervisor, ETS, Registry, concurrency | `references/otp-processes.md` |
| Controller, LiveView, HEEx, router, context, PubSub, auth scope | `references/phoenix.md` |
| Schema, changeset, query, migration, transaction, N+1 | `references/ecto.md` |
| Test, mock, factory, sandbox, mix task, credo, dialyzer | `references/testing-and-tooling.md` |
| `quote`, `defmacro`, `use`, `__using__`, DSL, code generation | `references/metaprogramming.md` |
| Reviewing code, or unsure why something feels wrong | `references/anti-patterns.md` |

Read `references/anti-patterns.md` for any review task. It carries the official
Elixir anti-patterns plus the mistakes that AI code generators make.

## Non-negotiable rules

These apply to every file. The reference files hold the detail.

1. **Pattern match in the function head.** Multiple clauses and guards replace
   `if`, `cond`, and nested `case`.
2. **Return `{:ok, value}` or `{:error, reason}`** for expected failure. Use a
   `!` function to raise. Use an exception only for the impossible.
3. **Use `with` for a chain of fallible steps.** Never nest `case` in `case`.
4. **Never use a catch-all `_ -> nil`** to silence a value you did not plan for.
   Match every expected shape. Let the rest crash.
5. **Pipe from a value, not from a single call.** Every piped call has
   parentheses.
6. **The web layer never calls `Repo`.** Contexts are the only door to the
   database.
7. **Every query is scoped by the current user or tenant.** Authorize inside
   every `handle_event/3`, not only in `mount/3`.
8. **Every uniqueness or foreign key validation pairs with a real DB
   constraint.** A changeset validation alone is a race condition.
9. **Preload associations.** Never ship an N+1.
10. **No business logic inside a GenServer callback.** Callbacks call pure
    modules.
11. **`@impl true` on every callback.** `@spec` on every public function.
12. **Never build an atom from user input.** Use `String.to_existing_atom/1`.
13. **Write a function, not a macro.** See the gate in
    `references/metaprogramming.md`.
14. **Every test is `async: true`** unless it changes global state.

## Red flags: stop and reconsider

Stop when you are about to write any of these. Each one is usually the wrong
tool.

- A GenServer that only holds a value another process reads. Use ETS, or pass
  the value as an argument.
- A macro that saves typing. Use a function.
- A `try/rescue` that controls normal flow. Use a tagged tuple.
- A single "god" changeset with option flags. Use one changeset per use case.
- A context module that grows past its subject. Split it.
- A `case` that ends with `_ -> nil` or `_ -> :ok`.
- A `Repo` call inside a controller, a LiveView, or a HEEx template.
- `Enum.map` inside `Enum.map` over database rows. That is a join.
- A defensive `if is_nil(x)` chain. Match on the shape instead.
- A private function you plan to make public only for a test.

## Excuse vs reality

| Excuse | Reality |
| --- | --- |
| "I need a GenServer to hold this state." | The caller can hold it. Or ETS can. A process serializes every read. |
| "A macro keeps this DRY." | A macro breaks tooling, dialyzer, and the reader. A function does not. |
| "I will add the DB constraint later." | Two concurrent requests pass the same validation. Add it now. |
| "The catch-all clause is defensive." | It converts a bug into silent wrong data. Let it crash. |
| "Preloading everywhere is slow." | An N+1 is slower. Select only the fields you need. |
| "This test needs `async: false`." | Usually it needs the sandbox `allow/3` call instead. |
| "The controller is small, one `Repo` call is fine." | The next one will not be. The boundary holds or it does not. |
| "The old code in this repo does it this way." | Match the local style. Do not copy a defect. Say what you found. |

## Verification

Run checks appropriate to the changed behavior. Use focused ExUnit tests or `mix test --stale` while iterating. Add a regression test only when it covers a meaningful behavior or risk not already covered.

Before completion, run the repository's required checks or `mix precommit` when required by its workflow. Do not repeat a full gate after every edit or for a conceptual explanation. Rerun affected checks after further changes. Report actual results and unresolved failures.
