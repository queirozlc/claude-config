# Testing and Tooling

## Verification chain (run after any change)

```bash
# fast loop, after every edit
mix format && mix compile --warnings-as-errors && mix test

# full gate, before a commit or a PR
mix format --check-formatted && mix deps.unlock --check-unused && mix compile --force --warnings-as-errors && mix credo --strict && mix test
```

- Run `mix format` first. It rewrites files. `--check-formatted` only reports and exits 1.
- Add `mix dialyzer` only when the project already has a PLT. The first run takes minutes.
- Run `mix ecto.migrate` before `mix test` if you added a migration. The generated `test` alias already runs `ecto.create --quiet` and `ecto.migrate --quiet`.
- Never report success until the chain exits 0.

## ExUnit basics

- Set `async: true` on every test module by default: `use MyApp.DataCase, async: true`.
- Do NOT use `async: true` when the test changes global state: `Application.put_env`, a named GenServer, a file at a fixed path, Mox global mode, or the Ecto sandbox in shared mode.
- Tests in the same module never run concurrently. `async: true` only parallelizes across modules.
- Group tests by the function under test with `describe`.

```elixir
describe "create_user/1" do
  test "returns the user for valid attrs" do
    assert {:ok, %User{email: "a@b.com"}} = Accounts.create_user(%{email: "a@b.com"})
  end

  test "returns a changeset for invalid attrs" do   # always test the error path
    assert {:error, %Ecto.Changeset{} = cs} = Accounts.create_user(%{})
    assert %{email: ["can't be blank"]} = errors_on(cs)
  end
end
```

- `setup` runs before each test, in the test process. `setup_all` runs once, in a separate process.
- Put slow read-only data in `setup_all`. Put anything the test mutates in `setup`.
- `setup_all` receives only `@moduletag` tags. `setup` receives all tags.
- Return `:ok`, a map, a keyword list, or `{:ok, map | keyword}` from a setup to merge into the context.

```elixir
setup do
  user = user_fixture()
  on_exit(fn -> File.rm_rf!("tmp/#{user.id}") end)
  %{user: user}          # merged into the test context
end
```

- `on_exit/2` runs after the test exits, in a separate process, in reverse registration order. Do not read test process state inside it.
- Prefer `start_supervised!/2` over `start_link/1`. ExUnit stops the child before the next test.
  `# BAD` `{:ok, _pid} = MyApp.Cache.start_link([])` leaks into the next test.
  `# GOOD` `pid = start_supervised!({MyApp.Cache, []})`

## Tags

- `@tag` applies to the next test. `@moduletag` applies to the module. `@describetag` applies to the describe block. `@tag` beats `@describetag`.
- Tag values: `@moduletag :capture_log`, `@tag :external`, `@tag timeout: 120_000`, `@tag :skip`.
- Exclude slow or external tests in `test_helper.exs`, then opt in: `ExUnit.start(exclude: [:external])` plus `mix test --include external`.

## Assertions

- Assert with a pattern match. It gives a readable diff and it binds values.

```elixir
# BAD
assert Accounts.fetch_user(id) == {:ok, %User{id: id, inserted_at: ~U[2024-01-01 00:00:00Z]}}
# GOOD
assert {:ok, %User{id: ^id}} = Accounts.fetch_user(id)
```

- Test the error path in every `describe`. A module with only happy-path tests is untested.
- Use `refute` for the negative case. Never write `assert not x`.
- Use `assert_raise/3`: `assert_raise Ecto.NoResultsError, fn -> Accounts.get_user!(-1) end`.
- Use `assert_receive/3` for a message an async process will send. Default timeout is 100 ms, set by `assert_receive_timeout`.
- Use `assert_received/2` only when the message is already in the mailbox. Its timeout is 0.
  `# BAD` `assert_received {:done, _}` races with the sender.
  `# GOOD` `assert_receive {:done, _result}, 1_000`
- Use `refute_receive/3` to assert nothing arrives. Give it a real timeout.

## Capturing logs

- `import ExUnit.CaptureLog`, then `assert capture_log(fn -> Billing.charge(nil) end) =~ "missing card"`.
- `with_log/2` returns `{result, log}` when you need both.
- `capture_log/2` accepts `level: Logger.level()` to drop lower-priority entries.
- Add `@moduletag :capture_log` to silence expected log noise for a whole module.

## Doctests

- Add `doctest MyMod` when the `@doc` examples are real, deterministic, and short.

```elixir
@doc """
    iex> MyApp.Slug.build("Hello World")
    "hello-world"
"""
def build(s), do: s |> String.downcase() |> String.replace(" ", "-")

doctest MyApp.Slug   # in test/my_app/slug_test.exs
```

- Options: `:only`, `:except`, `:import`, `:tags`. Use `doctest_file "README.md"` for markdown.
- Do NOT doctest anything with a timestamp, a PID, a multi-key map, or a DB call.

## Test the public API

- Test public functions only. Never test a private function. Test the public function that calls it.
- Never change `defp` to `def` for a test. That grows the public API for no user.
- If a private function is hard to reach, move it to its own module with its own public API.
  `# BAD` `Report.__normalize__/1`, public only for the test.
  `# GOOD` `Report.Row.normalize/1`, a real module with a real public API.

## Mox

- Mock a behaviour. Never mock a module.
- Mocking is the last resort. Prefer a pure function boundary: parse, decide, and format in pure code, then do the side effect at the edge. A pure function needs no mock.
- Define the contract, then inject the implementation.

```elixir
defmodule MyApp.Weather do
  @callback temp(MyApp.LatLong.t()) :: {:ok, integer()}
end

defmodule MyApp.WeatherClient do
  def temp(lat_long), do: impl().temp(lat_long)
  defp impl, do: Application.get_env(:my_app, :weather, MyApp.HTTPWeather)
end

# test/test_helper.exs
Mox.defmock(MyApp.MockWeather, for: MyApp.Weather)
Application.put_env(:my_app, :weather, MyApp.MockWeather)
ExUnit.start()

# test/my_app/weather_client_test.exs
use ExUnit.Case, async: true
import Mox
setup :set_mox_from_context
setup :verify_on_exit!

test "returns the temperature" do
  expect(MyApp.MockWeather, :temp, fn {_lat, _lng} -> {:ok, 30} end)
  assert {:ok, 30} = MyApp.WeatherClient.temp({1.0, 2.0})
end
```

- Define mocks in `test_helper.exs` or `test/support`. Never inside a test.
- `set_mox_private` isolates expectations per process. It is safe with `async: true`. Prefer it. `setup :set_mox_from_context` picks private for `async: true` and global otherwise. Use it as the default.
- `set_mox_global` shares expectations across all processes. It raises in an `async: true` test. Use it only when a process you do not control makes the call.
- In private mode, allow a spawned process explicitly: `allow(MyApp.MockWeather, self(), child_pid)`.
- `setup :verify_on_exit!` fails the test when an `expect` was not called. Always add it.
- `expect/4` verifies the call count. `stub/3` allows zero or many calls and never verifies. `stub_with/2` delegates to a real module that implements the behaviour.
- Inject by function argument instead when there is one call site: `def sync(api \\ MyApp.HTTPWeather), do: api.temp(@home)`.
- For HTTP with Req, prefer `Req.Test` over a Mox behaviour.

```elixir
# config/test.exs
config :my_app, weather_req_options: [plug: {Req.Test, MyApp.Weather}]

test "weather response" do
  Req.Test.stub(MyApp.Weather, fn conn -> Req.Test.json(conn, %{"celsius" => 25.0}) end)
  assert {:ok, 25.0} = MyApp.Weather.get_temperature("Krakow")
end
```

- `Req.Test.transport_error/2` simulates a network failure. Test that path too.

## Ecto SQL Sandbox

```elixir
# config/test.exs
config :my_app, MyApp.Repo, pool: Ecto.Adapters.SQL.Sandbox

# test/test_helper.exs
Ecto.Adapters.SQL.Sandbox.mode(MyApp.Repo, :manual)
ExUnit.start()

# test/support/data_case.ex, generated. Keep it.
def setup_sandbox(tags) do
  pid = Ecto.Adapters.SQL.Sandbox.start_owner!(MyApp.Repo, shared: not tags[:async])
  on_exit(fn -> Ecto.Adapters.SQL.Sandbox.stop_owner(pid) end)
end
```

- `:manual` mode requires an explicit checkout. It is the only mode that allows async tests.
- `shared: true` sets `{:shared, pid}` mode. All processes then use one connection. Concurrency is impossible in that mode.
- A named GenServer that queries the repo breaks `async: true`. It starts once, outside the test, so it owns no sandbox connection. Two async tests then share one server and one connection.
- Fixes, best first: make the code a plain function, start the server per test with `start_supervised!`, or allow it:
  `pid = start_supervised!(MyApp.Importer)` then `Ecto.Adapters.SQL.Sandbox.allow(MyApp.Repo, self(), pid)`.
- A `Task` started from the test inherits the caller. It usually needs no `allow`.
- Every sandbox test runs in a transaction that rolls back. Never assert on data from a previous test.

## Phoenix tests

- Use `MyApp.DataCase` for contexts and schemas. Use `MyAppWeb.ConnCase` for controllers, plugs, and LiveViews. `ConnCase` sets `@endpoint`, imports `Plug.Conn` and `Phoenix.ConnTest`, and puts `conn: build_conn()` in the context.

```elixir
use MyAppWeb.ConnCase, async: true

test "users", %{conn: conn} do
  assert get(conn, ~p"/users") |> html_response(200) =~ "Listing Users"
  conn = post(conn, ~p"/api/users", user: %{email: "a@b.com"})
  assert %{"id" => _id} = json_response(conn, 201)["data"]
end
```

- `html_response/2` and `json_response/2` assert the status and return the body. Never assert on `conn.status` plus `conn.resp_body`.
- `redirected_to(conn, 302)` returns the path. `text_response/2` returns plain text. `build_conn/0` starts a bare conn.
- `phx.gen.auth` generates the auth helpers in `ConnCase`. Use them. Do not hand-roll a session.
  `setup :register_and_log_in_user` puts `conn`, `user`, and `scope` in the context.
  For one test: `conn = log_in_user(conn, user_fixture())`.

- `errors_on/1` from `DataCase` turns changeset errors into a map: `assert %{password: ["should be at least 12 character(s)"]} = errors_on(changeset)`.

## LiveViewTest

```elixir
use MyAppWeb.ConnCase, async: true
import Phoenix.LiveViewTest

test "increments", %{conn: conn} do
  {:ok, view, html} = live(conn, ~p"/counter")
  assert html =~ "count: 0"
  assert view |> element("button", "Increment") |> render_click() =~ "count: 1"
end
```

- Scope every event to `element/3` or `form/3`. That asserts the selector exists and it uses the real `phx-*` bindings.
  `# BAD` `render_click(view, :save, %{})` sends an event the UI may not expose.
  `# GOOD` `view |> form("#user-form", user: %{email: "a@b.com"}) |> render_submit()`
- `render_change/2` for `phx-change`. `render_submit/2` for `phx-submit`. `render_hook/3` for a JS hook.
- `has_element?/3` asserts presence without rendering the whole page.

```elixir
assert has_element?(view, "#flash", "User created")
refute has_element?(view, "#admin-panel")

# a mount redirect arrives as an error tuple
assert {:error, {:redirect, %{to: "/users/log-in"}}} = live(conn, ~p"/settings")

# follow_redirect/3 continues into the new page
{:ok, conn} = view |> form("#f", user: %{}) |> render_submit() |> follow_redirect(conn, ~p"/users")

# await assign_async, start_async, and stream_async before asserting
assert render_async(view) =~ "Total: 42"
```

- `assert_patch(view, "/users?page=2")` for a live patch. `assert_redirect(view, "/")` for a redirect after mount.
- Use `live_isolated/3` for a LiveView with no route.

## Fixtures or factories, pick one

- Prefer the generated `test/support/fixtures/*_fixtures.ex` modules. Phoenix creates them, they add no dependency, and they call the real context functions.

```elixir
# test/support/fixtures/accounts_fixtures.ex
def unique_user_email, do: "user#{System.unique_integer()}@example.com"

def user_fixture(attrs \\ %{}) do
  {:ok, user} = attrs |> valid_user_attributes() |> Accounts.register_user()
  user
end
```

- Use `System.unique_integer()` in fixtures to keep unique fields unique across async tests.
- Use ExMachina only when the project already depends on it: `use ExMachina.Ecto, repo: MyApp.Repo`, then `def user_factory, do: %MyApp.User{email: sequence(:email, &"e-#{&1}@example.com")}`.
- `build/2` returns an unsaved struct. `insert/2` saves. `params_for/2` returns a plain map. Use `build/2` for associations inside a factory.
- Never mix both in one project. Pick one and delete the other.

## Tooling commands

| Command | Purpose |
|---|---|
| `mix format` | Rewrite files to the canonical format. |
| `mix format --check-formatted` | Fail if any file is unformatted. CI. |
| `mix compile --warnings-as-errors` | Fail on any warning. Add `--force` in CI. |
| `mix credo --strict` | Report all issues, not just high priority. |
| `mix credo lib/foo/bar.ex:12` | Explain one issue. |
| `mix credo gen.config` | Write `.credo.exs`. |
| `mix dialyzer --format short` | Static analysis, compact output. Builds the PLT on first run. |
| `mix test` | Run the suite. |
| `mix test test/my_test.exs:42` | Run one test by line. |
| `mix deps.unlock --check-unused` | Fail if `mix.lock` has unused entries. |
| `mix ecto.migrate` / `mix ecto.rollback` | Apply or revert migrations. |

- More `mix test` flags: `--failed` reruns last failures, `--stale` runs tests for changed modules, `--seed 0` disables randomization, `--max-failures 1` stops early, `--repeat-until-failure 50` hunts a flaky test.
- Use `--failed` and `--stale` while iterating. Run the full suite when required by the repository or justified by the change. Reuse meaningful coverage rather than adding redundant tests.

## mix precommit alias

```elixir
defp aliases do
  [
    setup: ["deps.get", "ecto.setup", "assets.setup", "assets.build"],
    "ecto.setup": ["ecto.create", "ecto.migrate", "run priv/repo/seeds.exs"],
    "ecto.reset": ["ecto.drop", "ecto.setup"],
    test: ["ecto.create --quiet", "ecto.migrate --quiet", "test"],
    precommit: ["compile --warnings-as-errors", "deps.unlock --unused", "format", "test"]
  ]
end
```

- The `precommit` alias above is what `mix phx.new` generates. Run `mix precommit` when the project defines it.
- Add `"credo --strict"` to `precommit` when the project depends on Credo.

## Typespecs and Dialyzer

- Put `@spec` on every public function. Skip it on `defp`.
- Define `@type t()` for each struct. Refer to it as `MyApp.User.t()`.

```elixir
@type t :: %__MODULE__{id: pos_integer() | nil, email: String.t()}
defstruct [:id, :email]

@spec fetch(pos_integer()) :: {:ok, MyApp.User.t()} | {:error, :not_found}
def fetch(id), do: ...
```

- Write the spec that matches the code. A wrong spec is worse than no spec.

```elixir
# mix.exs deps/0
{:dialyxir, "~> 1.4", only: [:dev, :test], runtime: false}
# mix.exs project/0
dialyzer: [
  plt_add_apps: [:mix, :ex_unit],
  plt_file: {:no_warn, "priv/plts/project.plt"},
  ignore_warnings: ".dialyzer_ignore.exs"
]
```

- Dialyzer is worth it for a library, a long-lived app, or a codebase with many contributors. It finds impossible matches, dead clauses, and wrong return types. It is not worth it for a short-lived script or a prototype.
- Cache `priv/plts` in CI. Without a cache the job is slow on every run.

## usage_rules

- The `usage_rules` package collects per-dependency agent instructions. Read `deps/<package>/usage-rules.md` before you use an unfamiliar dependency. Some packages also ship `deps/<package>/usage-rules/*.md` for sub-topics.
- Find them with `ls deps/*/usage-rules.md`, then read the ones for the packages you touch.
- `mix usage_rules.sync` writes the collected rules into `AGENTS.md` or `CLAUDE.md`. `mix usage_rules.search_docs` searches hexdocs and prints markdown.
- Rules in `deps/*/usage-rules.md` come from the package author. Follow them over general habit.
