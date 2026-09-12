# Phoenix reference

Targets Phoenix 1.8.12, Phoenix LiveView 1.2.10, phoenix_html 4.3.0 (latest on hex.pm, 2026-08-23).

## Project layout

- Put business logic in `lib/my_app`. Put web code in `lib/my_app_web`.
- Put Ecto schemas in `lib/my_app/<context>/<schema>.ex`. Example: `lib/my_app/blog/post.ex`.
- Put the context module in `lib/my_app/<context>.ex`. Example: `lib/my_app/blog.ex`.
- Put controllers, HTML modules, and `.heex` files in `lib/my_app_web/controllers`.
- Put LiveViews in `lib/my_app_web/live`. Put shared components in `lib/my_app_web/components`.
- `components/core_components.ex` holds `<.input>`, `<.icon>`, `<.button>`, `<.header>`, `<.table>`.
- Product pages use Inertia + React. `components/layouts/root.html.heex` is the only wired layout.
- Run `mix precommit` when you finish a change. Fix every warning it reports.
- Use `Req` for HTTP requests. Do not add `:httpoison`, `:tesla`, or `:httpc`.

## Contexts

- Treat the context module as the public API. Treat every other module in the context as private.
- Never call `Repo` from the web layer. Controllers, LiveViews, and templates call context functions only.
- Return `{:ok, struct}` or `{:error, %Ecto.Changeset{}}` from write functions.
- Return the struct or raise from `get_x!/2`. Return a list from `list_x/1`.
- Return `%Ecto.Changeset{}` from `change_x/2`. The changeset is the contract with forms.
- Name a context after a business domain, not after a table. Example: `Accounts`, `Blog`, `ShoppingCart`.
- Use the plural of the resource when no better name exists. Example: `Posts`.
- Split a context when two groups of functions do not share rules. A catalog does not know cart rules.
- Reference another context by `belongs_to` on the schema. Keep the dependency to the foreign key only.
- Do not create `ProductQueries` or `ProductChangesets` modules by default. Internal layout is free.

```elixir
# GOOD - context owns Repo, returns tagged tuples
def create_post(%Scope{} = scope, attrs) do
  with {:ok, post = %Post{}} <- %Post{} |> Post.changeset(attrs, scope) |> Repo.insert() do
    broadcast_post(scope, {:created, post})
    {:ok, post}
  end
end

# BAD - web layer touches Repo
def index(conn, _params), do: render(conn, :index, posts: Repo.all(Post))
```

## Scopes (Phoenix 1.8)

- `mix phx.gen.auth` creates `MyApp.Accounts.Scope`. It is a struct with a `user` field.
- The auth system assigns `@current_scope`. It does not assign `@current_user`.
- Read the user as `@current_scope.user` in templates. Never use `@current_user`.
- Pass the scope as the first argument to every context function.
- Filter every query by the scope key inside the context.
- Assert ownership before an update or a delete.
- Declare scopes in `config/config.exs` under `:scopes`. Generators read that config.

```elixir
config :my_app, :scopes,
  user: [
    default: true, module: MyApp.Accounts.Scope, assign_key: :current_scope,
    access_path: [:user, :id], schema_key: :user_id, schema_type: :id, schema_table: :users
  ]
```

```elixir
def list_posts(%Scope{} = scope), do: Repo.all_by(Post, user_id: scope.user.id)

def get_post!(%Scope{} = scope, id), do: Repo.get_by!(Post, id: id, user_id: scope.user.id)

def delete_post(%Scope{} = scope, %Post{} = post) do
  true = post.user_id == scope.user.id
  Repo.delete(post)
end
```

## Router

- `mix phx.gen.auth` creates the plugs `:fetch_current_scope_for_user`, `:require_authenticated_user`, and `:redirect_if_user_is_authenticated`.
- Put authenticated LiveViews in the existing `live_session :require_authenticated_user`.
- Put optional-auth LiveViews in the existing `live_session :current_user`.
- Never define a `live_session` name twice. Group all routes of one name in one block.
- Tell the user which pipeline and `live_session` you chose, and say why.

```elixir
scope "/", MyAppWeb do
  pipe_through [:browser, :require_authenticated_user]

  live_session :require_authenticated_user,
    on_mount: [{MyAppWeb.UserAuth, :ensure_authenticated}] do
    live "/posts", PostLive.Index, :index
  end
end
```

## Verified routes

- Build every path with the `~p` sigil. The compiler verifies it against the router.
- Never build a path by string interpolation or by concatenation.
- Interpolate structs and ids inside `~p`. `Phoenix.Param` derives the segment.
- Pass query strings as a keyword list or a map inside `~p`.
- Wrap `~p` in `url/1` when you need a full URL, for example in an email.

```elixir
# GOOD
~p"/posts/#{post}"
~p"/users/17?#{[admin: true]}"
url(~p"/posts")

# BAD
"/posts/" <> to_string(post.id)
Routes.post_path(conn, :show, post)
```

## Controllers

- Keep actions thin. Put business logic in the context.
- Use `with` for the happy path. Let `action_fallback` handle every other result.
- Read the scope from `conn.assigns.current_scope`.
- Redirect with `~p`. Never redirect to a user-supplied string.
- `mix phx.gen.json` generates `FallbackController` and `ChangesetJSON`. Reuse them.

```elixir
defmodule MyAppWeb.PostController do
  use MyAppWeb, :controller
  action_fallback MyAppWeb.FallbackController

  def show(conn, %{"id" => id}) do
    with {:ok, post} <- Blog.fetch_post(conn.assigns.current_scope, id) do
      render(conn, :show, post: post)
    end
  end
end
```

## HEEx

- Write markup in the `~H` sigil or in a `.heex` file. Never build HTML by string concatenation.
- Product pages are Inertia components; do not wrap them in a Phoenix component layout.
- No flash group component is wired in this application; do not call one.
- Use `{...}` for interpolation in a body and in an attribute.
- Use `<%= ... %>` only for block constructs and inside `<script>` or `<style>`. Never in an attribute.
- Use `:if` and `:for` instead of block `if` and `for`.
- Add `:key` to a `:for` tag when the list can change order. It improves change tracking.
- HEEx escapes interpolated values. `raw/1` disables escaping. Call `raw/1` only on trusted markup.
- Give `class` a list. HEEx drops `nil` and `false` entries. Spread attributes with `{@attrs}`.

```heex
<div class={["card", @active && "card-active"]} title={@title}>
  <p :if={@posts == []}>No posts yet.</p>
  <li :for={post <- @posts} :key={post.id}>{post.title}</li>
</div>
```

```heex
<!-- BAD - EEx tag inside an attribute -->
<div class="<%= @class %>">...</div>
<!-- BAD - unescaped user data -->
{raw(@comment_body)}
```

## Function components

- Declare every attribute with `attr/3`. Declare every block with `slot/1` or `slot/3`.
- Mark an attribute `required: true` or give it a `:default`. The compiler then checks callers.
- Declare `attr :rest, :global` to accept HTML and `phx-` attributes.
- Call a component in the same module as `<.name />`. Call one elsewhere as `<Mod.name />`.
- Compute values with `assign/2` on `assigns`. Never use `Map.put/3` on `assigns`.
- Do not define variables in a template. Do not pass `{assigns}` to a child. Change tracking stops working.

```elixir
attr :title, :string, required: true
attr :rest, :global
slot :inner_block, required: true
slot :actions

def panel(assigns) do
  ~H"""
  <section {@rest}>
    <h2>{@title}</h2>
    {render_slot(@inner_block)}
    <div :for={action <- @actions}>{render_slot(action)}</div>
  </section>
  """
end
```

## LiveView lifecycle

- `mount/3` runs twice. First on the HTTP request. Second on the WebSocket connection.
- Guard expensive work with `connected?/1`. The disconnected render must stay cheap.
- Use `render_with/2` to show a placeholder on the disconnected render of a heavy page.
- `handle_params/3` runs after `mount/3` and after every live patch. It reads `params` and the URI.
- `handle_event/3` handles client events. `handle_info/2` handles process messages.
- `render/1` must be a pure function of assigns. Never load data in `render/1` or in a template.
- Return `{:ok, socket, temporary_assigns: [messages: []]}` to drop large assigns after each render.

```elixir
def mount(_params, _session, socket) do
  scope = socket.assigns.current_scope
  if connected?(socket), do: Blog.subscribe_posts(scope)
  {:ok, stream(socket, :posts, Blog.list_posts(scope))}
end
```

## Assigns and streams

- Use assigns for scalar state and small maps.
- Use `stream/4` for collections. A stream keeps no list in server memory.
- Give the container `phx-update="stream"` and an `id`. Give each child the stream id.
- Insert with `stream_insert/4`. Remove with `stream_delete/3`. Replace all with `reset: true`.
- Pass `limit:` to cap the DOM. A negative limit keeps the last N items. A positive limit keeps the first N.
- You cannot read a stream back on the server. Keep any value you need in a separate assign.

```elixir
{:noreply, stream_insert(socket, :posts, post, at: 0)}
{:noreply, stream(socket, :posts, Blog.list_posts(scope), reset: true)}
```

```heex
<ul id="posts" phx-update="stream">
  <li :for={{dom_id, post} <- @streams.posts} id={dom_id}>{post.title}</li>
</ul>
```

## Async work

- Use `assign_async/3` to load data without blocking `mount/3`.
- The function must return `{:ok, %{key => value}}` or `{:error, reason}`.
- Render the states with `<.async_result>` and its `:loading` and `:failed` slots.
- Use `start_async/3` plus `handle_async/3` when the result is not an assign.
- A second `start_async/3` with the same key discards the earlier result.

```elixir
{:ok, assign_async(socket, :stats, fn -> {:ok, %{stats: Blog.expensive_stats()}} end)}
```

```heex
<.async_result :let={stats} assign={@stats}>
  <:loading>Loading...</:loading>
  <:failed :let={_reason}>Could not load stats.</:failed>
  {stats.count}
</.async_result>
```

## Forms

- Build the form assign with `to_form/2`. Never pass a raw changeset to `<.form for={...}>`.
- Give every form an `id`. LiveView needs it to recover the form after a disconnect.
- Handle `phx-change` for validation. Pass `action: :validate` so errors show.
- Handle `phx-submit` for the write. Navigate on success. Re-assign the form on failure.
- Use the imported `<.input field={@form[:name]} />` component from `core_components.ex`.

```elixir
def handle_event("validate", %{"post" => params}, socket) do
  changeset = Blog.change_post(socket.assigns.current_scope, socket.assigns.post, params)
  {:noreply, assign(socket, form: to_form(changeset, action: :validate))}
end

def handle_event("save", %{"post" => params}, socket) do
  case Blog.create_post(socket.assigns.current_scope, params) do
    {:ok, post} -> {:noreply, push_navigate(socket, to: ~p"/posts/#{post}")}
    {:error, changeset} -> {:noreply, assign(socket, form: to_form(changeset))}
  end
end
```

```heex
<.form id="post-form" for={@form} phx-change="validate" phx-submit="save">
  <.input field={@form[:title]} label="Title" />
  <.button>Save</.button>
</.form>
```

## Bindings

- `phx-click`, `phx-submit`, `phx-change`, `phx-blur`, `phx-focus`, `phx-keydown`, `phx-keyup` send events.
- `phx-value-*` attaches data to the payload. `phx-target={@myself}` routes to a LiveComponent.
- `phx-update` accepts `replace` (default), `stream`, and `ignore`. Use `ignore` for JS-owned DOM.
- `phx-debounce` and `phx-throttle` limit event rate. `phx-viewport-top` and `phx-viewport-bottom` drive infinite scroll.

## Navigation

- `push_patch/2` stays in the same LiveView. It calls `handle_params/3`. State survives.
- `push_navigate/2` mounts another LiveView over the same socket. The current process stops.
- `redirect/2` forces a full page load. All LiveView state is lost.
- In templates use `<.link patch={~p"/..."}>`, `<.link navigate={~p"/..."}>`, and `<.link href={...}>`.
- Never pass an unvalidated user value to `redirect(external: ...)`.

## PubSub

- Broadcast from the context, not from the LiveView.
- Scope the topic by the scope key. Do not use one global topic.
- Subscribe in `mount/3`. Handle the message in `handle_info/2`.

```elixir
def subscribe_posts(%Scope{} = scope) do
  Phoenix.PubSub.subscribe(MyApp.PubSub, "user:#{scope.user.id}:posts")
end

defp broadcast_post(%Scope{} = scope, message) do
  Phoenix.PubSub.broadcast(MyApp.PubSub, "user:#{scope.user.id}:posts", message)
end
```

```elixir
def handle_info({type, %Post{}}, socket) when type in [:created, :updated, :deleted] do
  {:noreply, stream(socket, :posts, Blog.list_posts(socket.assigns.current_scope), reset: true)}
end
```

## Security

- Treat `params`, `handle_params/3` params, and event payloads as attacker-controlled.
- Re-authorize inside every `handle_event/3`. A hidden button is not a permission check.
- Pass the scope to the context and let the context enforce the rule. Never trust an id from the client.
- Cast with a changeset. Never pass raw params to `Repo`.
- The `:browser` pipeline runs `:protect_from_forgery` and `:put_secure_browser_headers`. Keep them.
- Never change state through a GET request. CSRF tokens do not protect GET.
- Group LiveViews by authentication flow with `live_session`, not by fine-grained permission.
- Use `on_mount` hooks for shared auth. Use `assign_new/3` inside them to reuse the HTTP-mount value.
- Set `live_socket_id` in the session so logout can disconnect open sockets.

```elixir
def on_mount(:ensure_authenticated, _params, session, socket) do
  socket =
    assign_new(socket, :current_scope, fn ->
      Scope.for_user(Accounts.get_user_by_session_token(session["user_token"]))
    end)

  if socket.assigns.current_scope do
    {:cont, socket}
  else
    {:halt, redirect(socket, to: ~p"/users/log-in")}
  end
end
```

```elixir
# GOOD - the context re-checks ownership
def handle_event("delete", %{"id" => id}, socket) do
  scope = socket.assigns.current_scope
  post = Blog.get_post!(scope, id)
  {:ok, _} = Blog.delete_post(scope, post)
  {:noreply, stream_delete(socket, :posts, post)}
end
```

## Error handling

- Write assertive code. Match on `true = ...` or call a bang function for cases that must not happen.
- An exception in the HTTP mount renders the Phoenix error page.
- An exception in the connected mount crashes the process. The client reloads the page.
- An exception after mount crashes the process. The client remounts over the socket.
- A crash loses all socket state. Keep recoverable state in the URL or in the database.
- `Ecto.NoResultsError` from a scoped `Repo.get!` becomes a 404. Prefer it over a manual check.

## Telemetry

- `MyAppWeb.Telemetry` is a supervisor. It defines `metrics/0`, starts `:telemetry_poller`, and holds reporters.
- Define metrics with `Telemetry.Metrics` functions such as `summary/2` and `counter/2`.
- Phoenix emits `phoenix.endpoint.stop.duration` and `phoenix.router_dispatch.stop.duration`.
- Emit your own events with `:telemetry.execute/3` from the context, not from the web layer.

## Assets

- Tailwind v4 is the default. There is no `tailwind.config.js`.
- Keep the generated `@import "tailwindcss" source(none);` line and the `@source` lines in `app.css`.
- The generator installs the daisyUI plugin with two themes. Write your own Tailwind components anyway.
- Never use `@apply` in raw CSS.
- Only `app.js` and `app.css` are bundled. Import vendor code into them. Never write an inline `<script>` block.
- Use `<.icon name="hero-x-mark" class="w-5 h-5" />` for icons. Do not call `Heroicons` modules.

## Deprecated patterns

- Do not create view modules with `render/2` clauses. Use function components and `embed_templates`.
- Do not use `Routes.*_path/*` helpers. `phx.new` no longer generates them. Use `~p`.
- Do not use `live_redirect`, `live_patch`, or `push_redirect/2`. Use `<.link>`, `push_patch/2`, and `push_navigate/2`.
- Do not reference `@current_user` in a 1.8 app generated with scopes. Use `@current_scope.user`.
