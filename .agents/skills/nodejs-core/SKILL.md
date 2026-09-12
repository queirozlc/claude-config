---
name: nodejs-core
disable-model-invocation: true
description: Specialist guidance for Node.js core, libuv, V8, native addons, and runtime performance. Use only when the user explicitly activates this skill.
metadata:
  tags: nodejs, nodejs-core, contributing, commit-message, pull-request, v8, libuv, cpp, native-addons, performance, debugging, internals
---

## When to use

Use only after explicit user activation for deep Node.js internals work, including:
- C++ addon development
- V8 engine debugging
- libuv event loop issues
- Build system problems
- Compilation failures
- Performance optimization at the engine level
- Understanding Node.js core architecture
- Writing or reviewing `nodejs/node` commits and pull request descriptions

## How to use

Read individual rule files for detailed explanations and code examples:

### V8 Engine

- [rules/v8-garbage-collection.md](rules/v8-garbage-collection.md) - Scavenger, Mark-Sweep, Mark-Compact, generational GC
- [rules/v8-hidden-classes.md](rules/v8-hidden-classes.md) - Hidden classes, inline caching, optimization
- [rules/v8-jit-compilation.md](rules/v8-jit-compilation.md) - TurboFan, optimization/deoptimization patterns

### libuv

- [rules/libuv-event-loop.md](rules/libuv-event-loop.md) - Event loop phases, timers, I/O, idle, check, close
- [rules/libuv-thread-pool.md](rules/libuv-thread-pool.md) - Thread pool size, blocking operations, UV_THREADPOOL_SIZE
- [rules/libuv-async-io.md](rules/libuv-async-io.md) - Async I/O patterns, handles, requests

### Native Addons

- [rules/napi.md](rules/napi.md) - N-API development, ABI stability, async workers
- [rules/node-addon-api.md](rules/node-addon-api.md) - C++ wrapper patterns, best practices
- [rules/native-memory.md](rules/native-memory.md) - Buffer handling, external memory, prevent leaks

### Core Modules Internals

- [rules/streams-internals.md](rules/streams-internals.md) - How Node.js streams work at C++ level
- [rules/net-internals.md](rules/net-internals.md) - TCP/UDP implementation, socket handling
- [rules/fs-internals.md](rules/fs-internals.md) - libuv fs operations, sync vs async
- [rules/crypto-internals.md](rules/crypto-internals.md) - OpenSSL integration, performance considerations
- [rules/child-process-internals.md](rules/child-process-internals.md) - IPC, spawn, fork implementation
- [rules/worker-threads-internals.md](rules/worker-threads-internals.md) - SharedArrayBuffer, Atomics, MessageChannel

### JavaScript Internals

- [rules/primordials.md](rules/primordials.md) - **Using primordials to prevent prototype pollution (required for `lib/internal/`)**

### Build & Contributing

- [rules/build-and-test-workflow.md](rules/build-and-test-workflow.md) - Build and test procedures when changing Node core
- [rules/pre-commit-lint.md](rules/pre-commit-lint.md) - Repository checks when preparing a Node core commit
- [rules/configure.md](rules/configure.md) - `./configure` flags for debug builds, ASan, Ninja, etc.
- [rules/build-system.md](rules/build-system.md) - gyp, ninja, make, cross-platform compilation
- [rules/cli-options.md](rules/cli-options.md) - Adding CLI options and gating experimental modules
- [rules/contributing.md](rules/contributing.md) - How to contribute to Node.js core, the process
- [rules/commit-and-pr-guideline.md](rules/commit-and-pr-guideline.md) - Commit message and PR description style, trailers, DCO sign-off, and validation
- [rules/reviewing-prs.md](rules/reviewing-prs.md) - Reviewing PRs for correctness, clarity, and contribution quality

### Documentation

- [rules/documentation.md](rules/documentation.md) - **Updating doc/api/*.md files: structure, link ordering, error docs, code example constraints**

### Debugging & Profiling

- [rules/debugging-native.md](rules/debugging-native.md) - gdb, lldb, debugging C++ addons
- [rules/profiling-v8.md](rules/profiling-v8.md) - --prof, --trace-opt, --trace-deopt, flame graphs
- [rules/memory-debugging.md](rules/memory-debugging.md) - Heap snapshots, memory leak detection

## Apply only the relevant workflow

For diagnostics, inspect the actual runtime, build configuration, and failure before choosing a tool. Do not start a contribution or build workflow merely to explain a libuv or V8 concept.

For Node core changes, read the relevant build and contribution references. Rebuild when changed sources are embedded in the tested binary, including normal builds of `src/` and `lib/`. A stale binary does not validate the change. Inspect the existing configuration before asking the user about missing flags.

Before a Node core commit, preserve the repository's required formatting, lint, commit validation, and human contributor sign-off. Use the current checkout's documented commands. Do not add landing-only metadata. Select regression coverage for the changed behavior instead of creating redundant tests.

For performance work, establish a repeatable baseline and compare the same workload. Follow observed evidence; do not add a cache or native abstraction without a demonstrated need.
