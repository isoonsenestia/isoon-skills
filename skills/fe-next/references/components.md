# Components — Two Patterns

Read before creating a new component or refactoring an existing one.

## Pattern A: `React.FC<Props>` — Pages Router repos

(account-service-application, synphaet-care-app)

```tsx
// components/AppointmentCard/AppointmentCard.tsx
interface AppointmentCardProps {
  label: string
  onAction?: () => void
}

const AppointmentCard: React.FC<AppointmentCardProps> = ({ label, onAction }) => {
  return <div className="flex items-center gap-2">{label}</div>
}

export default AppointmentCard
```

## Pattern B: `export default function` — App Router repos

(backoffice-app, NESTA_UI, patient-journey-app, growth-monitoring-application)

```tsx
// components/AppointmentCard/AppointmentCard.tsx
interface AppointmentCardProps {
  label: string
  onAction?: () => void
}

export default function AppointmentCard({ label, onAction }: AppointmentCardProps) {
  return <div className="flex items-center gap-2">{label}</div>
}
```

## Rules for both patterns

- **Default export** (not named)
- Props interface above the component
- No `any` in props
- **Tailwind CSS** for all styling — no CSS Modules, no inline styles
- UI controls: match the repo's library — see "UI control library" below
- App Router interactive components add `"use client"` at the top

## Picking which pattern

Run the profile commands in SKILL.md Step 3. The decision table there maps grep counts → pattern.

## UI control library — two flavors

Senestia Next.js repos split into two UI systems. Profile before importing anything:

```bash
grep '"antd"' package.json                    # AntD repos
ls src/components/ui 2>/dev/null               # shadcn/CVA repos
grep '"class-variance-authority"\|"@line/liff"' package.json
```

- **AntD repos** (backoffice-app, most admin apps): Ant Design for Table, Form, Modal, Tabs, Alert, Spin, Button. v4 Modal uses `visible`, v5 uses `open`.
- **shadcn/CVA repos** (patient-journey-app and other LINE LIFF apps): **no AntD.** Local primitives in `src/components/ui/*` built with `class-variance-authority` (e.g. `Button` with `variant`/`size`, `Input`). Icons from `react-icons` — match the design weight: `react-icons/fa` (solid) vs `react-icons/io5` `*Outline` (thin/iOS); both inherit `currentColor`, so text color drives icon color. Reuse these primitives; don't add AntD.

## Styling with Tailwind tokens (shadcn/CVA repos)

Colors are HSL CSS variables in `src/app/globals.css` (`--primary`, `--primary-light`, `--background`, `--error-active`, `--gray-*`) exposed as Tailwind classes (`bg-primary`, `text-error-active`). Figma tokens usually map to ones that already exist — grep before inventing.

- **`body` is `bg-background`, a tinted (often lavender) token — NOT white.** A page that must be white needs `bg-white` on a **full-width** wrapper (not just the centered content column).
- The CVA `Button` **`outline` variant base is `bg-background`** (same tint) → it looks purple on white. Override with `bg-white`.
- Merge classes with `cn()` (`@/lib/utils`, twMerge): **the className you pass wins over the variant's classes** (last conflicting class wins) — that's how you override `bg`, height (`h-12` = 48px), or weight. To keep a solid disabled color add `disabled:opacity-100` (base cva sets `disabled:opacity-50`) plus an explicit `bg-*`.
