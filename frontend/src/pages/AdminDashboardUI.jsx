import React, { useState } from 'react'
import { useAuth } from '../hooks/useAuth'
import { createUser, deleteUser } from '../services/api'
import ChangePassword from '../components/ChangePassword'
import './AdminDashboardUI.css'

export default function AdminDashboardUI() {
  const { user, logout } = useAuth()
  const [form, setForm] = useState({ 
    epf: '', 
    name: '', 
    email: '', 
    password: '', 
    role: 'user', 
    department: '' 
  })
  const [deleteEpf, setDeleteEpf] = useState('')
  const [message, setMessage] = useState({ type: '', text: '' })
  const [deleteMessage, setDeleteMessage] = useState({ type: '', text: '' })
  const [loading, setLoading] = useState(false)
  const [deleteLoading, setDeleteLoading] = useState(false)
  const [activeView, setActiveView] = useState('add') // 'add', 'remove', or 'changePassword'
  const [showDeleteDialog, setShowDeleteDialog] = useState(false)
  const [showPassword, setShowPassword] = useState(false)

  const departments = ['Computer Science', 'Engineering', 'Mathematics', 'Library']

  const handleChange = (e) => setForm({ ...form, [e.target.name]: e.target.value })

  const handleAddUser = async (e) => {
    e.preventDefault()
    setLoading(true)
    setMessage({ type: '', text: '' })
    
    try {
      const result = await createUser(form)
      setMessage({ type: 'success', text: result.message || 'User created successfully!' })
      // Clear form on success
      setForm({ epf: '', name: '', email: '', password: '', role: 'user', department: '' })
    } catch (error) {
      setMessage({ type: 'error', text: error.message || 'Failed to create user' })
    } finally {
      setLoading(false)
    }
  }

  const handleRemoveUser = async (e) => {
    e.preventDefault()
    
    if (!deleteEpf || !deleteEpf.trim()) {
      setDeleteMessage({ type: 'error', text: 'Please enter an EPF number' })
      return
    }
    
    // Show confirmation dialog
    setShowDeleteDialog(true)
  }

  const confirmDelete = async () => {
    setShowDeleteDialog(false)
    setDeleteLoading(true)
    setDeleteMessage({ type: '', text: '' })
    
    try {
      const result = await deleteUser(deleteEpf.trim())
      setDeleteMessage({ type: 'success', text: result.message || `User ${deleteEpf.trim()} deleted successfully!` })
      setDeleteEpf('') // Clear form on success
    } catch (error) {
      setDeleteMessage({ type: 'error', text: error.message || 'Failed to delete user' })
    } finally {
      setDeleteLoading(false)
    }
  }

  const cancelDelete = () => {
    setShowDeleteDialog(false)
  }

  return (
    <div className="ad-root">
      <aside className="ad-sidebar">
        <div className="ad-brand">
          <img src="/OUSL LOGO.jpg" alt="OUSL" />
          <div className="ad-brand-text">EcoPrint Admin</div>
        </div>

        <nav className="ad-nav">
          <button 
            className={`ad-nav-item ${activeView === 'add' ? 'active' : ''}`}
            onClick={() => setActiveView('add')}
          >
            👤➕ Add User
          </button>
          <button 
            className={`ad-nav-item ${activeView === 'remove' ? 'active' : ''}`}
            onClick={() => setActiveView('remove')}
          >
            👤➖ Remove User
          </button>
          <button className="ad-nav-item">🔔 Notifications</button>
          <button className="ad-nav-item">📊 Generate Report</button>
          <button 
            className={`ad-nav-item ${activeView === 'changePassword' ? 'active' : ''}`}
            onClick={() => setActiveView('changePassword')}
          >
            🔒 Change Password
          </button>
        </nav>

        <div className="ad-logout">
          <button className="ad-logout-btn" onClick={async () => { await logout(); window.location.href = '/login' }}>
            ➡️ Logout
          </button>
        </div>
      </aside>

      <main className="ad-content">
        <header className="ad-header">
          <h1>Admin Dashboard - EcoPrint</h1>
        </header>

        <section className="ad-banner">
          <h2>Welcome, Administrator</h2>
          <p>Use this panel to manage users, view reports, and handle notifications.</p>
        </section>

        <section className="ad-main">
          {activeView === 'add' && (
            <div className="ad-card ad-add-user">
              <div className="ad-card-header">Add User</div>
              <form className="ad-card-body two-col" onSubmit={handleAddUser}>
                {message.text && (
                  <div className={`ad-message ${message.type}`} style={{ gridColumn: '1 / -1' }}>
                    {message.text}
                  </div>
                )}
                
                <div className="form-row">
                  <label>EPF Number</label>
                  <input name="epf" value={form.epf} onChange={handleChange} required />
                </div>
                <div className="form-row">
                  <label>Full Name</label>
                  <input name="name" value={form.name} onChange={handleChange} required />
                </div>
                <div className="form-row">
                  <label>Email Address</label>
                  <input name="email" value={form.email} onChange={handleChange} type="email" required />
                </div>
                <div className="form-row">
                  <label>Password</label>
                  <div className="ad-password-wrapper">
                    <input 
                      name="password" 
                      value={form.password} 
                      onChange={handleChange} 
                      type={showPassword ? 'text' : 'password'} 
                      required 
                      minLength={6} 
                    />
                    <button
                      type="button"
                      className="ad-toggle-password-btn"
                      onClick={() => setShowPassword(!showPassword)}
                      aria-label={showPassword ? 'Hide password' : 'Show password'}
                    >
                      {showPassword ? (
                        <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                          <path d="M17.94 17.94A10.07 10.07 0 0 1 12 20c-7 0-11-8-11-8a18.45 18.45 0 0 1 5.06-5.94M9.9 4.24A9.12 9.12 0 0 1 12 4c7 0 11 8 11 8a18.5 18.5 0 0 1-2.16 3.19m-6.72-1.07a3 3 0 1 1-4.24-4.24"></path>
                          <line x1="1" y1="1" x2="23" y2="23"></line>
                        </svg>
                      ) : (
                        <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                          <path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"></path>
                          <circle cx="12" cy="12" r="3"></circle>
                        </svg>
                      )}
                    </button>
                  </div>
                </div>
                <div className="form-row">
                  <label>Role</label>
                  <select name="role" value={form.role} onChange={handleChange} required>
                    <option value="user">User</option>
                    <option value="admin">Admin</option>
                  </select>
                </div>
                <div className="form-row">
                  <label>Department</label>
                  <select name="department" value={form.department} onChange={handleChange} required>
                    <option value="">Select department</option>
                    {departments.map(d => (
                      <option key={d} value={d}>{d}</option>
                    ))}
                  </select>
                </div>

                <div className="form-actions">
                  <button type="submit" className="ad-btn primary" disabled={loading}>
                    {loading ? 'Adding User...' : 'Add User'}
                  </button>
                </div>
              </form>
            </div>
          )}

          {activeView === 'remove' && (
            <div className="ad-card ad-remove-user">
              <div className="ad-card-header">Remove User</div>
              <form className="ad-card-body" onSubmit={handleRemoveUser}>
                {deleteMessage.text && (
                  <div className={`ad-message ${deleteMessage.type}`}>
                    {deleteMessage.text}
                  </div>
                )}
                
                <div className="form-row">
                  <label>EPF Number</label>
                  <input 
                    type="text"
                    value={deleteEpf} 
                    onChange={(e) => setDeleteEpf(e.target.value)} 
                    placeholder="Enter EPF number to remove"
                    required 
                  />
                </div>

                <div className="ad-warning-box">
                  <strong>⚠️ Warning:</strong> This action will permanently delete the user from both Firebase Authentication and Firestore database. This cannot be undone.
                </div>

                <div className="form-actions">
                  <button type="submit" className="ad-btn danger" disabled={deleteLoading}>
                    {deleteLoading ? 'Deleting User...' : 'Delete User'}
                  </button>
                  <button 
                    type="button" 
                    className="ad-btn secondary" 
                    onClick={() => {
                      setDeleteEpf('')
                      setDeleteMessage({ type: '', text: '' })
                    }}
                    disabled={deleteLoading}
                  >
                    Clear
                  </button>
                </div>
              </form>
            </div>
          )}

          {activeView === 'changePassword' && (
            <div className="ad-card">
              <ChangePassword
                onSuccess={() => {
                  // Optionally redirect or show a message
                  console.log('Password changed successfully')
                }}
                onCancel={() => setActiveView('add')}
              />
            </div>
          )}
        </section>
      </main>

      {/* Delete Confirmation Dialog */}
      {showDeleteDialog && (
        <div className="modal-overlay" onClick={cancelDelete}>
          <div className="modal-dialog" onClick={(e) => e.stopPropagation()}>
            <div className="modal-header">
              <h3>⚠️ Confirm Delete</h3>
              <button className="modal-close" onClick={cancelDelete}>&times;</button>
            </div>
            <div className="modal-body">
              <p className="modal-warning">You are about to permanently delete user:</p>
              <div className="modal-user-info">
                <strong>EPF:</strong> {deleteEpf}
              </div>
              <div className="modal-consequences">
                <p><strong>This action will:</strong></p>
                <ul>
                  <li>Remove the user from Firebase Authentication</li>
                  <li>Delete all user data from Firestore</li>
                  <li><strong>This action CANNOT be undone</strong></li>
                </ul>
              </div>
              <p className="modal-question">Are you sure you want to proceed?</p>
            </div>
            <div className="modal-footer">
              <button className="ad-btn secondary" onClick={cancelDelete}>
                Cancel
              </button>
              <button className="ad-btn danger" onClick={confirmDelete}>
                Yes, Delete User
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  )
}
