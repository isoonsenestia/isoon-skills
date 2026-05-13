# Forms — Three Patterns

Pick by complexity:

| Form complexity | Pattern |
|---|---|
| 3+ fields with validation rules | Formik + Yup — extract into `useForm` hook |
| CRUD modals, admin data entry | Ant Design `<Form>` with `Form.useForm()` |
| 1–2 field inputs (search, toggle) | Plain `useState` |

## Formik + Yup (growth-monitoring-application, health-checkup-app)

```typescript
// app/(unauthorized)/login/_hook/useForm.tsx
import { useFormik } from "formik"
import * as Yup from "yup"

export const useForm = (onSubmit: (username: string, password: string) => void) => {
  const formik = useFormik({
    initialValues: { username: "", password: "" },
    validationSchema: Yup.object().shape({
      username: Yup.string().required("Required"),
      password: Yup.string().required("Required"),
    }),
    validateOnChange: false,
    validateOnBlur: false,
    onSubmit: (values, helpers) => {
      helpers.setSubmitting(true)
      onSubmit(values.username, values.password)
    },
  })
  return [formik]
}
```

## Ant Design Form (backoffice-app)

```tsx
"use client"
import { Form, Input, Button } from "antd"

export default function EditHospitalForm({ onSubmit }: { onSubmit: (v: FormValues) => void }) {
  const [form] = Form.useForm()
  return (
    <Form form={form} onFinish={onSubmit} layout="vertical">
      <Form.Item name="name" label={t("hospital.name")} rules={[{ required: true }]}>
        <Input />
      </Form.Item>
      <Button type="primary" htmlType="submit">{t("common.save")}</Button>
    </Form>
  )
}
```
