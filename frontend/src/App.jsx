import React from 'react'
import { Routes, Route, Navigate } from 'react-router-dom'
import LoginPage from './pages/LoginPage'
import UserDashboard from './pages/UserDashboard'
import AdminDashboard from './pages/AdminDashboard'
import DeanDashboard from './pages/DeanDashboard'
import UserDashboardUI from './pages/UserDashboardUI'
import AdminDashboardUI from './pages/AdminDashboardUI'
import DeanDashboardUI from './pages/DeanDashboardUI'
import ChangePassword from './pages/ChangePassword'
import { AuthProvider, useAuth } from './hooks/useAuth'

function ProtectedRoute({ children, role }) {
  const { user, userRole, loading } = useAuth()
  
  // Show loading state while auth is being determined
  if (loading) return <div style={{padding: 20}}>Loading...</div>
  
  // Not logged in - redirect to login (with replace to prevent back button loop)
  if (!user) return <Navigate to="/login" replace />
  
  // If a specific role is required and user doesn't have it, redirect
  if (role && userRole && userRole !== role) {
    // Redirect to correct dashboard based on actual role (with replace)
    if (userRole === 'admin') return <Navigate to="/admin" replace />
    if (userRole === 'dean') return <Navigate to="/dean" replace />
    if (userRole === 'vc') return <Navigate to="/vc" replace />
    if (userRole === 'user') return <Navigate to="/user" replace />
    return <Navigate to="/login" replace />
  }
  
  return children
}

export default function App() {
  return (
    <AuthProvider>
      <Routes>
        <Route path="/login" element={<LoginPage />} />
        <Route
          path="/user"
          element={
            <ProtectedRoute role="user">
              <UserDashboardUI />
            </ProtectedRoute>
          }
        />
        <Route
          path="/admin"
          element={
            <ProtectedRoute role="admin">
              <AdminDashboardUI />
            </ProtectedRoute>
          }
        />
        <Route
          path="/dean"
          element={
            <ProtectedRoute role="dean">
              <DeanDashboardUI />
            </ProtectedRoute>
          }
        />
        <Route
          path="/vc"
          element={
            <ProtectedRoute role="vc">
              <DeanDashboardUI />
            </ProtectedRoute>
          }
        />
        <Route
          path="/change-password"
          element={
            <ProtectedRoute>
              <ChangePassword />
            </ProtectedRoute>
          }
        />
        <Route path="/" element={<Navigate to="/login" replace />} />
      </Routes>
    </AuthProvider>
  )
}
