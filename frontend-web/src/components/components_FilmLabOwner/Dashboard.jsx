import { useState } from 'react'
import './Dashboard.css'
import FilmLabManagement from './FilmLabManagement'
import ServiceManagement from './ServiceManagement'

function Dashboard({ user, onLogout }) {
  const [menuOpen, setMenuOpen] = useState(false)
  const [settingsOpen, setSettingsOpen] = useState(false)
  const [currentPage, setCurrentPage] = useState('dashboard')

  const handlePageChange = (page) => {
    setCurrentPage(page)
    setMenuOpen(false)
    setSettingsOpen(false)
  }

  return (
    <div className="dashboard">

      {/* =========================
          HEADER
      ========================= */}

      <header className="dashboard-header">

        {/* LEFT MENU */}

        <button
          className="menu-button"
          onClick={() => {
            setMenuOpen(!menuOpen)
            setSettingsOpen(false)
          }}
        >
          ☰
        </button>

        {/* TITLE */}

        <div className="header-title">
          Film Lab Platform
        </div>

        {/* RIGHT SETTINGS */}

        <button
          className="settings-button"
          onClick={() => {
            setSettingsOpen(!settingsOpen)
            setMenuOpen(false)
          }}
        >
          ⚙
        </button>

      </header>


      {/* =========================
          SIDE MENU
      ========================= */}

      {menuOpen && (
        <aside className="side-menu">

          <div className="side-menu-title">
            Film Lab Owner
          </div>

          <button
            onClick={() => handlePageChange('dashboard')}
          >
            🏠 Dashboard
          </button>

          <button
            onClick={() => handlePageChange('filmLabManagement')}
          >
            🏪 Film Lab Management
          </button>

          <button
            onClick={() => handlePageChange('serviceManagement')}
          >
            🛠 Service Management
          </button>

          <button>
            📦 Order Management
          </button>

          <button>
            🔄 Processing Workflow
          </button>

          <button>
            💳 Payment
          </button>

          <button>
            🚚 Delivery
          </button>

          <button>
            📊 Reports
          </button>

        </aside>
      )}


      {/* =========================
          SETTINGS MENU
      ========================= */}

      {settingsOpen && (
        <div className="settings-menu">

          <div className="settings-title">
            ⚙ Settings
          </div>

          <button>
            Account Information
          </button>

          <button>
            Change Password
          </button>

          <button>
            Report a Problem
          </button>

          <button onClick={onLogout}>
            Logout
          </button>

        </div>
      )}


      {/* =========================
          PAGE CONTENT
      ========================= */}

      {currentPage === 'filmLabManagement' ? (

        <FilmLabManagement />

      ) : currentPage === 'serviceManagement' ? (

        <ServiceManagement />

      ) : (

        <main className="dashboard-content">

          {/* =========================
              HERO
          ========================= */}

          <section className="hero-section">

            <p className="hero-small-title">
              WELCOME TO
            </p>

            <h1>
              Film Lab Platform
            </h1>

            <p className="hero-description">
              Connecting film photography enthusiasts
              with film processing labs.
            </p>

            <div className="hero-image-placeholder">
              <span>Film Photography</span>
            </div>

          </section>


          {/* =========================
              ABOUT
          ========================= */}

          <section className="information-section">

            <h2>
              Discover Film Lab Services
            </h2>

            <p>
              Explore film processing services, compare
              available options, and manage your film lab
              operations in one platform.
            </p>

            <div className="info-cards">

              <div className="info-card">

                <h3>
                  Discover
                </h3>

                <p>
                  Find film processing services and
                  information about film labs.
                </p>

              </div>

              <div className="info-card">

                <h3>
                  Manage
                </h3>

                <p>
                  Manage your film lab, services,
                  orders, and processing workflow.
                </p>

              </div>

              <div className="info-card">

                <h3>
                  Connect
                </h3>

                <p>
                  Connect photographers with film
                  processing labs.
                </p>

              </div>

            </div>

          </section>


          {/* =========================
              HOW IT WORKS
          ========================= */}

          <section className="information-section">

            <h2>
              How It Works
            </h2>

            <div className="steps">

              <div className="step">

                <div className="step-number">
                  1
                </div>

                <h3>
                  Choose a Lab
                </h3>

                <p>
                  Explore available film labs and
                  their services.
                </p>

              </div>


              <div className="step">

                <div className="step-number">
                  2
                </div>

                <h3>
                  Book a Service
                </h3>

                <p>
                  Select a suitable processing service
                  for your film.
                </p>

              </div>


              <div className="step">

                <div className="step-number">
                  3
                </div>

                <h3>
                  Process Your Film
                </h3>

                <p>
                  Track the processing workflow and
                  receive your processed film.
                </p>

              </div>

            </div>

          </section>


          {/* =========================
              PLATFORM
          ========================= */}

          <section className="information-section platform-section">

            <h2>
              Film Photography in One Platform
            </h2>

            <p>
              Film Lab Platform brings film photographers
              and film processing labs together in one
              centralized platform.
            </p>

            <p>
              Manage your lab information, services,
              orders, processing workflow, payment,
              and delivery from one place.
            </p>

          </section>


          {/* =========================
              FOOTER
          ========================= */}

          <footer className="dashboard-footer">

            <h3>
              Film Lab Platform
            </h3>

            <p>
              Connecting film photography enthusiasts
              with film processing labs.
            </p>

            <p>
              © 2026 Film Lab Platform
            </p>

          </footer>

        </main>

      )}

    </div>
  )
}

export default Dashboard