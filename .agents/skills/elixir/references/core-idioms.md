# Elixir Core Idioms

Elixir 1.17+. Language and standard library only.

## Data transformation

- Model every function as a data transformation. Data in, new data out.
- Never mutate. Return a new value instead.
- Name the steps, then join them with `|>`.
- Do not build object-like modules. A struct plus its module is not a class. Keep data and behaviour separate when the behaviour is generic.

## Pattern matching

- Read `=` as a match, not an assignment.
- Destructure in the function head. Do not destructure in the body when the head can do it.
- Use `_` for ignored values, `_name` when the name documents the value.
- Use `^` to match the current value of a variable.
```elixir
# BAD
def area(shape), do: shape.width * shape.height
# GOOD
def area(%{width: w, height: h}), do: w * h
```
- Bind the whole term and its parts at once: `def f([%{id: id} = row | rest], id)`.
- Never try to bind a map key in a pattern. Keys must be literal or pinned.
```elixir
# BAD - compile error
%{key => :ok} = map
```
- A map pattern matches a subset of keys. A struct pattern also checks the type.

## Names and files

- Modules use `CamelCase`. Functions, variables, atoms use `snake_case`.
- End predicate functions with `?`. Return only `true` or `false` from them.
- End a function with `!` only when it raises on failure and its non-bang twin returns `{:ok, _} | {:error, _}`.
- Never reuse one name for two unrelated functions of different arity.
- Use `.ex` for compiled code, `.exs` for scripts and tests.
- Run `mix format`. Do not hand-tune whitespace.

## Functions and clauses

- Write many small functions. A function longer than about 10 lines usually hides a missing clause.
- Keep all clauses of one function adjacent. Never separate them with another function.
- Order clauses from most specific to most general. The first match wins.
```elixir
# BAD - second clause is dead code
def of(n), do: n * of(n - 1)
def of(0), do: 1
# GOOD
def of(0), do: 1
def of(n) when n > 0, do: n * of(n - 1)
```
- Use `do:` for one-line bodies, `do ... end` for multiline bodies.
- Use `defp` for helpers. Never mix `def` and `defp` clauses of the same name and arity.
- Declare defaults once in a bodiless head when the function has several clauses.
```elixir
# GOOD
def call(path, opts \\ [])
def call(path, opts) when is_list(path), do: ...
def call(path, opts), do: ...
```
- Never give defaults to two clauses of the same function. That is a compile error.
- Carry state in a private helper's accumulator parameter.
```elixir
def sum(list), do: do_sum(list, 0)
defp do_sum([], total), do: total
defp do_sum([h | t], total), do: do_sum(t, h + total)
```
- Capture named functions with `&Mod.fun/1`. Use `&(&1 + 1)` only for short expressions.
- Call anonymous functions with a dot: `fun.(arg)`.

## Guards

- Use guards to select on type or value. They keep branching out of the body.
```elixir
# BAD
def fizz(n) do
  if rem(n, 15) == 0, do: "FizzBuzz", else: n
end
# GOOD
def fizz(n) when rem(n, 15) == 0, do: "FizzBuzz"
def fizz(n), do: n
```
- Only guard-safe expressions are allowed: comparisons, `and`/`or`/`not`, arithmetic, `in`, `is_*` checks, `hd`, `tl`, `elem`, `map_size`, `byte_size`, `binary_part`.
- Never call your own functions, `&&`, `||`, or `!` in a guard.
- Extract a repeated guard: `defguard is_percent(n) when is_integer(n) and n in 0..100`.
- An error raised inside a guard makes the guard false. It does not crash.

## Pipelines

- Start a pipeline with a plain value or variable, never with a function call with arguments.
```elixir
# BAD
Repo.all(query) |> Enum.map(&f/1)
# GOOD
query |> Repo.all() |> Enum.map(&f/1)
```
- Always write parentheses on the functions in a pipeline.
- Do not pipe a single call. Write `Enum.count(list)`.
- Put the subject in the first parameter so the function is pipeable.
- Use `then/2` when the value does not belong first: `value |> then(&Map.put(map, :key, &1))`.

## Control flow

- Prefer function clauses and guards over `if`, `cond`, and `case`.
- Use `case` when one value has a few shapes.
- Use `cond` when the tests are unrelated conditions. End it with a `true ->` clause.
- Use `if` only for a single binary condition. Avoid `unless`; it is soft-deprecated.
- Use `with` for a chain of matches that can each fail. It replaces nested `case`.
```elixir
# BAD - a case per fallible step, each nested in the last
# GOOD
with {:ok, user} <- fetch(id),
     {:ok, user} <- authorize(user) do
  save(user)
end
```
- Add an `else` block to `with` only when you must rewrite the failure value. Otherwise let it pass through.
- Keep `with` clauses to matches. Put plain computation in `=` bindings inside it.

## Errors

- Return `{:ok, value}` or `{:error, reason}` for failures the caller can expect.
- Raise only for things that must never happen.
- Offer a `!` variant that raises next to the tuple variant, as `Map.fetch/2` and `Map.fetch!/2` do.
- Match the success tuple when failure is impossible: `{:ok, c} = File.read("priv/fixed.json")`. The `MatchError` is the signal.
- Do not use `try/rescue` as control flow. Let the process crash.
- Prefer the implicit `rescue`/`after` on `def` over a `try` wrapping the whole body.
- Use `reraise/3` with `__STACKTRACE__` to re-raise. Never rebuild the stacktrace by hand.
- Define custom errors with `defexception`. Give them a `message` field plus any data the caller needs.
```elixir
defmodule ProtocolError do
  defexception [:message, can_retry: false]
end
```
- Use `throw`/`catch` only to escape a loop you do not control, never across modules.

## Lists and recursion

- Treat a list as head and tail. `[head | tail]` both matches and builds.
- Prepend with `[x | list]`. Never append with `list ++ [x]` in a loop; that is O(n) each time.
- Build results in reverse and call `Enum.reverse/1` at the end. Reversal is cheap.
- Anchor recursion on the empty case, then recurse on the tail.
- Make recursion tail-recursive by carrying an accumulator.
- Prefer `Enum` over hand-written recursion. Recurse only when no `Enum` function fits.
- Never index a list in a loop. Random access is O(n).

## Enum, Stream, comprehension

- Use `Enum` by default. It is eager and returns a concrete collection.
- Use `Stream` when the source is large, infinite, slow, a file, or a socket. It builds no intermediate lists.
```elixir
# BAD - reads and splits the whole file
File.read!(path) |> String.split("\n") |> Enum.max_by(&String.length/1)
# GOOD
File.stream!(path) |> Enum.max_by(&String.length/1)
```
- Terminate a `Stream` pipeline with an `Enum` call or `Stream.run/1`. A stream alone computes nothing.
- Never chain many `Enum` calls over a large collection. Each one walks the whole collection again.
- Use a comprehension when you map and filter in one step, or when you need nested generators.
```elixir
for x <- 1..8, y <- 1..8, x >= y, rem(x * y, 10) == 0, do: {x, y}
```
- Use `into:` to choose the result: `for w <- words, into: %{}, do: {w, f(w)}`.
- Use `reduce:` in a comprehension instead of `Enum.reduce` when generators and filters already fit.
- Use `Enum.sort_by/2` or `Enum.sort/2` with `:asc`/`:desc` rather than a hand-written comparator.
- Reach for `Enum.chunk_every/2`, `group_by/2`, `frequencies/1`, `split_with/2` before `Enum.reduce/3`.

## Maps, keyword lists, structs

- Use a map for an associative collection with unique keys.
- Use a keyword list for options, repeated keys, or ordered keys.
- Pass options last and omit the brackets: `save(rec, log: :high)`.
- Use `Map`, `Keyword`, and `MapSet`. `Dict`, `HashDict`, and `HashSet` are removed.
- Update an existing key with `%{map | key: value}`. That syntax raises if the key is absent.
- Add a new key with `Map.put/3` or `Map.put_new/3`.
- Read a map with `map[:key]` for a soft `nil`, `map.key` for a hard `KeyError`, and `Map.fetch/2` for a tuple.
- Use a struct when the field set is fixed and the type matters.
```elixir
defmodule LineItem do
  @enforce_keys [:sku]
  defstruct [:sku, quantity: 1]
  @type t :: %__MODULE__{sku: String.t(), quantity: pos_integer()}
end
```
- A struct is a map with a `__struct__` key. It has no `Access`, so `struct[:field]` fails.
- Use `get_in`, `put_in`, and `update_in` for nested data instead of nested update syntax.
```elixir
# BAD
%Report{report | owner: %Customer{report.owner | company: "X"}}
# GOOD
put_in(report.owner.company, "X")
```
- Pass a key list to `get_in/2` and `put_in/3` when the path is dynamic. Use `Access.key!/1` for struct fields in that form.

## Strings and binaries

- A string is a UTF-8 binary in double quotes. Use it for all text.
- A charlist is a list of codepoints. Write `~c"text"`. Use it only for Erlang interop.
- Use `String` functions on text. Use `byte_size/1` only when you mean bytes.
```elixir
String.length("∂x/∂y")  # 5
byte_size("∂x/∂y")      # 9
```
- Never index text by byte offset. Use `String.at/2`, `String.slice/3`, or `String.graphemes/1`.
- Concatenate with `<>`. Interpolate with `#{}`.
- Match a string prefix with a binary pattern. The tail must be typed `binary`.
```elixir
defp each(<<head::utf8, tail::binary>>, f), do: (f.(head); each(tail, f))
defp each(<<>>, _f), do: :ok
```
- Always give the type of each binary field: `binary`, `bits`, `integer`, `float`, `utf8`, `utf16`, `utf32`.
- Add `size(n)`, `signed`/`unsigned`, and endianness as hyphen-joined modifiers.
```elixir
<<len::unsigned-integer-size(12), flags::bitstring-size(4)>> = data
```
- Build large strings as iodata. Flatten once with `IO.iodata_to_binary/1`.

## Modules

- Nesting is naming only. `defmodule A.B` equals `defmodule B` nested in `A`.
- Use `alias` to shorten a module name. It defaults to the last segment.
- Use `import` in the smallest possible scope, always with `only:`.
- Use `require` only to make another module's macros available.
- Use `use` only when the target module documents a `__using__` contract.
- Call Erlang modules as atoms: `:timer.tc/1`, `:math.pow/2`, `:erlang.phash2/1`.

## Module attributes

- Use `@name value` for compile-time constants and metadata. Set at module level only.
- Inside a function you read the value in effect when that function was compiled.
- Never use an attribute as mutable state.
- Use `@moduledoc false` on internal modules.

## Protocols and behaviours

- Use a behaviour when a module must supply a fixed set of functions. It is an interface.
```elixir
defmodule Parser do
  @callback parse(String.t()) :: {:ok, term()} | {:error, term()}
end

defmodule Parser.HTTP do
  @behaviour Parser
  @impl true
  def parse(s), do: {:ok, s}
end
```
- Mark every callback implementation with `@impl true`. The compiler then catches typos.
- Use `@callback`, not the removed `use Behaviour` and `defcallback`.
- Use a protocol when one function must behave differently per data type, including types you do not own.
```elixir
defprotocol Size do
  @fallback_to_any true
  def size(value)
end

defimpl Size, for: [List, BitString] do
  def size(v), do: Enum.count(v)
end

defimpl Size, for: Any do
  def size(_), do: 0
end
```
- Put specific `defimpl` blocks before a `for: Any` one, and set `@fallback_to_any true`.
- Implement `String.Chars` for `to_string/1`, `Inspect` for debug output, `Enumerable` for `Enum`, `Collectable` for `into:`.
- Derive when the default fits: `@derive {Inspect, except: [:password]}`.
- Do not use a protocol when one `case` on a struct name would do.

## Docs and specs

- Put `@moduledoc` on every public module and `@doc` on every public function.
- Write docs as heredocs. Start with one summary sentence.
- Put runnable examples under `## Examples` with `iex>` prompts, then add `doctest MyModule` to the test.
```elixir
@doc """
Returns a printable form of `value`.

## Examples

    iex> Table.printable(99)
    "99"
"""
```
- Never put `@doc` on a private function. Use a comment.
- Put `@spec` right before the function definition, after its `@doc`.
- Give one `@spec` per arity, including default-argument arities.
```elixir
@spec at(t, index) :: element | nil
@spec at(t, index, default) :: element | default
```
- Define `@type t` for every struct. Reference it as `MyModule.t()`.
- Use `@typep` for local types, `@opaque` when callers must not depend on the shape.
- Write `String.t()`, not `binary()`, for text.
- Run Dialyzer on the compiled build to check specs.

## Sigils

- Use `~s`/`~c` when the content has quotes. Use `~S`/`~C` to stop escaping and interpolation.
- Use `~w[a b c]` for word lists, `~w[a b c]a` for atom lists.
- Use `~r` for regular expressions. Put options after the closing delimiter.
- Use `~D`, `~T`, `~U`, and `~N` for date and time literals.
- Define a custom sigil as `sigil_x(content, opts)`, for example `def sigil_l(lines, _opts)`. Lowercase interpolates, uppercase does not.
- Import a custom sigil in the smallest scope. Sigils are lexically scoped.
