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

/**
 * Fetch admin overview statistics
 */
export async function fetchOverviewStats() {
  try {
    const token = await getFreshToken()
    const res = await fetch(`${API_BASE}/admin/overview`, {
      method: 'GET',
      headers: {
        'Authorization': `Bearer ${token}`,
      },
    })
    if (!res.ok) {
      const error = await res.json().catch(() => ({ detail: 'Failed to fetch overview stats' }))
      throw new Error(error.detail || `Failed to fetch overview stats: ${res.status}`)
    }
    return res.json()
  } catch (error) {
    if (error instanceof TypeError && error.message.includes('fetch')) {
      throw new Error('Network error: Cannot connect to server. Please check if backend is running.')
    }
    throw error
  }
}

/**
 * Fetch current system settings
 */
export async function fetchSystemSettings() {
  try {
    const token = await getFreshToken()
    const res = await fetch(`${API_BASE}/system-settings`, {
      method: 'GET',
      headers: {
        'Authorization': `Bearer ${token}`,
      },
    })
    if (!res.ok) {
      const error = await res.json().catch(() => ({ detail: 'Failed to fetch system settings' }))
      throw new Error(error.detail || `Failed to fetch system settings: ${res.status}`)
    }
    return res.json()
  } catch (error) {
    if (error instanceof TypeError && error.message.includes('fetch')) {
      throw new Error('Network error: Cannot connect to server. Please check if backend is running.')
    }
    throw error
  }
}

/**
 * Fetch settings proposal history for an admin
 */
export async function fetchSettingsRequests(adminId) {
  try {
    const token = await getFreshToken()
    const res = await fetch(`${API_BASE}/settings-requests?adminId=${adminId}`, {
      method: 'GET',
      headers: {
        'Authorization': `Bearer ${token}`,
      },
    })
    if (!res.ok) {
      const error = await res.json().catch(() => ({ detail: 'Failed to fetch settings requests' }))
      throw new Error(error.detail || `Failed to fetch settings requests: ${res.status}`)
    }
    return res.json()
  } catch (error) {
    if (error instanceof TypeError && error.message.includes('fetch')) {
      throw new Error('Network error: Cannot connect to server. Please check if backend is running.')
    }
    throw error
  }
}

/**
 * Propose new system settings (admin only)
 */
export async function proposeSettings(proposal) {
  try {
    const token = await getFreshToken()
    const res = await fetch(`${API_BASE}/admin/propose-settings`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${token}`,
      },
      body: JSON.stringify(proposal),
    })
    if (!res.ok) {
      const error = await res.json().catch(() => ({ detail: 'Failed to propose settings' }))
      throw new Error(error.detail || `Failed to propose settings: ${res.status}`)
    }
    return res.json()
  } catch (error) {
    if (error instanceof TypeError && error.message.includes('fetch')) {
      throw new Error('Network error: Cannot connect to server. Please check if backend is running.')
    }
    throw error
  }
}

// ==================== Dean-specific API calls ====================

/**
 * Fetch Dean overview statistics
 */
export async function fetchDeanOverview() {
  try {
    const token = await getFreshToken()
    const res = await fetch(`${API_BASE}/dean/overview`, {
      method: 'GET',
      headers: {
        'Authorization': `Bearer ${token}`,
      },
    })
    if (!res.ok) {
      const error = await res.json().catch(() => ({ detail: 'Failed to fetch dean overview' }))
      throw new Error(error.detail || `Failed to fetch dean overview: ${res.status}`)
    }
    return res.json()
  } catch (error) {
    if (error instanceof TypeError && error.message.includes('fetch')) {
      throw new Error('Network error: Cannot connect to server. Please check if backend is running.')
    }
    throw error
  }
}

/**
 * Fetch settings proposals (pending by default)
 */
export async function fetchSettingsProposals(status = 'pending') {
  try {
    const token = await getFreshToken()
    const res = await fetch(`${API_BASE}/dean/settings-requests?status=${status}`, {
      method: 'GET',
      headers: {
        'Authorization': `Bearer ${token}`,
      },
    })
    if (!res.ok) {
      const error = await res.json().catch(() => ({ detail: 'Failed to fetch proposals' }))
      throw new Error(error.detail || `Failed to fetch proposals: ${res.status}`)
    }
    return res.json()
  } catch (error) {
    if (error instanceof TypeError && error.message.includes('fetch')) {
      throw new Error('Network error: Cannot connect to server. Please check if backend is running.')
    }
    throw error
  }
}

/**
 * Approve a settings proposal
 */
export async function approveSettingsProposal(proposalId, deanId, deanName, notes = '') {
  try {
    const token = await getFreshToken()
    const res = await fetch(`${API_BASE}/dean/settings/approve`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${token}`,
      },
      body: JSON.stringify({ proposalId, deanId, deanName, notes }),
    })
    if (!res.ok) {
      const error = await res.json().catch(() => ({ detail: 'Failed to approve proposal' }))
      throw new Error(error.detail || `Failed to approve proposal: ${res.status}`)
    }
    return res.json()
  } catch (error) {
    if (error instanceof TypeError && error.message.includes('fetch')) {
      throw new Error('Network error: Cannot connect to server. Please check if backend is running.')
    }
    throw error
  }
}

/**
 * Reject a settings proposal
 */
export async function rejectSettingsProposal(proposalId, deanId, deanName, reason = '') {
  try {
    const token = await getFreshToken()
    const res = await fetch(`${API_BASE}/dean/settings/reject`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${token}`,
      },
      body: JSON.stringify({ proposalId, deanId, deanName, reason }),
    })
    if (!res.ok) {
      const error = await res.json().catch(() => ({ detail: 'Failed to reject proposal' }))
      throw new Error(error.detail || `Failed to reject proposal: ${res.status}`)
    }
    return res.json()
  } catch (error) {
    if (error instanceof TypeError && error.message.includes('fetch')) {
      throw new Error('Network error: Cannot connect to server. Please check if backend is running.')
    }
    throw error
  }
}

/**
 * Fetch Dean notifications
 */
export async function fetchDeanNotifications() {
  try {
    const token = await getFreshToken()
    const res = await fetch(`${API_BASE}/dean/notifications`, {
      method: 'GET',
      headers: {
        'Authorization': `Bearer ${token}`,
      },
    })
    if (!res.ok) {
      const error = await res.json().catch(() => ({ detail: 'Failed to fetch notifications' }))
      throw new Error(error.detail || `Failed to fetch notifications: ${res.status}`)
    }
    return res.json()
  } catch (error) {
    if (error instanceof TypeError && error.message.includes('fetch')) {
      throw new Error('Network error: Cannot connect to server. Please check if backend is running.')
    }
    throw error
  }
}

/**
 * Fetch Dean reports
 */
export async function fetchDeanReports() {
  try {
    const token = await getFreshToken()
    const res = await fetch(`${API_BASE}/dean/reports`, {
      method: 'GET',
      headers: {
        'Authorization': `Bearer ${token}`,
      },
    })
    if (!res.ok) {
      const error = await res.json().catch(() => ({ detail: 'Failed to fetch reports' }))
      throw new Error(error.detail || `Failed to fetch reports: ${res.status}`)
    }
    return res.json()
  } catch (error) {
    if (error instanceof TypeError && error.message.includes('fetch')) {
      throw new Error('Network error: Cannot connect to server. Please check if backend is running.')
    }
    throw error
  }
}

