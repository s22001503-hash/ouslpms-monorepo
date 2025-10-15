import React from 'react'
import { useAuth } from '../hooks/useAuth'
import { useNavigate } from 'react-router-dom'

export default function UserDashboard() {
  const { user, logout, userEpf } = useAuth()
  const navigate = useNavigate()

  return (
    <div style={{ padding: 20 }}>
  <h2>User Dashboard</h2>
      <div>
        <button onClick={() => navigate('/change-password')}>Change Password</button>
        <button
          onClick={async () => {
            await logout()
            navigate('/login')
          }}
        >
          Logout
        </button>
      </div>
    </div>
  )
}
