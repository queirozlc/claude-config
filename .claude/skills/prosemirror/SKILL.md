---
name: prosemirror
disable-model-invocation: true
description: Build and debug rich text editors with ProseMirror, the headless toolkit underpinning Tiptap, Remirror, and Atlassian/Notion-style editors. Use for schema design (nodes/marks, content expressions, toDOM/parseDOM), document model & positions, transactions/transforms, plugins, decorations, NodeViews, commands, keymaps, input rules, history, and collaborative editing. Triggers on ProseMirror APIs, "prosemirror-state/view/model/transform", position mapping bugs, schema/content errors, custom node rendering, or low-level work under Tiptap/Remirror.
---

# ProseMirror

Headless rich-text toolkit. State is immutable; you describe changes as transactions, view renders them. Modular packages — install only what you use.

## Packages

| Package | Purpose |
|---|---|
| `prosemirror-model` | Document, Node, Fragment, Slice, Mark, Schema |
| `prosemirror-state` | EditorState, Transaction, Selection, Plugin |
| `prosemirror-view` | EditorView (renders to DOM, handles events) |
| `prosemirror-transform` | Steps, mapping (position remapping) |
| `prosemirror-commands` | baseKeymap, toggleMark, setBlockType, etc. |
| `prosemirror-keymap` | bind keys → commands |
| `prosemirror-history` | undo/redo |
| `prosemirror-inputrules` | text-trigger transforms (e.g. `## ` → heading) |
| `prosemirror-schema-basic`, `-list` | ready-made schemas/commands |
| `prosemirror-example-setup` | bundles plugins for quick start (dev only) |
| `prosemirror-collab` | collaborative editing primitives |

## Core data flow

```
EditorView ──user event──▶ Transaction ──dispatchTransaction──▶ state.apply(tr) ──▶ new EditorState ──updateState──▶ rerender
```

```js
import {EditorState} from "prosemirror-state"
import {EditorView} from "prosemirror-view"

const state = EditorState.create({schema, plugins})
const view = new EditorView(mount, {
  state,
  dispatchTransaction(tr) {            // intercept ALL changes here
    const next = view.state.apply(tr)  // pure: old state + tr → new state
    view.updateState(next)             // every update MUST go through this
  }
})
```
`EditorState.create({schema, doc?, selection?, plugins?})`. `view.dispatch(tr)` is shorthand. Read current state via `view.state`; destroy with `view.destroy()`.

## Document model

Tree of immutable `Node`s. A node has `type`, `attrs`, `content` (Fragment), and inline nodes carry `marks`. **Never mutate** — breaks structural sharing, history, collab. Build new docs via transforms.

**Positions are token offsets, not char indices:**
- pos 0 = very start of doc
- entering OR leaving a non-leaf node = 1 token each (a `<p>` start boundary is 1)
- each text char = 1 token; each leaf node (image, hr) = 1 token
- `<p>hi</p>` → 0 before p, 1 inside-start, 2,3 across "hi", 4 inside-end (5 = after p)

`doc.content.size` = end position (use this, NOT `doc.nodeSize` which adds outer tokens).

`$pos = doc.resolve(pos)` → `ResolvedPos`: `.depth`, `.parent`, `.parentOffset`, `.pos`, `.nodeBefore`, `.nodeAfter`, `.before(d)`, `.after(d)`, `.start(d)`, `.end(d)`, `.node(d)`. Use it instead of counting tokens by hand.

`Slice` = a piece of doc that may be "open" at edges: `.openStart`, `.openEnd`. Pasting/replacing uses slices. `Slice.empty` deletes.

## Schema

Declares allowed nodes/marks + DOM mapping. `0` in `toDOM` = the "content hole".

```js
import {Schema} from "prosemirror-model"
const schema = new Schema({
  nodes: {
    doc: {content: "block+"},
    paragraph: {group: "block", content: "inline*",
      toDOM: () => ["p", 0], parseDOM: [{tag: "p"}]},
    heading: {group: "block", content: "inline*", attrs: {level: {default: 1}},
      defining: true,
      toDOM: n => ["h" + n.attrs.level, 0],
      parseDOM: [1,2,3].map(l => ({tag: "h"+l, attrs: {level: l}}))},
    text: {group: "inline"},
    image: {group: "inline", inline: true, draggable: true,
      attrs: {src: {}, alt: {default: null}},
      toDOM: n => ["img", n.attrs], parseDOM: [{tag: "img[src]", getAttrs: d => ({src: d.src, alt: d.alt})}]},
    hard_break: {group: "inline", inline: true, selectable: false,
      toDOM: () => ["br"], parseDOM: [{tag: "br"}]}
  },
  marks: {
    strong: {toDOM: () => ["strong", 0],
      parseDOM: [{tag: "strong"}, {tag: "b"}, {style: "font-weight", getAttrs: v => /^(bold|[5-9]\d\d)/.test(v) && null}]},
    link: {attrs: {href: {}}, inclusive: false,
      toDOM: n => ["a", n.attrs, 0], parseDOM: [{tag: "a[href]", getAttrs: d => ({href: d.href})}]}
  }
})
```

**Content expressions** (regex-like over node names/groups): `"paragraph+"` 1+, `"block*"` 0+, `"heading paragraph"` sequence, `"(text | image)*"` alt, `"list_item{2,}"` ranges. First valid type in an expression is the default fill — bad ordering causes infinite recursion when auto-filling.

Key NodeSpec fields: `content`, `group`, `inline`, `atom` (treat as opaque leaf), `marks` (allowed marks, `""`=none), `defining`, `isolating`, `draggable`, `selectable`, `attrs`, `parseDOM`, `toDOM`. MarkSpec: `inclusive` (typing at boundary extends mark), `excludes`, `spanning`, `attrs`, `parseDOM`, `toDOM`.

`getAttrs` returning `false` rejects the rule; returning `null`/object accepts. Create nodes: `schema.node(type, attrs, content, marks)`, `schema.text(str, marks)`, `schema.mark(type, attrs)`. Serialize: `node.toJSON()` / `Node.fromJSON(schema, json)` (or `schema.nodeFromJSON`).

## Transactions & transforms

`Transaction extends Transform`. Get one via `state.tr`, mutate by chaining, then dispatch. Each method adds Steps and returns the tr (chainable).

```js
let tr = state.tr
  .insertText("hi", from)
  .delete(from, to)
  .replaceWith(from, to, node)
  .addMark(from, to, schema.marks.strong.create())
  .removeMark(from, to, schema.marks.strong)
  .setNodeMarkup(pos, type, attrs)
  .setBlockType(from, to, type, attrs)
  .wrap(range, [{type}])           // range = $from.blockRange($to)
  .setSelection(sel)
  .scrollIntoView()
dispatch(tr)
```
Selection-aware helpers: `replaceSelectionWith(node)`, `deleteSelection()`, `replaceSelection(slice)`. Metadata: `tr.setMeta(key, val)` / `tr.getMeta(key)` (key = string or PluginKey) to tag transactions for plugins. `tr.docChanged` true if any steps. Block undo: `tr.setMeta("addToHistory", false)`.

**Position mapping** — when the doc changes, old positions move. Map them through:
```js
let mapped = tr.mapping.map(oldPos)        // whole transaction
// single step: step.getMap().map(pos)
// bias: map(pos, -1) keeps pos before inserted content (default +1 = after)
```
Always re-map a stored position after dispatching changes, else it points to the wrong place.

`replace` (precise) vs `replaceRange`/`replaceRangeWith` (WYSIWYG-friendly, used for paste — may grow/shrink to fit). `maybeStep(step)` applies if valid else no-op.

## Plugins

```js
import {Plugin, PluginKey} from "prosemirror-state"
const key = new PluginKey("myPlugin")
const plugin = new Plugin({
  key,
  state: {                                   // optional per-plugin state field (immutable!)
    init(config, state) { return initial },
    apply(tr, value, oldState, newState) { return next }  // pure
  },
  props: {                                   // EditorView props
    handleKeyDown(view, event) { return false },  // true = handled, stop
    handleDOMEvents: {...}, handleClick, handlePaste, handleDrop,
    decorations(state) { return DecorationSet },
    nodeViews: {...}, attributes, transformPasted
  },
  view(editorView) { return {update(v, prev){}, destroy(){}} },  // imperative side effects
  filterTransaction(tr, state) { return true },   // false cancels tr
  appendTransaction(trs, oldState, newState) { return tr | null } // react to changes
})
```
Read plugin state anywhere: `key.getState(editorState)`. Order matters — earlier plugins' props/keymaps win.

## Decorations

Visual layer, no doc change. Build a `DecorationSet` in the `decorations` prop. Three kinds:
```js
import {Decoration, DecorationSet} from "prosemirror-view"
Decoration.inline(from, to, {class: "hl", style: "color:purple"})  // style/class a range
Decoration.node(from, to, {class: "selected"})                     // attrs on a single node
Decoration.widget(pos, domOrFn, {side: -1, key})                   // insert DOM, not in doc
DecorationSet.create(doc, [decos])
```
For perf with large docs, store the set in plugin `state` and `decoSet.map(tr.mapping, tr.doc)` on each apply instead of rebuilding.

## NodeView

Custom DOM + interaction for one node type. Register via `nodeViews` prop.
```js
nodeViews: {
  image(node, view, getPos) {
    const dom = document.createElement("img")
    dom.src = node.attrs.src
    return {
      dom,
      // contentDOM,                 // where child content renders (omit for leaf/atom)
      update(newNode) { if (newNode.type != node.type) return false
                        node = newNode; dom.src = node.attrs.src; return true },
      selectNode() {}, deselectNode() {}, stopEvent() {}, ignoreMutation() {}, destroy() {}
    }
  }
}
```
`getPos()` returns the node's current position (use to build transactions). Return `false` from `update` to force full re-render.

## Commands

`Command = (state, dispatch?, view?) => boolean`. Without `dispatch`: only test applicability (return true/false) — used to enable/disable toolbar buttons. With `dispatch`: perform and dispatch tr.
```js
import {toggleMark, setBlockType, chainCommands, baseKeymap, joinUp, lift} from "prosemirror-commands"
import {wrapInList} from "prosemirror-schema-list"
toggleMark(schema.marks.strong)            // returns a Command
chainCommands(cmdA, cmdB)                   // run until one returns true

function myCmd(state, dispatch) {
  if (!applies(state)) return false
  if (dispatch) dispatch(state.tr....)
  return true
}
```

## Keymap, input rules, history

```js
import {keymap} from "prosemirror-keymap"
import {undo, redo, history} from "prosemirror-history"
import {inputRules, wrappingInputRule, textblockTypeInputRule} from "prosemirror-inputrules"

plugins: [
  history(),
  keymap({"Mod-z": undo, "Mod-y": redo, "Mod-Shift-z": redo,
          "Mod-b": toggleMark(schema.marks.strong)}),
  keymap(baseKeymap),                       // enter/backspace/etc — add LAST
  inputRules({rules: [
    wrappingInputRule(/^\s*>\s$/, schema.nodes.blockquote),
    textblockTypeInputRule(/^(#{1,6})\s$/, schema.nodes.heading, m => ({level: m[1].length}))
  ]})
]
```
Key syntax: `Mod` = Cmd(mac)/Ctrl, `Shift-`, `Alt-`, `Ctrl-`. `history()` opts: `depth` (default 100), `newGroupDelay` (500ms).

## Collaborative editing

`prosemirror-collab`: central authority orders steps. Each client tracks a version, sends local steps, receives others' steps and rebases.
```js
import {collab, sendableSteps, receiveTransaction, getVersion} from "prosemirror-collab"
plugins: [collab({version})]
// send: const s = sendableSteps(state) → POST {version: s.version, steps, clientID}
// receive: dispatch(receiveTransaction(state, steps, clientIDs))
```
Server must reject steps whose version is stale; client rebases and retries. Yjs (`y-prosemirror`) is the common CRDT alternative — no central server needed.

## Gotchas

- **Immutability**: nodes & plugin state are persistent values. Build new ones; never assign into `.attrs`/`.content`.
- **All updates via `dispatchTransaction`/`updateState`** — direct DOM edits get clobbered on next render.
- **Map stored positions** through `tr.mapping` after every doc change.
- **`doc.content.size`** for the doc end, not `doc.nodeSize`.
- **Schema default-fill recursion**: order content-expression alternatives so the first match is a simple/leaf-reachable type.
- **`baseKeymap` last** so specific keymaps override it.
- **NodeView `contentDOM`**: omit it for leaf/atom nodes; include it (empty, PM-managed) for nodes with editable children.
- **`createChecked`/`node.check()`** validate schema conformance; plain `schema.node` does not fully.
- Use `prosemirror-example-setup` to prototype, but compose plugins yourself in production (it's a demo bundle).

## Fetching exact API

For precise signatures/edge cases, query Context7: `/websites/prosemirror_net` (largest) or per-module `/prosemirror/prosemirror-view`, `-model`. Official reference: prosemirror.net/docs/ref. Guides: prosemirror.net/docs/guide.
