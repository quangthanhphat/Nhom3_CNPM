import './App.css'

function Register({ onBack }) {
  return (
    <div className="login-page">
      <div className="login-card">

        <h1>Create Account</h1>

        <form>
          <div className="form-group">
            <input
              type="text"
              placeholder="Enter your username"
            />
          </div>

          <div className="form-group">
            <input
              type="email"
              placeholder="Enter your email"
            />
          </div>

          <div className="form-group">
            <input
              type="password"
              placeholder="Enter your password"
            />
          </div>

          <div className="form-group">
            <input
              type="password"
              placeholder="Confirm your password"
            />
          </div>

          <button type="submit">REGISTER</button>
        </form>

        <p className="register-text">
          Already have an account?{' '}
          <span onClick={onBack}>Login</span>
        </p>

      </div>
    </div>
  )
}

export default Register