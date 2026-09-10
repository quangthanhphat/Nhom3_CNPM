import { useEffect, useState } from 'react'
import './Dashboard_Admin.css'

const API_URL = 'http://127.0.0.1:9999'

function Dashboard_Admin({ user, onLogout }) {
  const [sidebarOpen, setSidebarOpen] = useState(false)

  const [supportTickets, setSupportTickets] = useState([])
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')

  const [selectedTicket, setSelectedTicket] = useState(null)
  const [replyText, setReplyText] = useState('')
  const [replying, setReplying] = useState(false)

  // =========================================================
  // LOAD SUPPORT
  // =========================================================

  const loadSupportTickets = async () => {
    try {
      const token = localStorage.getItem('token')

      if (!token) {
        setError('Authentication token not found.')
        return
      }

      setLoading(true)
      setError('')

      const response = await fetch(
        `${API_URL}/api/support`,
        {
          method: 'GET',
          headers: {
            Authorization: `Bearer ${token}`,
          },
        }
      )

      const data = await response.json()

      if (!response.ok) {
        throw new Error(
          data.message ||
          'Failed to load support requests.'
        )
      }

      setSupportTickets(
        Array.isArray(data)
          ? data
          : data.data || []
      )

    } catch (err) {
      console.error(
        'Failed to load support tickets:',
        err
      )

      setError(
        err.message ||
        'Failed to load support requests.'
      )

    } finally {
      setLoading(false)
    }
  }

  // =========================================================
  // INITIAL LOAD
  // =========================================================

  useEffect(() => {
    loadSupportTickets()
  }, [])

  // =========================================================
  // OPEN TICKET
  // =========================================================

  const openTicket = (ticket) => {
    setSelectedTicket(ticket)
    setReplyText(ticket.reply || '')
    setError('')
  }

  // =========================================================
  // CLOSE DETAIL
  // =========================================================

  const closeTicket = () => {
    setSelectedTicket(null)
    setReplyText('')
  }

  // =========================================================
  // REPLY
  // =========================================================

  const handleReply = async () => {
    if (!selectedTicket) {
      return
    }

    if (!replyText.trim()) {
      return
    }

    try {
      const token = localStorage.getItem('token')

      if (!token) {
        throw new Error(
          'Authentication token not found.'
        )
      }

      setReplying(true)
      setError('')

      const response = await fetch(
        `${API_URL}/api/support/${selectedTicket.id}/reply`,
        {
          method: 'PUT',
          headers: {
            'Content-Type': 'application/json',
            Authorization: `Bearer ${token}`,
          },
          body: JSON.stringify({
            reply: replyText.trim(),
          }),
        }
      )

      const data = await response.json()

      if (!response.ok) {
        throw new Error(
          data.message ||
          'Failed to send reply.'
        )
      }

      setSelectedTicket(data)

      setSupportTickets((previous) =>
        previous.map((ticket) =>
          String(ticket.id) ===
          String(data.id)
            ? data
            : ticket
        )
      )

    } catch (err) {
      console.error(
        'Failed to reply support ticket:',
        err
      )

      setError(
        err.message ||
        'Failed to send reply.'
      )

    } finally {
      setReplying(false)
    }
  }

  // =========================================================
  // CLOSE SUPPORT TICKET
  // =========================================================

  const handleCloseTicket = async () => {
    if (!selectedTicket) {
      return
    }

    try {
      const token = localStorage.getItem('token')

      if (!token) {
        throw new Error(
          'Authentication token not found.'
        )
      }

      const response = await fetch(
        `${API_URL}/api/support/${selectedTicket.id}/close`,
        {
          method: 'PUT',
          headers: {
            Authorization: `Bearer ${token}`,
          },
        }
      )

      const data = await response.json()

      if (!response.ok) {
        throw new Error(
          data.message ||
          'Failed to close support ticket.'
        )
      }

      setSelectedTicket(data)

      setSupportTickets((previous) =>
        previous.map((ticket) =>
          String(ticket.id) ===
          String(data.id)
            ? data
            : ticket
        )
      )

    } catch (err) {
      console.error(
        'Failed to close support ticket:',
        err
      )

      setError(
        err.message ||
        'Failed to close support ticket.'
      )
    }
  }

  // =========================================================
  // STATUS
  // =========================================================

  const getStatusClass = (status) => {
    switch (
      String(status || '').toLowerCase()
    ) {
      case 'open':
        return 'status-open'

      case 'answered':
        return 'status-answered'

      case 'closed':
        return 'status-closed'

      default:
        return ''
    }
  }

  const formatStatus = (status) => {
    if (!status) {
      return '-'
    }

    return (
      String(status).charAt(0).toUpperCase() +
      String(status).slice(1)
    )
  }

  const formatDate = (date) => {
    if (!date) {
      return '-'
    }

    const parsedDate = new Date(date)

    if (
      Number.isNaN(
        parsedDate.getTime()
      )
    ) {
      return '-'
    }

    return parsedDate.toLocaleString(
      'vi-VN'
    )
  }

  // =========================================================
  // SUPPORT PAGE
  // =========================================================

  const renderSupport = () => {
    return (
      <div className="admin-support-page">

        <div className="admin-page-header">

          <div>
            <h1>
              Support
            </h1>

            <p>
              Manage support requests from
              film lab owners.
            </p>
          </div>

          <button
            className="admin-refresh-button"
            onClick={loadSupportTickets}
            disabled={loading}
          >
            {loading
              ? 'Loading...'
              : '↻ Refresh'}
          </button>

        </div>

        {error && (
          <div className="admin-error">
            {error}
          </div>
        )}

        <div className="admin-support-card">

          {loading ? (

            <div className="admin-empty">
              Loading support requests...
            </div>

          ) : supportTickets.length === 0 ? (

            <div className="admin-empty">
              No support requests yet.
            </div>

          ) : (

            <div className="admin-support-list">

              {supportTickets.map(
                (ticket) => (

                  <div
                    className="admin-support-item"
                    key={ticket.id}
                    onClick={() =>
                      openTicket(ticket)
                    }
                  >

                    <div className="admin-support-main">

                      <h3>
                        {ticket.subject}
                      </h3>

                      <p>
                        {ticket.message}
                      </p>

                      <span>
                        Created:{' '}
                        {formatDate(
                          ticket.created_at
                        )}
                      </span>

                    </div>

                    <div className="admin-support-side">

                      <span
                        className={`admin-status ${getStatusClass(
                          ticket.status
                        )}`}
                      >
                        {formatStatus(
                          ticket.status
                        )}
                      </span>

                      <button
                        className="admin-view-button"
                        onClick={(event) => {
                          event.stopPropagation()
                          openTicket(ticket)
                        }}
                      >
                        View
                      </button>

                    </div>

                  </div>

                )
              )}

            </div>

          )}

        </div>

      </div>
    )
  }

  // =========================================================
  // MAIN
  // =========================================================

  return (
    <div className="admin-dashboard">

      {/* =====================================================
          HEADER
      ===================================================== */}

      <header className="admin-header">

        <button
          className="admin-menu-button"
          onClick={() =>
            setSidebarOpen(
              !sidebarOpen
            )
          }
        >
          ☰
        </button>

        <div className="admin-header-title">
          Film Lab Platform
        </div>

        <div className="admin-header-user">
          Admin
        </div>

      </header>

      {/* =====================================================
          SIDEBAR
      ===================================================== */}

      {sidebarOpen && (

        <aside className="admin-sidebar">

          <button
            className="admin-sidebar-item active"
            onClick={() => {
              setSidebarOpen(false)
              loadSupportTickets()
            }}
          >
            🛟 Support
          </button>

          <div className="admin-sidebar-divider" />

          <button
            className="admin-sidebar-logout"
            onClick={onLogout}
          >
            🚪 Logout
          </button>

        </aside>

      )}

      {/* =====================================================
          CONTENT
      ===================================================== */}

      <main className="admin-content">

        {renderSupport()}

      </main>

      {/* =====================================================
          SUPPORT DETAIL
      ===================================================== */}

      {selectedTicket && (

        <div
          className="admin-modal-overlay"
          onClick={closeTicket}
        >

          <div
            className="admin-modal"
            onClick={(event) =>
              event.stopPropagation()
            }
          >

            <div className="admin-modal-header">

              <div>

                <h2>
                  {selectedTicket.subject}
                </h2>

                <span
                  className={`admin-status ${getStatusClass(
                    selectedTicket.status
                  )}`}
                >
                  {formatStatus(
                    selectedTicket.status
                  )}
                </span>

              </div>

              <button
                className="admin-modal-close"
                onClick={closeTicket}
              >
                ×
              </button>

            </div>

            <div className="admin-modal-body">

              <div className="admin-ticket-info">

                <div>
                  <strong>
                    User ID
                  </strong>

                  <span>
                    {selectedTicket.user_id}
                  </span>
                </div>

                <div>
                  <strong>
                    Created
                  </strong>

                  <span>
                    {formatDate(
                      selectedTicket.created_at
                    )}
                  </span>
                </div>

              </div>

              <div className="admin-message-section">

                <h3>
                  Problem
                </h3>

                <div className="admin-message-box">
                  {selectedTicket.message}
                </div>

              </div>

              <div className="admin-reply-section">

                <h3>
                  Reply
                </h3>

                <textarea
                  value={replyText}
                  onChange={(event) =>
                    setReplyText(
                      event.target.value
                    )
                  }
                  placeholder="Write your reply..."
                  disabled={
                    replying ||
                    selectedTicket.status ===
                      'closed'
                  }
                />

              </div>

              {selectedTicket.reply && (
                <div className="admin-existing-reply">

                  <h3>
                    Current Reply
                  </h3>

                  <div className="admin-message-box">
                    {selectedTicket.reply}
                  </div>

                </div>
              )}

            </div>

            <div className="admin-modal-footer">

              <button
                className="admin-cancel-button"
                onClick={closeTicket}
              >
                Cancel
              </button>

              {selectedTicket.status !==
                'closed' && (

                <>
                  <button
                    className="admin-close-ticket-button"
                    onClick={
                      handleCloseTicket
                    }
                    disabled={replying}
                  >
                    Close Ticket
                  </button>

                  <button
                    className="admin-reply-button"
                    onClick={handleReply}
                    disabled={
                      replying ||
                      !replyText.trim()
                    }
                  >
                    {replying
                      ? 'Sending...'
                      : 'Send Reply'}
                  </button>
                </>

              )}

            </div>

          </div>

        </div>

      )}

    </div>
  )
}

export default Dashboard_Admin