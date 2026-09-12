# OTP, Processes, and Fault Tolerance

## Decision table: do you need a process?

Most code needs NO process. A process is a unit of concurrency, isolation, or state.
It is not a unit of code organization. Default to a plain module with plain functions.

| Need | Use |
|---|---|
| Transform data, no state, no concurrency | Plain function. Covers most code. |
| Run one side job, get the result | `Task.async/await`. Links to the caller. |
| Run N jobs over a collection | `Task.async_stream/3` with `max_concurrency` and `on_timeout`. |
| Fire and forget work, supervised | `Task.Supervisor.start_child/2`. Not linked. |
| Long lived state plus a custom protocol | `GenServer`. The workhorse. |
| Long lived state, get/update only | `Agent`. Rare. Prefer ETS or GenServer. |
| Look up a process by a non atom key | `Registry` with `:via` tuples. |
| Shared read heavy state, many readers | ETS table. |
| Children started on demand, count unknown | `DynamicSupervisor`. |

## Process basics

Processes share no memory. Every message is deep copied. A closure passed to `spawn`
copies the variables it captures. Binaries over 64 bytes live on a shared heap and are
not copied.

Send a key, not a payload. Never use `spawn/1` in production. OTP compliant processes
log crashes with detail and fit in a supervision tree.

```elixir
# BAD
spawn(fn -> do_work(arg) end)
# GOOD
Task.Supervisor.start_child(MyApp.TaskSupervisor, fn -> do_work(arg) end)
```

## GenServer: call vs cast

Prefer `handle_call`. Start with a call. Switch to a cast only after you measure a problem.

- A call blocks the caller and returns the outcome. It applies back pressure, so a client
  cannot outrun the server.
- A cast is fire and forget. No delivery guarantee, no outcome. Clients can flood the
  unbounded mailbox until the VM runs out of memory.

```elixir
# BAD: a write that must not be lost
def store(k, v), do: GenServer.cast(__MODULE__, {:store, k, v})
# GOOD
def store(k, v), do: GenServer.call(__MODULE__, {:store, k, v})
```

Never block in a callback. The server handles one message at a time.

```elixir
# BAD: the whole server stalls for every client
def handle_call({:fetch, url}, _from, state), do: {:reply, HTTP.get(url), state}
# GOOD: reply later from a task
def handle_call({:fetch, url}, from, state) do
  Task.start(fn -> GenServer.reply(from, HTTP.get(url)) end)
  {:noreply, state}
end
```

## Never put business logic in a callback

A callback is plumbing. Keep domain logic in pure functions in a separate module, and
test that module without starting a process.

```elixir
# BAD
def handle_call({:add, e}, _from, state) do
  e = Map.put(e, :id, state.next_id)
  {:reply, :ok, %{state | entries: [e | state.entries], next_id: state.next_id + 1}}
end
# GOOD
def handle_call({:add, e}, _from, state), do: {:reply, :ok, TodoList.add_entry(state, e)}
```

Run all transformations first. Persist or publish only after they all succeed.

## Timeouts

`GenServer.call/3` defaults to 5000 ms and exits the caller on timeout.

- Set an explicit timeout when the work can be slow. Use `:infinity` only when the call
  must never be abandoned.
- A timeout does not cancel the server work. A late reply arrives as a stray message.
- Never raise the client timeout to hide a slow server. Fix the server.

Keep `init/1` fast. A slow `init/1` blocks the whole supervisor start.

```elixir
def init(arg), do: {:ok, arg, {:continue, :load}}
def handle_continue(:load, arg), do: {:noreply, load_state(arg)}
```

## Mailboxes and unmatched messages

A mailbox is unbounded, limited only by memory. Unmatched messages stay there forever.
They waste memory and slow every later scan. Add a catch all `handle_info/2`.

```elixir
def handle_info(msg, state) do
  Logger.warning("unexpected message: #{inspect(msg)}")
  {:noreply, state}
end
```

## Avoid the single process bottleneck

A process is sequential. Many clients on one process serialize. Under load the server
also competes for CPU with every other process, so throughput drops further.

Fix in this order:

1. Make message handling faster. Move the slow call out of the callback.
2. Move read only state to ETS so readers never touch the process.
3. Split the state across many processes, one per key.
4. Parallelize. This is the last resort. It does not fix a bad algorithm.

## ETS

Use ETS when many processes read shared state and one process is the bottleneck. Do not
reach for it first. Prefer immutable data and processes.

```elixir
:ets.new(:cache, [:named_table, :set, :public, read_concurrency: true])
```

- Do lookups in the client process, not in the owner.
- Keep writes in one process when you need consistency. ETS is atomic per row only.
- Set `read_concurrency: true` or `write_concurrency: true` to match the access pattern.
- The table dies with its owner. Own it from a supervised, long lived process.
- Data is copied in and out. Large rows can be slower than plain maps.
- ETS data cannot be sent to another node. It makes distribution harder.
- Persist state in ETS across restarts only for error kernel processes.

## Registry and name registration

Register under an atom name only for singletons. Never build an atom from user input.
Atoms are never garbage collected.

```elixir
defp via(name), do: {:via, Registry, {MyApp.Registry, name}}
def start_link(name), do: GenServer.start_link(__MODULE__, name, name: via(name))
def add(name, entry), do: GenServer.call(via(name), {:add, entry})
```

`Registry` uses ETS, so lookups are concurrent, and it removes entries when a process dies.
Never store a pid for a long time. A restarted process gets a new pid. Look it up by name.
Never use `:global` or a mutable global store. State belongs to one process, or to one
ETS table with one writer.

## Links, monitors, and trap_exit

- A link is bidirectional. An abnormal exit takes down the linked process. Use
  `start_link` everywhere in a supervision tree, so a supervisor can stop a whole subtree
  with no dangling processes.
- A monitor is unidirectional and delivers a `:DOWN` message. Use it when you depend on a
  process but must not die with it.
- `GenServer.call/3` sets up a temporary monitor, so a server crash exits the caller.

`Process.flag(:trap_exit, true)` caveats:

- It converts exit signals into `{:EXIT, pid, reason}` messages that you must handle.
- Trap exits only when the process must clean up or must supervise. Never by default.
- A trapping process no longer dies with its links. It can leak or hang the tree.
- `terminate/2` runs only if the process traps exits, stops itself, or is shut down by its
  supervisor within the shutdown window.
- `Process.exit(pid, :kill)` cannot be trapped. Always have a supervision plan.
- Never use `terminate/2` for critical persistence. It is not guaranteed to run.

## Supervisors and child specs

Every process belongs in a supervision tree. That is how the system stops cleanly.

```elixir
defmodule MyApp.Supervisor do
  use Supervisor

  def start_link(arg), do: Supervisor.start_link(__MODULE__, arg, name: __MODULE__)

  @impl true
  def init(_arg) do
    children = [
      {Registry, keys: :unique, name: MyApp.Registry},
      MyApp.Database,
      {DynamicSupervisor, name: MyApp.ServerSupervisor, strategy: :one_for_one}
    ]

    Supervisor.init(children, strategy: :one_for_one)
  end
end
```

`use GenServer` generates `child_spec/1`. Override it only when the defaults are wrong.

```elixir
def child_spec(arg) do
  %{id: {__MODULE__, arg.name}, start: {__MODULE__, :start_link, [arg]},
    restart: :transient, shutdown: 10_000, type: :worker}
end
```

## Restart strategies

Ask one question: if this child crashes, what must happen to its siblings?

- `:one_for_one` — restart only the crashed child. The default.
- `:one_for_all` — the siblings cannot work without it. Restart all.
- `:rest_for_one` — later children depend on it, earlier ones do not.

Order the child list by dependency. A registry goes before every process that uses it.

## Restart type

- `:permanent` — always restart. The default. Use for services that must always run.
- `:transient` — restart only on abnormal exit. Use for a worker that may finish normally,
  such as a per user session that idles out.
- `:temporary` — never restart. Use for a connection or request handler, where a restart
  cannot recover anything. Keep it supervised so shutdown stays clean.

```elixir
# a socket handler: restarting cannot revive the closed connection
use GenServer, restart: :temporary
```

## Restart frequency and shutdown

A supervisor gives up after `max_restarts` (default 3) in `max_seconds` (default 5).
It then terminates itself and its children, and the failure escalates up the tree.
This is the design. Recover locally, escalate when local recovery fails.
Never raise the limits to silence a crash loop. Fix the cause.

- The default child shutdown is 5000 ms, then a brutal kill.
- Use `shutdown: :infinity` for a supervisor child.
- Use `shutdown: :brutal_kill` when there is nothing to clean up.

## DynamicSupervisor

Use it when the children are not known up front.

```elixir
case DynamicSupervisor.start_child(MyApp.ServerSupervisor, {MyApp.Server, name}) do
  {:ok, pid} -> pid
  {:error, {:already_started, pid}} -> pid
end
```

Pair it with a `Registry` so a restarted child stays reachable under the same name.
Use `PartitionSupervisor` when one `DynamicSupervisor` becomes the bottleneck.

## Task and Task.async_stream

`Task.async/await` links the task to the caller. A task crash kills the caller. That is
correct when the caller cannot continue without the result.

Always set `max_concurrency` and `on_timeout` on `Task.async_stream`.

```elixir
# BAD: unbounded concurrency, default 5s timeout kills the caller
ids |> Task.async_stream(&fetch/1) |> Enum.to_list()

# GOOD
ids
|> Task.async_stream(&fetch/1,
     max_concurrency: 10,
     timeout: :timer.seconds(30),
     on_timeout: :kill_task,
     ordered: false)
|> Enum.reduce([], fn
     {:ok, result}, acc -> [result | acc]
     {:exit, _reason}, acc -> acc
   end)
```

Use `ordered: false` when order does not matter. Use
`Task.Supervisor.async_stream_nolink/4` when a task crash must not kill the caller.

## Let it crash

Let it crash means: do not write defensive code for errors you cannot handle.
It does not mean let everything crash. Handle an error explicitly in two cases only:
you have a meaningful action for it, or the process is in the error kernel.

```elixir
# GOOD: the expected cases are handled, anything else crashes on purpose
case File.read(path) do
  {:ok, contents} -> :erlang.binary_to_term(contents)
  {:error, :enoent} -> nil
end
```

Use `File.write!/2` when a failed write means the worker failed. Fail fast. Never wrap a whole callback in `try/rescue` to keep a process alive, except in the error
kernel. Keep error kernel code small. Split the state holder from the worker.

## State and restarts

A restart discards the state and the mailbox. That is a feature. A clean slate often fixes
the bug that caused the crash. Persist state across restarts only when you must, because
persisted bad state creates a permanent crash loop. Save only after all transformations
complete.

## OTP applications

- One application per deployable component. `mod:` names the module that starts the
  top level supervisor.
- Read runtime values in `config/runtime.exs`. `config/config.exs` is compile time.
- Never read Application env into a module attribute. That freezes it at compile time.

```elixir
@port Application.compile_env(:my_app, :port)          # BAD: frozen at compile time
defp port, do: Application.fetch_env!(:my_app, :port)  # GOOD
```

- Add `:runtime_tools` to `extra_applications` so `:observer` can attach remotely.
- Use `mix release` for deployment. Set `RELEASE_COOKIE` and a stable node name.

## Distribution

- A process is the distribution primitive. `send`, `GenServer.call`, links, and monitors
  work across nodes with the same code.
- Reach a remote registered process with `{:name, :node@host}`. Use calls, not casts.
  A cast over a broken link is lost silently.
- Links and monitors fire on node loss with reason `:noconnection`.
- `:rpc.call/4` returns a remote result. `Node.spawn` does not.
- Plan for netsplits. During a partition you get consistency or availability, not both.
  A quorum of `2F + 1` nodes is the simple way to build a CP cluster.
- Avoid `:global` locks. Synchronize through processes. Use a lock only to avoid copying
  a large payload across the network.

## Observability

- Never rely on a step debugger for a concurrent system. Use logging and tracing.
- `Logger` captures OTP crash reports with stack traces. Read them first.
- Inspect a live node with `Process.list/0`, `Process.info/2`, `:erlang.memory/0`.
- Watch `:message_queue_len` on long lived processes. Growth means the process is behind.
- Run `:observer` from a hidden local node. Use `:sys.get_state/1`, `:sys.trace/2`, and
  `:sys.statistics/2` on any OTP process. Use `:recon` for production safe inspection.
- Never enable an untargeted `:dbg` trace on a busy production node.
