import { useState } from 'react'
import './App.css'
import Register from './Register'

function App() {
  const [showRegister, setShowRegister] = useState(false)

  if (showRegister) {
    return <Register onBack={() => setShowRegister(false)} />
  }

  return (
    <div className="login-page">
      <div className="login-card">

        <h1>Welcome Film Photography Platform</h1>

        <form>
          <div className="form-group">
            <input
              type="text"
              placeholder="Enter your username"
            />
          </div>

          <div className="form-group">
            <input
              type="password"
              placeholder="Enter your password"
            />
          </div>

          <button type="submit">LOGIN</button>
        </form>

        <p className="register-text">
          Don't have an account?{' '}
          <span onClick={() => setShowRegister(true)}>
            Register
          </span>
        </p>

      </div>
    </div>
  )
}

export default App