import { createFileRoute, Outlet, redirect } from "@tanstack/react-router"

export const Route = createFileRoute("/_authenticated")({
  beforeLoad: ({ location }) => {
    const token = localStorage.getItem("token")
    if (!token) {
      throw redirect({
        to: "/auth/login",
        search: { redirect: location.href },
      })
    }
  },
  component: () => <Outlet />,
})
