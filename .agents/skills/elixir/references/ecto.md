# Ecto reference

Target: Ecto v3.14.2, ecto_sql v3.14.0. Verified against hexdocs. Do not use an API that is not listed here without checking the docs.

## Schemas

- Keep schemas dumb. Declare fields, types, and associations only. Put logic in context modules.
- Never call the Repo from a schema module.
- Set `@primary_key` explicitly when the key is not a serial integer. Set `@foreign_key_type` too, or `belongs_to` still uses `:id`.
- Use `:utc_datetime_usec` timestamps. The default is `:naive_datetime`, which drops the time zone.
- Mark secrets `redact: true`. Mark non-persisted fields `virtual: true`.

```elixir
defmodule MyApp.Accounts.User do
  use Ecto.Schema

  @primary_key {:id, :binary_id, autogenerate: true}
  @foreign_key_type :binary_id
  @timestamps_opts [type: :utc_datetime_usec]

  schema "users" do
    field :email, :string
    field :password, :string, virtual: true, redact: true
    field :status, Ecto.Enum, values: [:active, :inactive, :pending]
    belongs_to :org, MyApp.Accounts.Org
    has_many :posts, MyApp.Blog.Post
    timestamps()
  end
end
```

- Use `Ecto.Enum` instead of raw strings. Use `values: [admin: "Administrator"]` when the stored string differs from the atom.
- Use `embedded_schema` for data with no table. It has no `__meta__`.
- Use `embeds_one` / `embeds_many` for owned data in a `map` or `jsonb` column. Always set `:on_replace`, for example `embeds_many :items, Item, on_replace: :delete`.

- Field options: `:default`, `:source` (other column name), `:load_in_query`, `:writable` (`:always` | `:insert` | `:never`).
- Types: `:id`, `:binary_id`, `:string`, `:integer`, `:float`, `:decimal`, `:boolean`, `:binary`, `:map`, `{:array, t}`, `:date`, `:time(_usec)`, `:naive_datetime(_usec)`, `:utc_datetime(_usec)`.

## Changesets

- Write one changeset function per use case. Name it after the use case.
- Do not write one god changeset with option flags.

```elixir
def changeset(user, attrs, opts \\ [])   # BAD: branches on opts[:admin?], opts[:step]
def registration_changeset(user, attrs)  # GOOD
def password_changeset(user, attrs)      # GOOD
```

- `cast(data, params, permitted, opts \\ [])` takes external data. It filters keys and casts types.
- `change/2` and `put_change/3` take internal data. They do not cast.
- List the permitted fields literally. Never build that list from user input.

```elixir
def registration_changeset(user, attrs) do
  user
  |> cast(attrs, [:email, :password, :status])
  |> validate_required([:email, :password])
  |> validate_format(:email, ~r/@/)
  |> validate_length(:password, min: 12)
  |> validate_number(:age, greater_than_or_equal_to: 18)
  |> validate_inclusion(:status, [:active, :pending])
  |> validate_change(:slug, fn :slug, s ->
    if s =~ ~r/^[a-z0-9-]+$/, do: [], else: [slug: "invalid"]
  end)
  |> unique_constraint(:email)
end
```

- `validate_change/3` returns a keyword list of errors, or `[]` when valid.
- Use `apply_action(changeset, :insert)` to validate without touching the database.

### cast_assoc vs put_assoc vs cast_embed

- `cast_assoc(changeset, name, opts)` takes external params for children. Ecto matches existing rows and computes inserts, updates, and deletes.
- `put_assoc(changeset, name, value, opts)` takes structs or changesets you already hold. It needs the association preloaded, except on a newly built parent.
- `cast_embed(changeset, name, opts)` does the same as `cast_assoc` for `embeds_one` / `embeds_many`.
- Pass `with: &Mod.fun/2` to pick the child changeset.

```elixir
|> cast_assoc(:addresses, with: &Address.changeset/2)  # GOOD: form params
|> put_assoc(:tags, tags)                              # GOOD: loaded structs
|> put_assoc(:tags, params["tags"])                    # BAD: raw params
```

### Constraints

- A validation alone is a race condition. Two processes can both pass the check and both insert. The docs state it: "there is always a chance two tags with the same name would be validated and inserted simultaneously, passing the validation and leading to duplicated entries."
- A constraint call runs no query. It converts the database error into a changeset error at insert or update time.
- Every `unique_constraint/3`, `foreign_key_constraint/3`, and `check_constraint/3` MUST have a matching database constraint in a migration. Without it the call never fires and the operation raises.

```elixir
create unique_index(:users, [:email])   # migration
|> unique_constraint(:email)            # changeset
```

- Pass `name:` when the index name is not the default `table_field_index`.
- `foreign_key_constraint(:org_id)` needs `references(:orgs)` in the migration.
- `unsafe_validate_unique(changeset, fields, repo, opts)` gives an early friendly error. It is unsafe alone. Always keep `unique_constraint` after it.

## Queries

- Write query functions that take a queryable and return a queryable. They compose.

```elixir
def published(q), do: from p in q, where: not is_nil(p.published_at)
def by_org(q, org_id), do: from p in q, where: p.org_id == ^org_id
def recent(q, n), do: from p in q, order_by: [desc: p.inserted_at], limit: ^n

Post |> published() |> by_org(org_id) |> recent(10) |> Repo.all()
```

- Use named bindings. Never depend on binding position across modules.

```elixir
def with_comments(q), do: from p in q, join: c in assoc(p, :comments), as: :comment
def commented_after(q, d), do: from [comment: c] in q, where: c.inserted_at > ^d
```

- Select only the fields you need. A bare query loads every column.

```elixir
from p in Post, select: %{id: p.id, title: p.title}
from p in Post, select: map(p, [:id, :title])   # or struct(p, [:id, :title])
```

- Use `Repo.exists?(query)` instead of `Repo.aggregate(query, :count) > 0`.
- Use `Ecto.Query.exclude(query, :order_by)` to strip a clause before reuse.
- Use `subquery/1` in `from`, `join`, `where ... in`, and `select`.
- Build runtime conditions with `dynamic/2`, then pin them: `where(Post, ^dynamic([p], p.archived == false))`.

### N+1

```elixir
# BAD: one query per post
Enum.map(Repo.all(Post), &Repo.all(from c in Comment, where: c.post_id == ^&1.id))

# GOOD: two queries, run in parallel outside a transaction
Repo.all(from p in Post, preload: [:comments])

# GOOD: one query, when the child needs filtering or ordering
Repo.all(
  from p in Post,
    join: c in assoc(p, :comments), as: :comment,
    where: c.published_at > p.updated_at,
    preload: [comments: c]
)
```

- Prefer plain `preload`. Separate queries parallelize and do not duplicate parent rows.
- Use `join` plus `preload: [assoc: binding]` only when the child must be filtered, ordered, or limited in the same query.
- Use `Repo.preload/2` on structs you already loaded.

## Dynamic query safety

- Never build SQL by string concatenation. Use the query DSL.
- Pin every runtime value with `^`. Ecto sends it as a bound parameter.

```elixir
Repo.query!("SELECT * FROM users WHERE email = '#{email}'")   # BAD
from u in User, where: fragment("email = '#{email}'")         # BAD
from u in User, where: u.email == ^email                      # GOOD
from u in User, where: fragment("lower(?) = lower(?)", u.email, ^email)  # GOOD
```

- `fragment/1` is safe only through `?` placeholders bound to pinned values. Keep the SQL text a literal.
- `unsafe_fragment/1` injects text with no escaping. The docs say uncontrolled input "should never be used" with it.
- Never pass a user value as a column name, table name, or sort direction. Map it to an allowlist first.

```elixir
dir = if params["dir"] == "asc", do: :asc, else: :desc
from p in Post, order_by: [{^dir, :inserted_at}]
```

## Transactions

- Use `Ecto.Multi` for more than one write. Never nest `Repo.transaction` calls.
- Ecto 3.14 marks `Repo.transaction/2` as deprecated in favour of `Repo.transact/2`. Both take the same arguments. Use `transact/2` on Ecto 3.14+. Use `transaction/2` on older versions. Check `mix.exs`.

```elixir
# BAD: nested transactions
Repo.transaction(fn -> Repo.transaction(fn -> Repo.insert(profile_cs) end) end)

# GOOD
Ecto.Multi.new()
|> Ecto.Multi.insert(:user, user_changeset)
|> Ecto.Multi.insert(:profile, fn %{user: user} ->
  Profile.changeset(%Profile{}, %{user_id: user.id})
end)
|> Ecto.Multi.run(:notify, fn _repo, %{user: user} -> Notifier.send(user) end)
|> Repo.transact()
```

- Name each step after its operation. A name is any unique term. Use `{:account, id}` inside a reduce.
- Success returns `{:ok, %{user: user, profile: profile, notify: result}}`.
- Failure returns `{:error, failed_name, failed_value, changes_so_far}`. Match on the failed name.

```elixir
case Repo.transact(multi) do
  {:ok, %{user: user}} -> {:ok, user}
  {:error, :user, changeset, _changes} -> {:error, changeset}
  {:error, :profile, changeset, _changes} -> {:error, changeset}
end
```

- A `Multi.run/3` function must return `{:ok, value}` or `{:error, value}`. An `{:error, _}` rolls back.
- A plain `Repo.transact/2` function that returns `{:error, reason}` rolls back and returns `{:error, reason}`.
- Prefer `Multi.insert_all/5`, `Multi.update_all/5`, `Multi.delete_all/4`, `Multi.all/4`, `Multi.one/4`, `Multi.put/3`, `Multi.error/3` over raw calls inside `run`.
- Compose multis from different contexts with `Multi.append/2` and `Multi.prepend/2`.

## Repo API

- `Repo.get/3` and `Repo.get_by/3` return `nil` for no row. Use them when absence is normal.
- `Repo.get!/3` and `Repo.get_by!/3` raise `Ecto.NoResultsError`. Use them when absence is a bug.
- `Repo.one/2` returns `nil` for no row and raises when more than one row matches. `Repo.all/2` returns a list.
- `Repo.insert/2` returns `{:ok, struct}` or `{:error, changeset}`. `Repo.insert!/2` raises. Use the bang form in seeds, tests, and Multi steps only.
- `Repo.insert_all/3` returns `{count, nil | rows}`. It skips changesets, so it runs no validations and sets no timestamps.

```elixir
now = DateTime.utc_now()
rows = Enum.map(names, &%{name: &1, inserted_at: now, updated_at: now})
Repo.insert_all(Tag, rows, on_conflict: :nothing, conflict_target: :name)
```

- `Repo.update_all/3` does not touch `updated_at`. Set it in the `set:` list.
- Use `on_conflict:` with `conflict_target:` for upserts. `:nothing` ignores the conflict. `[set: [...]]` updates the row and needs a target.
- `Repo.stream/2` needs a transaction on SQL adapters.

```elixir
Repo.transact(fn ->
  Post |> Repo.stream() |> Stream.each(&archive/1) |> Stream.run()
end)
```

## Migrations

- Write `change/0` and let Ecto derive the rollback. Write `up/0` and `down/0` only when `change/0` cannot reverse.
- Reversible: `create`, `drop`, `add`, `modify`, `alter`, `rename`. Not reversible: `execute/1`, `remove/1`, `add_if_not_exists/3`.
- Use `execute/2` to give raw SQL an explicit rollback: `execute "CREATE EXTENSION citext", "DROP EXTENSION citext"`.
- Give `modify` a `:from` so it can reverse: `modify :title, :text, from: :string`.

- Never edit a migration that shipped. It already ran elsewhere. Add a new migration.
- A concurrent index needs `@disable_ddl_transaction true`. Postgres refuses `CREATE INDEX CONCURRENTLY` inside a transaction.

```elixir
defmodule MyApp.Repo.Migrations.AddPostsSlugIndex do
  use Ecto.Migration
  @disable_ddl_transaction true
  @disable_migration_lock true

  def change, do: create index("posts", [:slug], concurrently: true)
end
```

- Add a `NOT NULL` column on a large table in three steps. Migration one adds the nullable column. A backfill runs outside the schema migration. Migration two adds `null: false` with `modify ..., from:`.
- Keep data migrations out of schema migrations. Schema migrations must stay fast and must not depend on schema modules, which change later.
- Write backfills as a `mix` task or a separate migration directory. Use `Repo.stream` and batches.
- Add here every index and `references(...)` that a changeset constraint depends on.

## Prefixes and multi-tenancy

- Every Repo operation takes `:prefix`, for example `Repo.all(Post, prefix: "tenant_42")`.
- Set a fixed prefix per schema with `@schema_prefix "main"`, or per query with `from p in Post, prefix: "foo"`.
- Query precedence: from/join prefix, then schema prefix, then the `:prefix` option, then the connection prefix.
- Use `Ecto.put_meta(struct, prefix: "public")` to move a loaded struct before writing it.
- For a tenant foreign key column, scope every query in the Repo.

```elixir
defmodule MyApp.Repo do
  use Ecto.Repo, otp_app: :my_app
  require Ecto.Query

  @impl true
  def prepare_query(_operation, query, opts) do
    cond do
      opts[:skip_org_id] || opts[:ecto_query] in [:schema_migration, :preload] ->
        {query, opts}

      org_id = opts[:org_id] ->
        {Ecto.Query.where(query, org_id: ^org_id), opts}

      true ->
        raise "expected org_id or skip_org_id to be set"
    end
  end

  @impl true
  def default_options(_operation), do: [org_id: Process.get({__MODULE__, :org_id})]
end
```

- Raise when the tenant is missing. Never fall back to an unscoped query.

## Testing

- Set `config :my_app, MyApp.Repo, pool: Ecto.Adapters.SQL.Sandbox` in the test config.
- Put `Ecto.Adapters.SQL.Sandbox.mode(MyApp.Repo, :manual)` in `test_helper.exs`.
- Check out one owner per test. Each test runs in a transaction that rolls back.

```elixir
defmodule PostTest do
  use ExUnit.Case, async: true

  setup do
    pid = Ecto.Adapters.SQL.Sandbox.start_owner!(MyApp.Repo)
    on_exit(fn -> Ecto.Adapters.SQL.Sandbox.stop_owner(pid) end)
    :ok
  end
end
```

- Use `Ecto.Adapters.SQL.Sandbox.allow(Repo, self(), pid)` to share the test connection with another process. Allowances keep `async: true`.
- `mode(Repo, {:shared, self()})` forces `async: false`. Use it only when you cannot list the collaborating processes.
- Write factories as plain functions in `test/support`. Return attribute maps or inserted structs. Make unique values with `System.unique_integer([:positive])`.

- Test changeset rules with `apply_action(changeset, :insert)` and no database.
- Test a constraint with a real insert. The error only appears after the database rejects the row.
