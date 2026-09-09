import { useState } from 'react'
import './App.css'
import Register from './components/components_Common/Register'
import Dashboard from './components/components_FilmLabOwner/Dashboard'
import Dashboard_Admin from './components/components_Admin/Dashboard_Admin'

function App() {
  const [showRegister, setShowRegister] = useState(false)
  const [showForgotPassword, setShowForgotPassword] = useState(false)

  const [username, setUsername] = useState('')
  const [password, setPassword] = useState('')

  const [error, setError] = useState('')

  const [loggedInUser, setLoggedInUser] = useState(() => {
    const savedUser = localStorage.getItem('user')

    if (savedUser) {
      try {
        return JSON.parse(savedUser)
      } catch {
        localStorage.removeItem('user')
        return null
      }
    }

    return null
  })

  // =========================
  // LOGIN
  // =========================

  const handleLogin = async (e) => {
    e.preventDefault()

    setError('')
    setShowForgotPassword(false)

    try {
      const response = await fetch(
        'http://127.0.0.1:9999/auth/login',
        {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({
            username,
            password,
          }),
        }
      )

      const data = await response.json()

      if (!response.ok) {
        setError(data.message || 'Incorrect username or password.')
        setShowForgotPassword(true)
        return
      }

      // Backend trả về "token"
      localStorage.setItem('token', data.token)

      localStorage.setItem(
        'user',
        JSON.stringify(data.user)
      )

      setLoggedInUser(data.user)

      setUsername('')
      setPassword('')
    } catch (err) {
      setError('Cannot connect to backend server.')
    }
  }

  // =========================
  // LOGOUT
  // =========================

  const handleLogout = () => {
    localStorage.removeItem('token')
    localStorage.removeItem('user')

    setLoggedInUser(null)
    setUsername('')
    setPassword('')
    setError('')
    setShowForgotPassword(false)
  }

  // =========================
  // LOGGED IN
  // =========================

  if (loggedInUser) {

    // ADMIN
    if (loggedInUser.role === 'admin') {
      return (
        <Dashboard_Admin
          user={loggedInUser}
          onLogout={handleLogout}
        />
      )
    }

    // FILM LAB OWNER
    return (
      <Dashboard
        user={loggedInUser}
        onLogout={handleLogout}
      />
    )
  }

  // =========================
  // REGISTER
  // =========================

  if (showRegister) {
    return (
      <Register
        onBackToLogin={() => {
          setShowRegister(false)
          setError('')
          setShowForgotPassword(false)
        }}
      />
    )
  }

  // =========================
  // LOGIN PAGE
  // =========================

  return (
    <div className="login-page">

      <div className="login-card">

        <h1>
          Film Lab Platform
        </h1>

        <form onSubmit={handleLogin}>

          {/* USERNAME */}

          <div className="form-group">

            <label>
              Username
            </label>

            <input
              type="text"
              value={username}
              onChange={(e) => {
                setUsername(e.target.value)
                setError('')
                setShowForgotPassword(false)
              }}
              placeholder="Enter username"
              required
            />

          </div>


          {/* PASSWORD */}

          <div className="form-group">

            <label>
              Password
            </label>

            <input
              type="password"
              value={password}
              onChange={(e) => {
                setPassword(e.target.value)
                setError('')
                setShowForgotPassword(false)
              }}
              placeholder="Enter password"
              required
            />

          </div>


          {/* ERROR */}

          {error && (
            <p className="error-message">
              {error}
            </p>
          )}


          {/* FORGOT PASSWORD */}

          {showForgotPassword && (
            <button
              type="button"
              className="forgot-password-button"
              onClick={() => {
                alert(
                  'Password reset feature will be available soon.'
                )
              }}
            >
              Forgot Password?
            </button>
          )}


          {/* LOGIN */}

          <button
            type="submit"
            className="login-button"
          >
            Login
          </button>

        </form>


        {/* REGISTER */}

        <div className="register-section">

          <p>
            Don't have an account?
          </p>

          <button
            className="register-button"
            onClick={() => {
              setShowRegister(true)
              setError('')
              setShowForgotPassword(false)
            }}
          >
            Create Account
          </button>

        </div>

      </div>

    </div>
  )
}

export default App