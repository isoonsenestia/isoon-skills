# Axios Configuration — Three Patterns

Read before configuring HTTP or fixing a request-layer bug.

## Pages Router: `next/config` publicRuntimeConfig

```typescript
// services/axios.config.ts
import axios from 'axios'
import getConfig from 'next/config'

const { publicRuntimeConfig } = getConfig()

const customAxios = axios.create({
  baseURL: publicRuntimeConfig.baseURL,
  withCredentials: true,
})

export default customAxios
```

Multiple instances for multiple services (synphaet-care-app):
```typescript
export const axiosForAccountApi = axios.create({
  baseURL: publicRuntimeConfig.accountServiceApiBaseURL,
  withCredentials: true,
})
```

## App Router + Redux: runtime config via `/api/config` route (backoffice-app)

Express serves env vars at runtime. Pages dispatch `getConfig()` first, then use the URLs from Redux to dispatch feature thunks. **Never hardcode base URLs.**

## App Router + proxy: `/proxy` with 401 interceptor (growth-monitoring-application)

```typescript
// utils/helpers/axios-request.ts
import axios from "axios"

export const axiosAuthInstance = axios.create({
  baseURL: "/proxy",
  withCredentials: true,
  timeout: 10000,
})

axiosAuthInstance.interceptors.response.use(
  (res) => res,
  (error) => {
    if (error?.response?.status === 401) window.location.replace("/login")
    return Promise.reject(error)
  }
)
```
