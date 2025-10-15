import React from 'react'

export default function Header({ title }) {
  return (
    <header style={{ padding: 10, borderBottom: '1px solid #ddd' }}>
      <h1>{title}</h1>
    </header>
  )
}
