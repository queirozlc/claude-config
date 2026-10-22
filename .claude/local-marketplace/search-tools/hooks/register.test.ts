import { grepArgs, globArgs, cap, render } from './register'

const eq = (a: unknown, b: unknown, msg: string) => {
  if (JSON.stringify(a) !== JSON.stringify(b)) throw new Error(`${msg}: ${JSON.stringify(a)} != ${JSON.stringify(b)}`)
}

// The pattern is one argv element: no shell parsing, quotes and $ survive.
eq(
  grepArgs({ pattern: 'it("a $b")', path: 'src', glob: '*.ts' }).slice(-5),
  ['-g', '*.ts', '-e', 'it("a $b")', '--', 'src'].slice(-5),
  'grep pattern is passed verbatim',
)
eq(grepArgs({ pattern: 'x' }).slice(-3), ['-e', 'x', '--', '.'].slice(-3), 'grep defaults to project root')
eq(grepArgs({ pattern: 'x', files_only: true, case_insensitive: true }).includes('-l'), true, 'files_only adds -l')
eq(globArgs({ pattern: '**/*.tsx' }).slice(-2), ['**/*.tsx', '.'], 'glob keeps a ** pattern')
eq(globArgs({ pattern: 'src/*.ts', path: 'app' }).slice(-2), ['**/src/*.ts', 'app'], 'glob prefixes a relative pattern')

const many = Array.from({ length: 300 }, (_, i) => `f:${i}:x`).join('\n')
eq(cap(many).endsWith('50 more lines. Narrow with path or glob.'), true, 'cap truncates at 250')
eq(cap('a\nb\n'), 'a\nb', 'cap keeps short output')

eq(render({ exitCode: 1, stdout: '', stderr: '' }, 'No matches.'), 'No matches.', 'exit 1 is no match')
eq(render({ exitCode: 2, stdout: '', stderr: 'bad regex' }, ''), 'search failed (2): bad regex', 'exit 2 is an error')

console.log('ok')
