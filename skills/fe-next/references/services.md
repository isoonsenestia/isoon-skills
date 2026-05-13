# Services / Repositories — Three Patterns

Read before adding or modifying an API call.

## Pattern A: `XxxService` object

Pages Router: account-service-application, synphaet-care-app.

```typescript
// services/appointmentService/getAppointments.ts
import axios from '@/axios.config'
import { BaseResponse } from '../base'

interface AppointmentApiResponse extends BaseResponse {
  data: Appointment[]
}

const getAppointments = async (patientId: string): Promise<Appointment[]> => {
  const res = await axios.get<AppointmentApiResponse>(`/v1/appointments?patientId=${patientId}`)
  return res.data.data
}

// services/appointmentService/index.ts
const AppointmentService = { getAppointments }
export default AppointmentService
```

`BaseResponse` (from `services/base.ts`):
```typescript
export interface BaseResponse {
  code: number
  success: boolean
}
```

## Pattern B: `xxxRepository` object

App Router, no Redux: growth-monitoring-application.

```typescript
// app/(authorized)/_repositories/appointment.ts
import { axiosAuthInstance } from "@utils/helpers/axios-request"

const getAppointments = async (patientId: string): Promise<Appointment[]> => {
  const response = await axiosAuthInstance.get(`/v1/appointments?patientId=${patientId}`)
  return response.data as Appointment[]
}

export const appointmentRepository = { getAppointments }
```

## Pattern C: Inline axios call in `createAsyncThunk`

App Router + Redux: backoffice-app, NESTA_UI, patient-journey-app.

```typescript
// redux/thunks/getAppointmentsThunk.ts  (backoffice-app pattern)
import { createAsyncThunk } from "@reduxjs/toolkit"
import axios from "axios"

type Args = { apiBaseURL: string; apiKey: string }

export const getAppointmentsThunk = createAsyncThunk<Appointment[], Args, { rejectValue: string }>(
  "appointments/getAll",
  async ({ apiBaseURL, apiKey }, thunkAPI) => {
    try {
      const response = await axios.get<Appointment[]>(`${apiBaseURL}/v1/appointments`, {
        headers: { "X-Api-Key": apiKey },
      })
      return response.data
    } catch (error: unknown) {
      const msg = (error as { response?: { data: string } }).response?.data || "Failed to fetch"
      return thunkAPI.rejectWithValue(msg)
    }
  }
)
```

## Rule

Never put axios calls directly in components or pages.
