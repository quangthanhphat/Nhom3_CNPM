import { useState } from 'react'
import './Register.css'

function Register({ onBackToLogin }) {
  const [formData, setFormData] = useState({
    username: '',
    email: '',
    password: '',
    full_name: '',
    phone: '',
  })

  const [error, setError] = useState('')
  const [success, setSuccess] = useState('')

  const handleChange = (e) => {
    const { name, value } = e.target

    setFormData({
      ...formData,
      [name]: value,
    })
  }

  const handleRegister = async (e) => {
    e.preventDefault()

    setError('')
    setSuccess('')

    try {
      const response = await fetch(
        'http://127.0.0.1:9999/auth/register',
        {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify(formData),
        }
      )

      const data = await response.json()

      if (!response.ok) {
        setError(data.message || 'Registration failed')
        return
      }

      setSuccess('Registration successful!')

      setFormData({
        username: '',
        email: '',
        password: '',
        full_name: '',
        phone: '',
      })

      setTimeout(() => {
        onBackToLogin()
      }, 1000)

    } catch (err) {
      setError('Cannot connect to backend server.')
    }
  }

  return (
    <div className="register-page">
      <div className="register-card">

        <h1>Create Account</h1>

        <p className="register-subtitle">
          Register for Film Lab Platform
        </p>

        <form onSubmit={handleRegister}>

          <div className="form-group">
            <label>Username</label>

            <input
              type="text"
              name="username"
              value={formData.username}
              onChange={handleChange}
              placeholder="Enter username"
              required
            />
          </div>

          <div className="form-group">
            <label>Email</label>

            <input
              type="email"
              name="email"
              value={formData.email}
              onChange={handleChange}
              placeholder="Enter email"
              required
            />
          </div>

          <div className="form-group">
            <label>Password</label>

            <input
              type="password"
              name="password"
              value={formData.password}
              onChange={handleChange}
              placeholder="Enter password"
              required
            />
          </div>

          <div className="form-group">
            <label>Full Name</label>

            <input
              type="text"
              name="full_name"
              value={formData.full_name}
              onChange={handleChange}
              placeholder="Enter full name"
              required
            />
          </div>

          <div className="form-group">
            <label>Phone</label>

            <input
              type="text"
              name="phone"
              value={formData.phone}
              onChange={handleChange}
              placeholder="Enter phone number"
            />
          </div>

          {error && (
            <p className="error-message">
              {error}
            </p>
          )}

          {success && (
            <p className="success-message">
              {success}
            </p>
          )}

          <button
            type="submit"
            className="register-submit-button"
          >
            Register
          </button>

        </form>

        <div className="back-login-section">

          <p>Already have an account?</p>

          <button
            className="back-login-button"
            onClick={onBackToLogin}
          >
            Back to Login
          </button>

        </div>

      </div>
    </div>
  )
}

export default Register