import './Dashboard_Admin.css'

function Dashboard_Admin({ user, onLogout }) {
  return (
    <div className="admin-dashboard">
      <button
        className="admin-logout-button"
        onClick={onLogout}
      >
        Logout
      </button>
    </div>
  )
}

export default Dashboard_Admin