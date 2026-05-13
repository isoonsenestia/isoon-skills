# Hooks — Two Sub-patterns

Read before writing a data-fetching hook.

## Pages Router / no React Query: manual loading state

```typescript
// hooks/useAppointments.ts
export const useAppointments = (patientId: string) => {
  const [appointments, setAppointments] = useState<Appointment[]>([])
  const [loading, setLoading] = useState(false)
  const [isError, setIsError] = useState(false)

  const fetchAppointments = async () => {
    try {
      setLoading(true)
      setIsError(false)
      const data = await AppointmentService.getAppointments(patientId)
      setAppointments(data)
    } catch (error) {
      setIsError(true)
    } finally {
      setLoading(false)
    }
  }

  return { appointments, loading, isError, fetchAppointments }
}
```

## synphaet-care-app: React Query

```typescript
import { useQuery } from '@tanstack/react-query'

export function useAppointments(patientId: string) {
  const query = useQuery({
    queryKey: ['appointments', patientId],
    queryFn: () => AdminAppointmentService.getAppointments(patientId),
    staleTime: 25000,
  })
  return { data: query.data, isLoading: query.isLoading, error: query.error, refetch: query.refetch }
}
```

Pick based on `@tanstack/react-query` presence in `package.json`.
