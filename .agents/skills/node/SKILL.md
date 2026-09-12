---
name: node
disable-model-invocation: true
description: Specialist guidance for Node.js application async behavior and performance. Use only when the user explicitly activates this skill.
metadata:
  tags: node, nodejs, javascript, typescript, performance
---

# Node.js application performance

Use only after explicit user activation. Focus on the requested async, stream, resource-lifecycle, or performance problem. Use nodejs-core when explicitly selected for runtime internals.

Inspect the supported Node version, existing architecture, and relevant callers. Reproduce the problem and measure the suspected bottleneck before adding caching, concurrency, or dependencies. Reuse the installed stack and native APIs when they satisfy the requirement. Do not require type stripping or replace the project's compiler setup.

For a slow path, capture a representative profile and compare the changed path under the same conditions. For streams, preserve backpressure, failure propagation, and teardown. An async generator or cache is optional, not a checklist requirement.

Read only the relevant rule files. Their examples are options to assess against the current runtime and project. Run affected checks and preserve required repository gates. Do not add redundant tests to increase test count.

## References


- [rules/error-handling.md](rules/error-handling.md) - Error handling patterns in Node.js
- [rules/async-patterns.md](rules/async-patterns.md) - Async/await and Promise patterns
- [rules/streams.md](rules/streams.md) - Working with Node.js streams
- [rules/modules.md](rules/modules.md) - ES Modules and CommonJS patterns
- [rules/testing.md](rules/testing.md) - Testing strategies for Node.js applications
- [rules/flaky-tests.md](rules/flaky-tests.md) - Identifying and diagnosing flaky tests with node:test
- [rules/stuck-processes-and-tests.md](rules/stuck-processes-and-tests.md) - Diagnosing processes that do not exit and tests that get stuck
- [rules/node-modules-exploration.md](rules/node-modules-exploration.md) - Navigating and analyzing node_modules directories
- [rules/performance.md](rules/performance.md) - Performance optimization techniques
- [rules/caching.md](rules/caching.md) - Caching patterns and libraries
- [rules/profiling.md](rules/profiling.md) - Profiling and benchmarking tools
- [rules/logging.md](rules/logging.md) - Logging and debugging patterns
- [rules/environment.md](rules/environment.md) - Environment configuration and secrets management
- [rules/graceful-shutdown.md](rules/graceful-shutdown.md) - Graceful shutdown and signal handling
- [rules/typescript.md](rules/typescript.md) - TypeScript configuration and type stripping in Node.js
