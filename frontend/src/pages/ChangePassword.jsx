import React, { useState } from 'react'
import { useAuth } from '../hooks/useAuth'
import { useNavigate } from 'react-router-dom'

export default function ChangePassword() {
  const { changePassword } = useAuth()
  const [password, setPassword] = useState('')
  const [message, setMessage] = useState(null)
  const navigate = useNavigate()

  const handleSubmit = async (e) => {
    e.preventDefault()
    setMessage(null)
    try {
      await changePassword(password)
      setMessage('Password changed successfully')
      setTimeout(() => navigate('/'), 1000)
    } catch (err) {
      setMessage(err.message)
    }
  }

  return (
    <div style={{ padding: 20 }}>
      <h2>Change Password</h2>
      <form onSubmit={handleSubmit}>
        <div>
          <label>New Password:</label>
          <input type="password" value={password} onChange={(e) => setPassword(e.target.value)} required />
        </div>
        <button type="submit">Change</button>
      </form>
      {message && <div>{message}</div>}
    </div>
  )
}
