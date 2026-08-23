#!/usr/bin/env node
// Resolve a repo's colour tokens to {name: hex} for measure.py's nearest-token step.
//
// Regex-scanning globals.css finds hsl(var(--x)) in a minority of repos and cannot
// follow theme('colors.darkgray2') at all, so ask Tailwind to resolve its own
// config first and fall back only when that is impossible.
import { readFileSync, existsSync } from 'node:fs'
import { createRequire } from 'node:module'
import { resolve, join } from 'node:path'

const repo = resolve(process.argv[2] ?? '.')
const require = createRequire(join(repo, 'noop.cjs'))
const out = { token_source: null, tokens: {} }

const flatten = (obj, prefix = '') => {
  const acc = {}
  for (const [k, v] of Object.entries(obj ?? {})) {
    const name = prefix ? `${prefix}-${k}` : k
    if (typeof v === 'string') acc[k === 'DEFAULT' ? prefix : name] = v
    else if (v && typeof v === 'object') Object.assign(acc, flatten(v, name))
  }
  return acc
}

const configPath = ['tailwind.config.ts', 'tailwind.config.js', 'tailwind.config.cjs',
                    'tailwind.config.mjs'].map(f => join(repo, f)).find(existsSync)

// A config may be CJS or ESM; require throws on the latter, so try both.
const loadConfig = async () => {
  try {
    return require(configPath)
  } catch (e) {
    if (!/require is not defined|Cannot use import statement|Unexpected token/.test(String(e.message))) throw e
    const m = await import(new URL(`file://${configPath}`))
    return m.default ?? m
  }
}

// 1. Tailwind resolves its own config, including presets and extends.
if (configPath) {
  try {
    const resolveConfig = require('tailwindcss/resolveConfig')
    const cfg = await loadConfig()
    const full = resolveConfig(cfg.default ?? cfg)
    out.tokens = flatten(full.theme.colors)
    out.token_source = 'tailwindcss/resolveConfig'
  } catch (e) {
    out.resolve_config_error = String(e.message ?? e)
  }
}

// 2. The config alone, when the repo has no installed tailwindcss to resolve with.
if (!Object.keys(out.tokens).length && configPath) {
  try {
    const cfg = await loadConfig()
    const c = cfg.default ?? cfg
    out.tokens = flatten(c?.theme?.extend?.colors ?? c?.theme?.colors)
    if (Object.keys(out.tokens).length) out.token_source = 'config-require'
  } catch (e) {
    out.config_require_error = String(e.message ?? e)
  }
}

// 3. Tailwind v4 declares tokens as CSS custom properties rather than in a config.
if (!Object.keys(out.tokens).length) {
  const cssFiles = ['app/globals.css', 'src/app/globals.css', 'styles/globals.css',
                    'src/styles/globals.css'].map(f => join(repo, f)).filter(existsSync)
  const found = {}
  for (const f of cssFiles) {
    const css = readFileSync(f, 'utf8')
    for (const m of css.matchAll(/--color-([\w-]+)\s*:\s*([^;]+);/g)) found[m[1]] = m[2].trim()
    for (const m of css.matchAll(/--([\w-]+)\s*:\s*(#[0-9a-fA-F]{3,8})\s*;/g)) found[m[1]] = m[2]
  }
  if (Object.keys(found).length) {
    out.tokens = found
    out.token_source = 'css-custom-properties'
    out.css_files = cssFiles
  }
}

// 4. No repo tokens. Flagged, because snapping to stock Tailwind is a degraded
// answer that the interview must confirm rather than a resolved one.
if (!Object.keys(out.tokens).length) {
  out.token_source = 'tailwind-default'
  out.flag = 'repo tokens unresolved - ask for brand colours before snapping'
  // A .ts config that uses require() internally only loads inside the repo's own
  // toolchain, so name that cause instead of reporting a bare fallback.
  if (/require is not defined/.test(String(out.resolve_config_error ?? ''))
      && String(configPath ?? '').endsWith('.ts')) {
    out.flag = ('tailwind.config.ts uses require() and does not load under plain node - '
                + 'the repo tokens exist but are unreadable here; snap only after confirming colours')
  }
  try {
    out.tokens = flatten(require('tailwindcss/resolveConfig')(
      require('tailwindcss/defaultConfig')).theme.colors)
  } catch {
    // A repo without tailwindcss installed still needs a palette to snap against,
    // so fall back to the copy shipped with this skill rather than returning none.
    try {
      const here = new URL('./fixtures/tailwind-subset.json', import.meta.url)
      out.tokens = JSON.parse(readFileSync(here, 'utf8'))
      out.token_source = 'tailwind-default (bundled subset)'
    } catch { out.tokens = {} }
  }
}

out.count = Object.keys(out.tokens).length
process.stdout.write(JSON.stringify(out, null, 1))
