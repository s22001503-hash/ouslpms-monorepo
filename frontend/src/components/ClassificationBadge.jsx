import React from 'react'
import './ClassificationBadge.css'

/**
 * ClassificationBadge - Display AI document classification
 * @param {string} type - 'official', 'personal', 'confidential'
 * @param {string} size - 'small', 'medium', 'large'
 */
export default function ClassificationBadge({ type, size = 'medium' }) {
  const badges = {
    official: {
      icon: '📄',
      label: 'Official',
      className: 'cb-official'
    },
    personal: {
      icon: '👤',
      label: 'Personal',
      className: 'cb-personal'
    },
    confidential: {
      icon: '🔒',
      label: 'Confidential',
      className: 'cb-confidential'
    },
    processing: {
      icon: '⏳',
      label: 'Processing...',
      className: 'cb-processing'
    }
  }

  const badge = badges[type?.toLowerCase()] || badges.processing

  return (
    <span className={`classification-badge ${badge.className} cb-${size}`}>
      <span className="cb-icon">{badge.icon}</span>
      <span className="cb-label">{badge.label}</span>
    </span>
  )
}
