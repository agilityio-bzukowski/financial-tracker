import { apiClient } from "@/lib/api-client"
import type {
  LoginRequest,
  LoginResponse,
  RegisterRequest,
  UserResponse,
} from "./types"

export const authApi = {
  register(body: RegisterRequest): Promise<UserResponse> {
    return apiClient.post<UserResponse>("/auth/register", body).then((r) => r.data)
  },

  login(body: LoginRequest): Promise<LoginResponse> {
    return apiClient.post<LoginResponse>("/auth/login", body).then((r) => r.data)
  },

deleteMe(): Promise<void> {
    return apiClient.delete("/users/me").then(() => undefined)
  },
}
