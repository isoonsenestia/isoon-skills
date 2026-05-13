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
- Ant Design for UI controls (Table, Form, Modal, Tabs, Alert, Spin, Button)
- App Router interactive components add `"use client"` at the top

## Picking which pattern

Run the profile commands in SKILL.md Step 3. The decision table there maps grep counts → pattern.
