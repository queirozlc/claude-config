# Metaprogramming in Elixir

## Do not write a macro

The default answer is a function. A macro is a last resort.

Before you write `defmacro`, the case must pass ALL of these tests. If one test
fails, write a function.

1. **Deferred evaluation.** The code needs an unevaluated argument. A function
   evaluates every argument first. `if`, `unless`, and `assert` need macros.
   Business logic does not.
2. **Compile-time knowledge.** The value is known at compile time and must be
   burned into the BEAM file. Example: clauses generated from a static data file.
3. **No function can do it.** You tried `import`, higher-order functions, a
   behaviour, a protocol, and plain data first. All failed.
4. **Less code, not moved code.** The macro must remove real boilerplate.
5. **The caller can read the result.** You ran `Macro.to_string/1` on the output
   and the code is simple.
6. **You can test it.** The logic lives in normal functions a test calls
   directly.

Reject these reasons. None of them justifies a macro.

- "It reads nicer." Use a function with a good name.
- "It saves typing." Use `import` or a helper module.
- "I want a mix-in." Use `import` or `defdelegate`. Never `use`.
- "It is faster." Measure first. Most macros do not change runtime cost.
- "The framework does it." A framework hides complexity from many users. Your
  module has few users.

Costs you accept: stack traces point at generated code; dialyzer and the
language server see less, so errors move to runtime; `grep` no longer finds the
definition; every caller recompiles when the macro changes; a reader must expand
the macro in their head.

Try these first:

```elixir
import StringTransforms      # mix-in of functions, not `use`
@behaviour MyApp.Storage     # a contract
defimpl Jason.Encoder, for: MyStruct   # polymorphism on data
```

If you must generate code, generate the smallest body. Make that body call a
normal function in your module at once.

## AST, quote, unquote

Every expression is a 3-tuple `{form, metadata, arguments}`. Literals stay as
themselves. Use `quote` to build an AST. Use `unquote` to inject a value from
macro scope. Inspect source with `Code.string_to_quoted!/1`. Read generated code
with `Macro.to_string/1`.

```elixir
quote do: 1 + 2   #=> {:+, [context: Elixir, imports: [...]], [1, 2]}

defmacro double(n), do: quote(do: unquote(n) * 2)
```

`quote` runs at compile time. The block it returns runs in the caller at
runtime. Keep this split clear at all times.

## bind_quoted

Use `bind_quoted` when you inject an argument more than once. A repeated
`unquote` evaluates the caller expression more than once.

```elixir
quote do: [IO.inspect(unquote(expr)), unquote(expr)]      # wrong: runs twice
quote bind_quoted: [expr: expr], do: [IO.inspect(expr), expr]   # right: once
```

`bind_quoted` disables `unquote` in the block. Pass `unquote: true` to `quote`
if you still need it.

## Hygiene

Variables, imports, and aliases from a macro do not leak into the caller. This
default is correct.

```elixir
defmacro bind_name(str), do: quote(do: name = unquote(str))  # caller safe
quote do: var!(conn) = build_conn()                          # avoid
```

Do not use `var!`. It rewrites a variable in the caller scope, and the call site
does not show it. Use `var!` only when the DSL documents the variable name in public, as
`Plug.Conn` and `ExUnit` do. Return a value instead whenever you can.

## defmacro, defmacrop, expansion

Export with `defmacro` only when an outside caller uses it. Use `defmacrop` for
a private helper. A helper that takes no unevaluated argument must be a plain
private function.

```elixir
quote(do: MyMod.my_macro(1)) |> Macro.expand_once(__ENV__) |> Macro.to_string()
```

Use `Macro.prewalk/2` and `Macro.postwalk/2` to rewrite an AST at compile time,
so the runtime does no extra work.

## __using__ and use

`use M` calls `require M` and then `M.__using__(opts)`. Keep the injected block
tiny. Delegate at once.

```elixir
defmodule Emailer do
  defmacro __using__(config) do
    quote do
      def send_email(to, subject, body) do
        Emailer.send_email(unquote(config), to, subject, body)
      end
    end
  end

  def send_email(config, to, subject, body), do: # real work here
end
```

- Inject imports, aliases, attributes, and hooks. Do not inject function bodies.
- Never inject dozens of functions. That is `import` misused as a mix-in.
- Keep logic in the library module. Stack traces then point at your code, and
  tests call the function directly.
- Validate `opts` at compile time. Raise a clear error.

## Compile-time hooks

`@before_compile` injects code after the module body runs. Use it to read
accumulated attributes.

```elixir
defmacro __using__(_) do
  quote do
    Module.register_attribute(__MODULE__, :tests, accumulate: true)
    @before_compile unquote(__MODULE__)
  end
end

defmacro __before_compile__(_env) do
  quote do: def all_tests, do: @tests
end
```

Other hooks: `@after_compile`, `@on_definition`, `@after_verify`. Use
`@before_compile` first. It covers most needs. Each read of an attribute copies
its value into the bytecode. Do not put a large term in an attribute that many
functions read.

## Pseudo variables

`__MODULE__`, `__ENV__`, `__DIR__`, and `__CALLER__` come from
`Kernel.SpecialForms`. You cannot override them. `__CALLER__` works only in a
macro. Inside `quote`, write `unquote(__MODULE__)` for your own module. A bare
`__MODULE__` resolves in the caller.

## Code generation from external data

This is the strongest legitimate use. Read data at compile time. Emit function
clauses. The BEAM pattern matcher does the lookup at runtime.

```elixir
defmodule Mime do
  @external_resource path = Path.join(__DIR__, "mimes.txt")

  for line <- File.stream!(path) do
    [type, exts] = line |> String.trim() |> String.split("\t")
    def exts_from_type(unquote(type)), do: unquote(String.split(exts))
  end

  def exts_from_type(_type), do: []
end
```

- Use `@external_resource` so `mix` recompiles when the file changes.
- Use unquote fragments (`def unquote(name)()`) to name functions from data.
- Always add a catch-all clause last.
- Do this with `for` in the module body. No `defmacro` is needed.

## Legitimate uses you will meet

- `use MyAppWeb, :controller`. One `__using__` per role. Each block holds
  `import`, `alias`, and `plug` lines only.
- Compile-time validation. Raise in the macro when a required option is missing.
- A small DSL for a domain with real notation: routes, queries, HTML, schemas.
- Generating clauses from a data list, as above.
- Deferred evaluation: assertions, logging that must not evaluate its argument.

## Testing macros

- Test the plain functions the macro delegates to. This is most of the work.
- Add one integration test that defines a small module with `use` and calls it.
- Keep the number of test modules low. Modules slow the suite.
- Assert on behavior, not on AST shape, unless the AST is the product.
- Use `Macro.to_string/1` in a failing test to see what you generated.

## Traps checklist

- `unquote` used twice on one argument. Runtime work runs twice. Use
  `bind_quoted`.
- `var!` in a public macro. The caller cannot see the binding.
- `__using__` that injects many functions. Use `import`.
- A macro that hides a network call or a database query. The call site looks
  free and is not.
- A macro used only for terse syntax. Delete it.
- Generated code with no `@doc` and no `@spec`. Tooling and dialyzer go blind.
- `Application.get_env/2` read in a macro. The value freezes at compile time.
  Use `Application.compile_env/2` and state the intent.
