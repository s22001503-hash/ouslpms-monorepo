// API service with automatic token refresh
import { getAuth } from 'firebase/auth'

const API_BASE = import.meta.env.VITE_API_BASE || 'http://localhost:8000'

/**
 * Get a fresh Firebase Auth token (auto-refreshes if needed)
 */
async function getFreshToken() {
  const auth = getAuth()
  if (!auth.currentUser) {
    throw new Error('Not authenticated')
  }
  // Force refresh if token is close to expiring
  return await auth.currentUser.getIdToken(true)
}

/**
 * Verify Firebase ID token with backend
 */
export async function verifyToken(idToken) {
  const res = await fetch(`${API_BASE}/auth/verify`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ idToken }),
  })
  if (!res.ok) {
    const text = await res.text()
    throw new Error(`Failed to verify token: ${res.status} ${text}`)
  }
  return res.json()
}

/**
 * Create a new user (admin only)
 */
export async function createUser(userData) {
  try {
    const token = await getFreshToken()
    const res = await fetch(`${API_BASE}/auth/create-user`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${token}`,
      },
      body: JSON.stringify(userData),
    })
    if (!res.ok) {
      const error = await res.json().catch(() => ({ detail: 'Failed to create user' }))
      throw new Error(error.detail || `Failed to create user: ${res.status}`)
    }
    return res.json()
  } catch (error) {
    // Handle network errors specifically
    if (error instanceof TypeError && error.message.includes('fetch')) {
      throw new Error('Network error: Cannot connect to server. Please check if backend is running.')
    }
    throw error
  }
}

/**
 * Delete a user by EPF (admin only)
 */
export async function deleteUser(epf) {
  try {
    console.log('Deleting user with EPF:', epf)
    console.log('API_BASE:', API_BASE)
    const token = await getFreshToken()
    console.log('Token obtained, making request...')
    const res = await fetch(`${API_BASE}/auth/delete-user`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${token}`,
      },
      body: JSON.stringify({ epf }),
    })
    console.log('Response received:', res.status, res.statusText)
    if (!res.ok) {
      const error = await res.json().catch(() => ({ detail: 'Failed to delete user' }))
      throw new Error(error.detail || `Failed to delete user: ${res.status}`)
    }
    return res.json()
  } catch (error) {
    console.error('Delete user error:', error)
    // Don't override authentication or other specific errors
    if (error.message === 'Not authenticated') {
      throw error
    }
    // Handle network errors specifically - fetch() throws TypeError for network issues
    if (error.name === 'TypeError' || error.message.toLowerCase().includes('failed to fetch')) {
      throw new Error('Network error: Cannot connect to server. Please check if backend is running.')
    }
    throw error
  }
}

/**
 * Change password for the authenticated user
 */
export async function changePassword(currentPassword, newPassword) {
  try {
    const token = await getFreshToken()
    const res = await fetch(`${API_BASE}/auth/change-password`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${token}`,
      },
      body: JSON.stringify({ currentPassword, newPassword }),
    })
    if (!res.ok) {
      const error = await res.json().catch(() => ({ detail: 'Failed to change password' }))
      throw new Error(error.detail || `Failed to change password: ${res.status}`)
    }
    return res.json()
  } catch (error) {
    // Handle network errors specifically
    if (error instanceof TypeError && error.message.includes('fetch')) {
      throw new Error('Network error: Cannot connect to server. Please check if backend is running.')
    }
    throw error
  }
}

