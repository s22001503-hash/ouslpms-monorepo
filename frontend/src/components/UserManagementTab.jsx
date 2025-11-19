import React, { useState } from 'react'
import { createUser, deleteUser } from '../services/api'
import './UserManagementTab.css'

export default function UserManagementTab() {
  const [activeSection, setActiveSection] = useState('add') // 'add' or 'remove'
  
  // Add User State
  const [addForm, setAddForm] = useState({ 
    epf: '', 
    name: '', 
    email: '', 
    password: '', 
    role: 'user', 
    department: '' 
  })
  const [addMessage, setAddMessage] = useState({ type: '', text: '' })
  const [addLoading, setAddLoading] = useState(false)
  const [showPassword, setShowPassword] = useState(false)
  
  // Remove User State
  const [deleteEpf, setDeleteEpf] = useState('')
  const [deleteMessage, setDeleteMessage] = useState({ type: '', text: '' })
  const [deleteLoading, setDeleteLoading] = useState(false)
  const [showDeleteDialog, setShowDeleteDialog] = useState(false)

  const departments = ['Computer Science', 'Engineering', 'Mathematics', 'Library']

  const handleAddChange = (e) => setAddForm({ ...addForm, [e.target.name]: e.target.value })

  const handleAddUser = async (e) => {
    e.preventDefault()
    setAddLoading(true)
    setAddMessage({ type: '', text: '' })
    
    try {
      const result = await createUser(addForm)
      setAddMessage({ type: 'success', text: result.message || 'User created successfully!' })
      // Clear form on success
      setAddForm({ epf: '', name: '', email: '', password: '', role: 'user', department: '' })
    } catch (error) {
      setAddMessage({ type: 'error', text: error.message || 'Failed to create user' })
    } finally {
      setAddLoading(false)
    }
  }

  const handleRemoveUser = async (e) => {
    e.preventDefault()
    
    if (!deleteEpf || !deleteEpf.trim()) {
      setDeleteMessage({ type: 'error', text: 'Please enter an EPF number' })
      return
    }
    
    setShowDeleteDialog(true)
  }

  const confirmDelete = async () => {
    setShowDeleteDialog(false)
    setDeleteLoading(true)
    setDeleteMessage({ type: '', text: '' })
    
    try {
      const result = await deleteUser(deleteEpf.trim())
      setDeleteMessage({ type: 'success', text: result.message || `User ${deleteEpf.trim()} deleted successfully!` })
      setDeleteEpf('')
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
    <div className="user-management-tab">
      <div className="umt-header">
        <h2>User Management</h2>
        <p>Add new users or remove existing users from the system</p>
      </div>

      {/* Section Tabs */}
      <div className="umt-section-tabs">
        <button
          className={`umt-tab ${activeSection === 'add' ? 'active' : ''}`}
          onClick={() => setActiveSection('add')}
        >
          👤➕ Add User
        </button>
        <button
          className={`umt-tab ${activeSection === 'remove' ? 'active' : ''}`}
          onClick={() => setActiveSection('remove')}
        >
          👤➖ Remove User
        </button>
      </div>

      {/* Add User Section */}
      {activeSection === 'add' && (
        <div className="umt-section umt-add-user">
          <h3>Add New User</h3>
          <form onSubmit={handleAddUser}>
            {addMessage.text && (
              <div className={`umt-message ${addMessage.type}`}>
                {addMessage.text}
              </div>
            )}
            
            <div className="umt-form-grid">
              <div className="umt-form-row">
                <label>EPF Number *</label>
                <input 
                  name="epf" 
                  value={addForm.epf} 
                  onChange={handleAddChange} 
                  placeholder="e.g., 10001"
                  required 
                />
              </div>

              <div className="umt-form-row">
                <label>Full Name *</label>
                <input 
                  name="name" 
                  value={addForm.name} 
                  onChange={handleAddChange}
                  placeholder="e.g., John Doe"
                  required 
                />
              </div>

              <div className="umt-form-row">
                <label>Email Address *</label>
                <input 
                  name="email" 
                  value={addForm.email} 
                  onChange={handleAddChange} 
                  type="email"
                  placeholder="e.g., john.doe@ousl.lk"
                  required 
                />
              </div>

              <div className="umt-form-row">
                <label>Password *</label>
                <div className="umt-password-wrapper">
                  <input 
                    name="password" 
                    value={addForm.password} 
                    onChange={handleAddChange} 
                    type={showPassword ? 'text' : 'password'} 
                    placeholder="Minimum 6 characters"
                    required 
                    minLength={6} 
                  />
                  <button
                    type="button"
                    className="umt-toggle-password-btn"
                    onClick={() => setShowPassword(!showPassword)}
                    aria-label={showPassword ? 'Hide password' : 'Show password'}
                  >
                    {showPassword ? '👁️' : '👁️‍🗨️'}
                  </button>
                </div>
              </div>

              <div className="umt-form-row">
                <label>Role *</label>
                <select name="role" value={addForm.role} onChange={handleAddChange} required>
                  <option value="user">User</option>
                  <option value="admin">Admin</option>
                </select>
              </div>

              <div className="umt-form-row">
                <label>Department *</label>
                <select name="department" value={addForm.department} onChange={handleAddChange} required>
                  <option value="">Select department</option>
                  {departments.map(d => (
                    <option key={d} value={d}>{d}</option>
                  ))}
                </select>
              </div>
            </div>

            <div className="umt-form-actions">
              <button type="submit" className="umt-btn primary" disabled={addLoading}>
                {addLoading ? '⏳ Adding User...' : '✅ Add User'}
              </button>
              <button 
                type="button" 
                className="umt-btn secondary"
                onClick={() => {
                  setAddForm({ epf: '', name: '', email: '', password: '', role: 'user', department: '' })
                  setAddMessage({ type: '', text: '' })
                }}
                disabled={addLoading}
              >
                🔄 Clear Form
              </button>
            </div>
          </form>
        </div>
      )}

      {/* Remove User Section */}
      {activeSection === 'remove' && (
        <div className="umt-section umt-remove-user">
          <h3>Remove User</h3>
          <form onSubmit={handleRemoveUser}>
            {deleteMessage.text && (
              <div className={`umt-message ${deleteMessage.type}`}>
                {deleteMessage.text}
              </div>
            )}
            
            <div className="umt-form-row">
              <label>EPF Number *</label>
              <input 
                type="text"
                value={deleteEpf} 
                onChange={(e) => setDeleteEpf(e.target.value)} 
                placeholder="Enter EPF number to remove"
                required 
              />
            </div>

            <div className="umt-warning-box">
              <strong>⚠️ Warning:</strong> This action will permanently delete the user from both Firebase Authentication and Firestore database. This cannot be undone.
            </div>

            <div className="umt-form-actions">
              <button type="submit" className="umt-btn danger" disabled={deleteLoading}>
                {deleteLoading ? '⏳ Deleting User...' : '🗑️ Delete User'}
              </button>
              <button 
                type="button" 
                className="umt-btn secondary" 
                onClick={() => {
                  setDeleteEpf('')
                  setDeleteMessage({ type: '', text: '' })
                }}
                disabled={deleteLoading}
              >
                🔄 Clear
              </button>
            </div>
          </form>
        </div>
      )}

      {/* Delete Confirmation Dialog */}
      {showDeleteDialog && (
        <div className="umt-modal-overlay">
          <div className="umt-modal">
            <div className="umt-modal-header">
              <h3>⚠️ Confirm Deletion</h3>
            </div>
            <div className="umt-modal-body">
              <p>Are you sure you want to delete user with EPF <strong>{deleteEpf}</strong>?</p>
              <p>This action cannot be undone.</p>
            </div>
            <div className="umt-modal-actions">
              <button className="umt-btn danger" onClick={confirmDelete}>
                Yes, Delete
              </button>
              <button className="umt-btn secondary" onClick={cancelDelete}>
                Cancel
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  )
}
