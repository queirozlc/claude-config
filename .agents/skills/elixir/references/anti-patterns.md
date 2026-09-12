# Elixir Anti-Patterns
Source: official Elixir docs (code, design, process, macro anti-patterns), plus `Kernel`, `Task`, `Module`, `Stream` docs for the agent traps.

## Code

### Comments Overuse
Problem: Comments that repeat the code add noise and go stale.
Fix: Use clear names and module attributes. Comment the reason, not the mechanics.
```elixir
# BAD:  unix_now + (60 * 5)   # adds 5 minutes in seconds
# GOOD: @five_min_in_seconds 60 * 5
#       unix_now + @five_min_in_seconds
```
### Complex `else` Clauses in `with`
Problem: One `else` block collects the errors of every clause. You cannot tell which clause failed.
Fix: Normalize each step in a private function that returns a tagged error, then drop the `else`.
```elixir
# BAD
with {:ok, e} <- File.read(p), {:ok, d} <- Base.decode64(e) do
  {:ok, d}
else
  {:error, _} -> {:error, :badfile}
  :error -> {:error, :badencoding}
end
# GOOD: with {:ok, e} <- file_read(p), {:ok, d} <- base_decode64(e), do: {:ok, d}
```
### Complex Extractions in Clauses
Problem: The head extracts many fields. The reader cannot separate matching from body use.
Fix: Match only what guards and dispatch need. Extract the rest in the body.
```elixir
# BAD
def drive(%User{name: name, age: age}) when age >= 18, do: "#{name} can drive"
# GOOD
def drive(%User{age: age} = user) when age >= 18 do
  %User{name: name} = user
  "#{name} can drive"
end
```
### Dynamic Atom Creation
Problem: Atoms from external input are never garbage collected. They exhaust the VM atom table.
Fix: Map known strings with function clauses, or use `String.to_existing_atom/1`.
```elixir
# BAD:  %{status: String.to_atom(status)}
# GOOD: defp convert_status("ok"), do: :ok
#       defp convert_status("error"), do: :error
```
### Long Parameter List
Problem: Many parameters are hard to order and easy to swap at the call site.
Fix: Group related parameters into a map, struct, or keyword list.
```elixir
# BAD:  def loan(user_name, email, password, user_alias, book_title, book_ed)
# GOOD: def loan(%User{} = user, %Book{} = book)
```
### Namespace Trespassing
Problem: A package defines modules under another package namespace. The VM loads one module per name, so the names collide.
Fix: Prefix every module with your package name.
```elixir
# BAD:  defmodule Plug.Auth do
# GOOD: defmodule PlugAuth do
```
### Non-Assertive Map Access
Problem: `map[:key]` returns `nil` for a required key. The `nil` travels far from the real fault.
Fix: Use `map.key` for required keys. Keep `map[:key]` for optional keys.
```elixir
# BAD:  {point[:x], point[:y], point[:z]}
# GOOD: {point.x, point.y, point[:z]}
```
### Non-Assertive Pattern Matching
Problem: Defensive code returns a wrong value instead of crashing. The bug hides.
Fix: Match the expected shape. Let bad input crash at the source.
```elixir
# BAD:  Enum.at(kv, 0) == key && Enum.at(kv, 1)
# GOOD: [k, v] = String.split(pair, "=")
#       k == key && v
```
### Non-Assertive Truthiness
Problem: `&&`, `||`, and `!` accept any term. They hide a non-boolean operand.
Fix: Use `and`, `or`, and `not` when both sides must be booleans.
```elixir
# BAD:  if is_binary(name) && is_integer(age) do
# GOOD: if is_binary(name) and is_integer(age) do
```
### Structs with 32 Fields or More
Problem: At 32 keys or more a map changes to the hash map representation. It loses key sharing and uses more memory.
Fix: Nest optional or related fields into a child map or struct.
```elixir
# BAD:  defstruct [:f1, :f2, ..., :f35]
# GOOD: defstruct [:f1, :f2, metadata: %{}]
```

## Design

### Alternative Return Types
Problem: An option changes the return type. The caller cannot know the shape from the call.
Fix: Define one function per return type.
```elixir
# BAD:  def parse(string, opts \\ [])   # integer or tuple
# GOOD: def parse(string)
#       def parse_discard_rest(string)
```
### Boolean Obsession
Problem: Several boolean options encode states that overlap or conflict.
Fix: Use one option that holds an atom per state.
```elixir
# BAD:  cond do
#          opts[:admin] -> ...
#          opts[:editor] -> ...
#        end
# GOOD: case Keyword.get(opts, :role, :default) do
#          :admin -> ...
#          :editor -> ...
#        end
```
### Exceptions for Control-Flow
Problem: `try/rescue` handles an expected failure. The success path and the error path split apart.
Fix: Return `{:ok, value}` or `{:error, reason}` and match on it. Keep `!` for truly exceptional cases.
```elixir
# BAD:  try do IO.puts(File.read!(f)) rescue e -> ... end
# GOOD: case File.read(f) do
#          {:ok, bin} -> IO.puts(bin)
#          {:error, reason} -> IO.puts(:stderr, "error")
#        end
```
### Primitive Obsession
Problem: A string or plain map holds a domain concept. The structure stays implicit and validation spreads.
Fix: Define a struct for the concept.
```elixir
# BAD:  def extract_postal_code(address) when is_binary(address)
# GOOD: defstruct [:street, :city, :postal_code]
#       def extract_postal_code(%Address{} = a), do: a.postal_code
```
### Unrelated Multi-Clause Function
Problem: One name holds clauses for unrelated business rules. The purpose of the function is unclear.
Fix: Split into functions with specific names.
```elixir
# BAD:  def update(%Product{}) / def update(%Animal{})
# GOOD: def update_product(%Product{}) / def update_animal(%Animal{})
```
### Using Application Configuration for Libraries
Problem: A library reads the global application environment. Two callers cannot configure it differently.
Fix: Take configuration as a function argument or keyword list.
```elixir
# BAD:  parts = Application.fetch_env!(:app_config, :parts)
# GOOD: def split(s, opts \\ []), do: String.split(s, "-", parts: Keyword.get(opts, :parts, 2))
```

## Process

### Code Organization by Process
Problem: A process wraps plain logic. It adds a bottleneck and a message protocol for no runtime need.
Fix: Use modules and functions. Add a process only for state, concurrency, or fault isolation.
```elixir
# BAD:  def add(a, b, pid), do: GenServer.call(pid, {:add, a, b})
# GOOD: def add(a, b), do: a + b
```
### Scattered Process Interfaces
Problem: Many modules call the same process directly. No module owns the data format.
Fix: Put all interaction with the process in one module and export a clear API.
```elixir
# BAD:  Agent.update(pid, fn _ -> 123 end)      # module A
#       Agent.update(pid, fn c -> %{a: c} end)  # module B
# GOOD: def put(b, k, v), do: Agent.update(b, &Map.put(&1, k, v))
```
### Sending Unnecessary Data
Problem: A message is copied in full to the receiver. A big term costs memory and time.
Fix: Extract the needed fields before you send or spawn.
```elixir
# BAD:  spawn(fn -> log_request_ip(conn) end)
# GOOD: ip = conn.remote_ip
#       spawn(fn -> log_request_ip(ip) end)
```
### Unsupervised Processes
Problem: A long running process starts outside a supervision tree. It has no restart and no ordered shutdown.
Fix: Start it under a supervisor in the application tree.
```elixir
# BAD:  Counter.start_link()
# GOOD: Supervisor.start_link([Counter], strategy: :one_for_one)
```

## Macro

### Compile-Time Dependencies
Problem: A macro that injects a module reference creates a compile-time dependency. One change recompiles many files.
Fix: Expand literals in the caller context so the dependency becomes a runtime dependency.
```elixir
# BAD:  defmacro plug(mod), do: quote(do: @plugs unquote(mod))
# GOOD: mod = Macro.expand_literals(mod, %{__CALLER__ | function: {:call, 2}})
```
### Large Code Generation
Problem: A macro expands a large body at every call site. Compile time and artifact size grow.
Fix: Keep the quote small. Call a normal function that does the work.
```elixir
# BAD:  quote do: (if not is_binary(unquote(route)), do: raise ArgumentError, "...")
# GOOD: quote do: Routes.__define__(__MODULE__, unquote(route), unquote(handler))
```
### Unnecessary Macros
Problem: A macro does work that a function can do. It costs readability and traceability.
Fix: Write a function.
```elixir
# BAD:  defmacro sum(a, b), do: quote(do: unquote(a) + unquote(b))
# GOOD: def sum(a, b), do: a + b
```
### `use` Instead of `import`
Problem: `use` runs arbitrary code in the caller. The reader cannot see what it injects.
Fix: Prefer `import` and `alias`. Keep `use` for real setup and document what it injects.
```elixir
# BAD:  use Library
# GOOD: import Library
```
### Untracked Compile-Time Dependencies
Problem: `Module.concat/2` builds a name at runtime. The compiler cannot track it and skips recompilation.
Fix: Write static module names, or build the name at compile time in a macro with `unquote/1`.
```elixir
# BAD:  Module.concat(OtherModule, part).example()
# GOOD: for mod <- [OtherModule.Foo, OtherModule.Bar], do: mod.example()
```

## Agent traps

### `if`/`else` Where Clauses Fit
Problem: A chain of `if` or `cond` tests the shape of a term. Elixir dispatches on shape in the function head.
Fix: Write multi-clause functions with patterns and guards.
```elixir
# BAD:  def area(s), do: if s.type == :circle, do: ..., else: ...
# GOOD: def area(%Circle{r: r}), do: :math.pi() * r * r
#       def area(%Square{a: a}), do: a * a
```
### `try/rescue` as Control Flow
Problem: The generator calls the `!` variant and rescues it. This is Exceptions for Control-Flow.
Fix: Call the non-bang function and match `{:ok, _}` or `{:error, _}`.
### Atoms from External Input
Problem: `String.to_atom/1` on request data leaks memory. Atoms are not garbage collected and the atom table has a hard limit. The VM crashes when the table fills.
Fix: Use `String.to_existing_atom/1`, or map known values with function clauses. Keep external data as strings.
```elixir
# BAD:  String.to_atom(params["sort_by"])
# GOOD: String.to_existing_atom(params["sort_by"])
```
### Eager `Enum` on a Large or Streamed Source
Problem: `Enum` is eager. It loads every row and builds an intermediate list per step.
Fix: Use `Stream` for large sources. Run a repo stream inside its transaction.
```elixir
# BAD:  Repo.all(q) |> Enum.map(&f/1) |> Enum.filter(&g/1)
# GOOD: Repo.stream(q) |> Stream.map(&f/1) |> Stream.filter(&g/1) |> Enum.to_list()
```
### Nested `Enum` for a Join
Problem: `Enum.find` inside `Enum.map` scans the second list once per element. The cost is O(n*m).
Fix: Index the second list with `Map.new/2`, then look up in one pass. Or join in the database.
```elixir
# BAD:  Enum.map(orders, fn o -> Enum.find(users, &(&1.id == o.user_id)) end)
# GOOD: by_id = Map.new(users, &{&1.id, &1})
#       Enum.map(orders, &Map.fetch!(by_id, &1.user_id))
```
### GenServer as a Mutable Variable
Problem: A GenServer holds a value that one caller uses. It adds a serialization point and copies. This is Code Organization by Process.
Fix: Pass the value through function arguments and return values.
### Structural Comparison of Structs
Problem: `<`, `>`, `min`, `max`, and default sort use term order. `~D[2017-03-31] > ~D[2017-04-01]` returns `true` because `:day` is compared before `:month`.
Fix: Use the `compare/2` function of the type. Pass the module to `Enum.sort/2` and `Enum.max/2`.
```elixir
# BAD:  if date1 > date2 do
# GOOD: if Date.compare(date1, date2) == :gt do
#       Enum.sort(dates, Date)
```
### `length/1` in a Loop or Guard
Problem: `length/1` walks the whole list. A check per iteration turns O(n) into O(n^2).
Fix: Match on `[]` and `[head | tail]`. Use `== []` for an empty test.
```elixir
# BAD:  def sum(list) when length(list) == 0, do: 0
# GOOD: def sum([]), do: 0
#       def sum([h | t]), do: h + sum(t)
```
### `++` in an Accumulator
Problem: The cost of `a ++ b` is proportional to `length(a)`. Appending in a loop is quadratic.
Fix: Prepend with `[element | acc]`, then call `Enum.reverse/1`.
```elixir
# BAD:  Enum.reduce(l, [], fn x, acc -> acc ++ [f.(x)] end)
# GOOD: l |> Enum.reduce([], fn x, acc -> [f.(x) | acc] end) |> Enum.reverse()
```
### `Task.async` Without `await`
Problem: `Task.async/1` always sends a reply. Without `await` the message stays in the mailbox. The task is also linked, so a task crash kills the caller.
Fix: Always await an async task. Use `Task.Supervisor.start_child` for fire and forget. Use `Task.Supervisor.async_nolink` when a failure must not kill the caller.
```elixir
# BAD:  Task.async(fn -> send_email(u) end)
# GOOD: Task.async(fn -> send_email(u) end) |> Task.await()
#       Task.Supervisor.start_child(MyApp.TaskSup, fn -> send_email(u) end)
```
### Missing `@impl`
Problem: Without `@impl` the compiler does not check that the function is a real callback. A typo in a callback name compiles clean.
Fix: Add `@impl true` or `@impl Behaviour` to every callback. If one callback carries it, all callbacks of that behaviour must carry it.
```elixir
# BAD:  def handle_call(msg, from, state)
# GOOD: @impl true
#       def handle_call(msg, from, state)
```
### Catch-All `_ ->` That Hides Errors
Problem: A final `_ -> ...` clause swallows a shape the code does not expect. The failure appears later with no cause.
Fix: List the expected clauses. Let an unknown shape raise `CaseClauseError`. Add a catch-all only when you handle it on purpose.
```elixir
# BAD:  case call() do {:ok, v} -> v; _ -> nil end
# GOOD: case call() do
#         {:ok, v} -> v
#         {:error, r} -> handle(r)
#       end
```
