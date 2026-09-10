import { useEffect, useState } from 'react'
import './Dashboard.css'
import DeliveryManagement from './DeliveryManagement'
import FilmLabManagement from './FilmLabManagement'
import ServiceManagement from './ServiceManagement'
import OrderManagement from './OrderManagement'
import Community from './Community'

const API_URL = 'http://127.0.0.1:9999'

function Dashboard({ user, onLogout }) {
  const [sidebarOpen, setSidebarOpen] = useState(false)
  const [settingsOpen, setSettingsOpen] = useState(false)
  const [currentPage, setCurrentPage] = useState('home')

  const [labData, setLabData] = useState(null)

  const [photoMenuOpen, setPhotoMenuOpen] = useState(false)
  const [uploadingPhoto, setUploadingPhoto] = useState(false)
  const [photoError, setPhotoError] = useState('')

  const [profileImage, setProfileImage] = useState(null)
  const [coverImage, setCoverImage] = useState(null)

  // =========================
  // SUPPORT
  // =========================

  const [supportMenuOpen, setSupportMenuOpen] = useState(false)
  const [supportSubject, setSupportSubject] = useState('')
  const [supportMessage, setSupportMessage] = useState('')
  const [supportTickets, setSupportTickets] = useState([])
  const [supportLoading, setSupportLoading] = useState(false)
  const [supportSubmitting, setSupportSubmitting] = useState(false)
  const [supportError, setSupportError] = useState('')
  const [supportSuccess, setSupportSuccess] = useState('')

  // =========================
  // REVENUE
  // =========================

  const [payments, setPayments] = useState([])
  const [revenueLoading, setRevenueLoading] = useState(false)
  const [revenueError, setRevenueError] = useState('')

  // =========================
  // GET IMAGE URL
  // =========================

  const getImageUrl = (storagePath) => {
    if (!storagePath) {
      return null
    }

    if (
      storagePath.startsWith('http://') ||
      storagePath.startsWith('https://')
    ) {
      return storagePath
    }

    return `${API_URL}/film-labs/images/${storagePath}`
  }

  // =========================
  // LOAD FILM LAB
  // =========================

  const loadFilmLab = async () => {
    try {
      const token = localStorage.getItem('token')

      if (!token || !user?.id) {
        console.error(
          'User information is not available'
        )
        return
      }

      const response = await fetch(
        `${API_URL}/film-labs/`,
        {
          method: 'GET',
          headers: {
            Authorization: `Bearer ${token}`,
          },
        }
      )

      if (!response.ok) {
        console.error(
          'Failed to load film labs:',
          response.status
        )
        return
      }

      const data = await response.json()

      const labs = Array.isArray(data)
        ? data
        : data.film_labs ||
          data.data ||
          []

      const ownLab = labs.find(
        (lab) =>
          String(lab.owner_id) ===
          String(user.id)
      )

      if (!ownLab) {
        console.error(
          'Film lab not found for current user'
        )
        return
      }

      setLabData(ownLab)

      setProfileImage(
        ownLab.profile_image_path || null
      )

      setCoverImage(
        ownLab.cover_image_path || null
      )

    } catch (error) {
      console.error(
        'Failed to load film lab:',
        error
      )
    }
  }

  // =========================
  // LOAD PAYMENTS
  // =========================

  const loadPayments = async () => {
    try {
      const token = localStorage.getItem('token')

      if (!token) {
        return
      }

      setRevenueLoading(true)
      setRevenueError('')

      const response = await fetch(
        `${API_URL}/payments/`,
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
          'Failed to load payment data'
        )
      }

      const paymentList =
        Array.isArray(data)
          ? data
          : data.payments ||
            data.data ||
            []

      setPayments(paymentList)

    } catch (error) {
      console.error(
        'Failed to load payments:',
        error
      )

      setRevenueError(
        error.message ||
        'Failed to load revenue data'
      )

    } finally {
      setRevenueLoading(false)
    }
  }

  // =========================
  // LOAD SUPPORT
  // =========================

  const loadSupportTickets = async () => {
    try {
      const token = localStorage.getItem('token')

      if (!token) {
        return
      }

      setSupportLoading(true)
      setSupportError('')

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

      const tickets = Array.isArray(data)
        ? data
        : data.data || []

      setSupportTickets(tickets)

    } catch (error) {
      console.error(
        'Failed to load support tickets:',
        error
      )

      setSupportError(
        error.message ||
        'Failed to load support requests.'
      )

    } finally {
      setSupportLoading(false)
    }
  }

  // =========================
  // INITIAL LOAD
  // =========================

  useEffect(() => {
    if (user?.id) {
      loadFilmLab()
      loadPayments()
    }
  }, [user])

  // =========================
  // RELOAD REVENUE
  // =========================

  useEffect(() => {
    if (
      currentPage === 'revenueStatistics' &&
      user?.id
    ) {
      loadPayments()
    }
  }, [currentPage])

  // =========================
  // NAVIGATION
  // =========================

  const handleNavigation = (page) => {
    setCurrentPage(page)
    setSidebarOpen(false)
  }

  // =========================
  // OPEN SUPPORT
  // =========================

  const handleOpenSupport = () => {
    setSettingsOpen(false)

    setSupportSubject('')
    setSupportMessage('')
    setSupportError('')
    setSupportSuccess('')

    setSupportMenuOpen(true)

    loadSupportTickets()
  }

  // =========================
  // CLOSE SUPPORT
  // =========================

  const handleCloseSupport = () => {
    if (supportSubmitting) {
      return
    }

    setSupportMenuOpen(false)
    setSupportError('')
    setSupportSuccess('')
  }

  // =========================
  // SUBMIT SUPPORT
  // =========================

  const handleSubmitSupport = async () => {
    if (!supportSubject.trim()) {
      setSupportError(
        'Please enter a subject.'
      )
      return
    }

    if (!supportMessage.trim()) {
      setSupportError(
        'Please describe your problem.'
      )
      return
    }

    try {
      const token = localStorage.getItem('token')

      if (!token) {
        setSupportError(
          'Authentication token not found.'
        )
        return
      }

      setSupportSubmitting(true)
      setSupportError('')
      setSupportSuccess('')

      const response = await fetch(
        `${API_URL}/api/support`,
        {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            Authorization: `Bearer ${token}`,
          },
          body: JSON.stringify({
            subject:
              supportSubject.trim(),
            message:
              supportMessage.trim(),
          }),
        }
      )

      const data = await response.json()

      if (!response.ok) {
        throw new Error(
          data.message ||
          'Failed to submit support request.'
        )
      }

      setSupportTickets((previous) => [
        data,
        ...previous,
      ])

      setSupportSubject('')
      setSupportMessage('')

      setSupportSuccess(
        'Your support request has been submitted successfully.'
      )

    } catch (error) {
      console.error(
        'Failed to submit support request:',
        error
      )

      setSupportError(
        error.message ||
        'Failed to submit support request.'
      )

    } finally {
      setSupportSubmitting(false)
    }
  }

  // =========================
  // PROFILE IMAGE
  // =========================

  const handleProfileImageChange = async (
    event
  ) => {
    const file = event.target.files?.[0]

    event.target.value = ''

    if (!file) {
      return
    }

    if (!labData?.id) {
      setPhotoError(
        'Film lab information is not available.'
      )
      return
    }

    setUploadingPhoto(true)
    setPhotoError('')

    try {
      const token = localStorage.getItem('token')

      const formData = new FormData()
      formData.append('image', file)

      const response = await fetch(
        `${API_URL}/film-labs/${labData.id}/profile-image`,
        {
          method: 'PUT',
          headers: {
            Authorization: `Bearer ${token}`,
          },
          body: formData,
        }
      )

      const data = await response.json()

      if (!response.ok) {
        throw new Error(
          data.message ||
          'Failed to update profile image'
        )
      }

      setProfileImage(
        data.profile_image_path
      )

      setLabData((previousLab) => ({
        ...previousLab,
        profile_image_path:
          data.profile_image_path,
      }))

      setPhotoMenuOpen(false)

    } catch (error) {
      console.error(
        'Failed to update profile image:',
        error
      )

      setPhotoError(
        error.message ||
        'Failed to update profile image'
      )

    } finally {
      setUploadingPhoto(false)
    }
  }

  // =========================
  // COVER IMAGE
  // =========================

  const handleCoverImageChange = async (
    event
  ) => {
    const file = event.target.files?.[0]

    event.target.value = ''

    if (!file) {
      return
    }

    if (!labData?.id) {
      setPhotoError(
        'Film lab information is not available.'
      )
      return
    }

    setUploadingPhoto(true)
    setPhotoError('')

    try {
      const token = localStorage.getItem('token')

      const formData = new FormData()
      formData.append('image', file)

      const response = await fetch(
        `${API_URL}/film-labs/${labData.id}/cover-image`,
        {
          method: 'PUT',
          headers: {
            Authorization: `Bearer ${token}`,
          },
          body: formData,
        }
      )

      const data = await response.json()

      if (!response.ok) {
        throw new Error(
          data.message ||
          'Failed to update cover image'
        )
      }

      setCoverImage(
        data.cover_image_path
      )

      setLabData((previousLab) => ({
        ...previousLab,
        cover_image_path:
          data.cover_image_path,
      }))

      setPhotoMenuOpen(false)

    } catch (error) {
      console.error(
        'Failed to update cover image:',
        error
      )

      setPhotoError(
        error.message ||
        'Failed to update cover image'
      )

    } finally {
      setUploadingPhoto(false)
    }
  }

  // =========================
  // REVENUE HELPERS
  // =========================

  const getCompletedPayments = () => {
    return payments.filter(
      (payment) =>
        String(payment.status || '').toLowerCase() ===
        'completed' &&
        payment.paid_at
    )
  }

  const getPaymentAmount = (payment) => {
    const amount = Number(
      payment.amount || 0
    )

    return Number.isFinite(amount)
      ? amount
      : 0
  }

  const formatCurrency = (amount) => {
    return new Intl.NumberFormat(
      'vi-VN',
      {
        style: 'currency',
        currency: 'VND',
        maximumFractionDigits: 0,
      }
    ).format(amount)
  }

  const formatMonthLabel = (
    year,
    month
  ) => {
    return `${String(month).padStart(2, '0')}/${year}`
  }

  // =========================
  // REVENUE PAGE
  // =========================

  const renderRevenueStatistics = () => {
    const completedPayments =
      getCompletedPayments()

    const totalRevenue =
      completedPayments.reduce(
        (total, payment) =>
          total +
          getPaymentAmount(payment),
        0
      )

    const now = new Date()

    const currentYear =
      now.getFullYear()

    const currentMonth =
      now.getMonth()

    const thisMonthRevenue =
      completedPayments
        .filter((payment) => {
          const paidDate =
            new Date(payment.paid_at)

          return (
            paidDate.getFullYear() ===
              currentYear &&
            paidDate.getMonth() ===
              currentMonth
          )
        })
        .reduce(
          (total, payment) =>
            total +
            getPaymentAmount(payment),
          0
        )

    const monthlyMap = {}

    completedPayments.forEach(
      (payment) => {
        const paidDate =
          new Date(payment.paid_at)

        if (
          Number.isNaN(
            paidDate.getTime()
          )
        ) {
          return
        }

        const year =
          paidDate.getFullYear()

        const month =
          paidDate.getMonth() + 1

        const key =
          `${year}-${String(month).padStart(2, '0')}`

        if (!monthlyMap[key]) {
          monthlyMap[key] = {
            year,
            month,
            revenue: 0,
          }
        }

        monthlyMap[key].revenue +=
          getPaymentAmount(payment)
      }
    )

    const monthlyRevenue =
      Object.values(monthlyMap)
        .sort((a, b) => {
          if (a.year !== b.year) {
            return b.year - a.year
          }

          return b.month - a.month
        })

    const maxRevenue =
      monthlyRevenue.length > 0
        ? Math.max(
            ...monthlyRevenue.map(
              (item) =>
                item.revenue
            )
          )
        : 0

    return (
      <div className="revenue-page">

        <div className="revenue-header">

          <div>
            <h1>
              Revenue Statistics
            </h1>

            <p>
              Track your film lab revenue
              from successful payments.
            </p>
          </div>

          <button
            className="revenue-refresh-button"
            onClick={loadPayments}
            disabled={revenueLoading}
          >
            {revenueLoading
              ? 'Loading...'
              : '↻ Refresh'}
          </button>

        </div>

        {revenueError && (
          <div className="revenue-error">
            {revenueError}
          </div>
        )}

        <div className="revenue-summary">

          <div className="revenue-card">

            <div className="revenue-card-icon">
              💰
            </div>

            <div>
              <span className="revenue-card-label">
                Total Revenue
              </span>

              <strong className="revenue-card-value">
                {formatCurrency(
                  totalRevenue
                )}
              </strong>
            </div>

          </div>

          <div className="revenue-card">

            <div className="revenue-card-icon">
              📅
            </div>

            <div>
              <span className="revenue-card-label">
                This Month
              </span>

              <strong className="revenue-card-value">
                {formatCurrency(
                  thisMonthRevenue
                )}
              </strong>
            </div>

          </div>

          <div className="revenue-card">

            <div className="revenue-card-icon">
              💳
            </div>

            <div>
              <span className="revenue-card-label">
                Successful Payments
              </span>

              <strong className="revenue-card-value">
                {completedPayments.length}
              </strong>
            </div>

          </div>

        </div>

        <div className="revenue-section">

          <div className="revenue-section-header">

            <div>
              <h2>
                Monthly Revenue
              </h2>

              <p>
                Revenue based on payment
                completion date.
              </p>
            </div>

          </div>

          {revenueLoading ? (

            <div className="revenue-empty">
              Loading revenue data...
            </div>

          ) : monthlyRevenue.length === 0 ? (

            <div className="revenue-empty">
              No successful payments yet.
            </div>

          ) : (

            <div className="monthly-revenue-list">

              {monthlyRevenue.map(
                (item) => {

                  const percentage =
                    maxRevenue > 0
                      ? (
                          item.revenue /
                          maxRevenue
                        ) * 100
                      : 0

                  return (
                    <div
                      className="monthly-revenue-row"
                      key={`${item.year}-${item.month}`}
                    >

                      <div className="monthly-revenue-info">

                        <span className="monthly-revenue-month">
                          {formatMonthLabel(
                            item.year,
                            item.month
                          )}
                        </span>

                        <strong>
                          {formatCurrency(
                            item.revenue
                          )}
                        </strong>

                      </div>

                      <div className="monthly-revenue-bar-wrapper">

                        <div
                          className="monthly-revenue-bar"
                          style={{
                            width:
                              `${percentage}%`,
                          }}
                        />

                      </div>

                    </div>
                  )
                }
              )}

            </div>

          )}

        </div>

        <div className="revenue-section">

          <div className="revenue-section-header">

            <div>
              <h2>
                Successful Payments
              </h2>

              <p>
                Payments included in revenue.
              </p>
            </div>

          </div>

          {completedPayments.length === 0 ? (

            <div className="revenue-empty">
              No completed payments.
            </div>

          ) : (

            <div className="revenue-payment-table-wrapper">

              <table className="revenue-payment-table">

                <thead>
                  <tr>
                    <th>
                      Payment
                    </th>

                    <th>
                      Paid At
                    </th>

                    <th>
                      Method
                    </th>

                    <th>
                      Amount
                    </th>
                  </tr>
                </thead>

                <tbody>

                  {completedPayments
                    .slice()
                    .sort(
                      (a, b) =>
                        new Date(
                          b.paid_at
                        ) -
                        new Date(
                          a.paid_at
                        )
                    )
                    .map(
                      (payment) => (

                        <tr
                          key={
                            payment.id
                          }
                        >

                          <td>
                            <strong>
                              {payment.id
                                ? String(
                                    payment.id
                                  ).slice(
                                    0,
                                    8
                                  )
                                : 'Payment'}
                            </strong>
                          </td>

                          <td>
                            {payment.paid_at
                              ? new Date(
                                  payment.paid_at
                                ).toLocaleString(
                                  'vi-VN'
                                )
                              : '-'}
                          </td>

                          <td>
                            {payment.payment_method ||
                              payment.method ||
                              'Demo'}
                          </td>

                          <td>
                            <strong>
                              {formatCurrency(
                                getPaymentAmount(
                                  payment
                                )
                              )}
                            </strong>
                          </td>

                        </tr>

                      )
                    )}

                </tbody>

              </table>

            </div>

          )}

        </div>

      </div>
    )
  }

  // =========================
  // HOME
  // =========================

  const renderHome = () => {
    const profileImageUrl =
      getImageUrl(profileImage)

    const coverImageUrl =
      getImageUrl(coverImage)

    return (
      <div className="home-page">

        <div className="profile-section">

          <div
            className="profile-cover"
            style={
              coverImageUrl
                ? {
                    backgroundImage:
                      `url("${coverImageUrl}")`,
                  }
                : {}
            }
          />

          <div className="profile-info">

            <div className="profile-avatar-wrapper">

              <div
                className="profile-avatar"
                style={
                  profileImageUrl
                    ? {
                        backgroundImage:
                          `url("${profileImageUrl}")`,
                      }
                    : {}
                }
              >
                {!profileImageUrl && '📷'}
              </div>

            </div>

            <div className="profile-details">

              <h1>
                {labData?.name ||
                  'Film Lab'}
              </h1>

              <p className="profile-type">
                Film Lab
              </p>

              <p className="profile-description">
                {labData?.description ||
                  'Film photography lab and processing services.'}
              </p>

              <div className="profile-contact">

                {labData?.phone && (
                  <span>
                    📞 {labData.phone}
                  </span>
                )}

                {(labData?.address ||
                  labData?.district ||
                  labData?.city) && (
                  <span>
                    📍{' '}
                    {[
                      labData?.address,
                      labData?.district,
                      labData?.city,
                    ]
                      .filter(Boolean)
                      .join(', ')}
                  </span>
                )}

              </div>

            </div>

            <div className="profile-actions">

              <button
                className="edit-profile-button"
                disabled={
                  !labData ||
                  uploadingPhoto
                }
                onClick={() => {
                  setPhotoError('')
                  setPhotoMenuOpen(true)
                }}
              >
                📷 Change Photo
              </button>

            </div>

          </div>

        </div>

      </div>
    )
  }

  // =========================
  // CURRENT PAGE
  // =========================

  const renderCurrentPage = () => {
    switch (currentPage) {

      case 'filmLabManagement':
        return <FilmLabManagement />

      case 'serviceManagement':
        return <ServiceManagement />

      case 'orderManagement':
        return <OrderManagement />

      case 'revenueStatistics':
        return renderRevenueStatistics()

      case 'delivery':
        return <DeliveryManagement />

      case 'community':
        return <Community />

      default:
        return renderHome()
    }
  }

  return (
    <div className="dashboard">

      {/* =========================
          HEADER
      ========================= */}

      <header className="dashboard-header">

        <button
          className="menu-button"
          onClick={() =>
            setSidebarOpen(
              !sidebarOpen
            )
          }
        >
          ☰
        </button>

        <div className="header-title">
          Film Lab Platform
        </div>

        <button
          className="settings-button"
          onClick={() =>
            setSettingsOpen(
              !settingsOpen
            )
          }
        >
          ⚙
        </button>

        {settingsOpen && (

          <div className="settings-menu">

            <button>
              Account Information
            </button>

            <button>
              Change Password
            </button>

            <button
              onClick={handleOpenSupport}
            >
              Report a Problem
            </button>

            <div className="settings-divider" />

            <button
              className="logout-menu-button"
              onClick={onLogout}
            >
              Logout
            </button>

          </div>

        )}

      </header>

      {/* =========================
          SIDEBAR
      ========================= */}

      {sidebarOpen && (

        <aside className="sidebar">

          <button
            className={
              currentPage === 'home'
                ? 'sidebar-item active'
                : 'sidebar-item'
            }
            onClick={() =>
              handleNavigation('home')
            }
          >
            🏠 Home
          </button>

          <button
            className={
              currentPage ===
              'filmLabManagement'
                ? 'sidebar-item active'
                : 'sidebar-item'
            }
            onClick={() =>
              handleNavigation(
                'filmLabManagement'
              )
            }
          >
            🏪 Film Lab Management
          </button>

          <button
            className={
              currentPage ===
              'serviceManagement'
                ? 'sidebar-item active'
                : 'sidebar-item'
            }
            onClick={() =>
              handleNavigation(
                'serviceManagement'
              )
            }
          >
            🛠 Service Management
          </button>

          <button
            className={
              currentPage ===
              'orderManagement'
                ? 'sidebar-item active'
                : 'sidebar-item'
            }
            onClick={() =>
              handleNavigation(
                'orderManagement'
              )
            }
          >
            📦 Order Management
          </button>

          <button
            className={
              currentPage ===
              'revenueStatistics'
                ? 'sidebar-item active'
                : 'sidebar-item'
            }
            onClick={() =>
              handleNavigation(
                'revenueStatistics'
              )
            }
          >
            💰 Revenue Statistics
          </button>

          <button
            className={
              currentPage === 'delivery'
                ? 'sidebar-item active'
                : 'sidebar-item'
            }
            onClick={() =>
              handleNavigation(
                'delivery'
              )
            }
          >
            🚚 Delivery
          </button>

          <button
            className={
              currentPage === 'community'
                ? 'sidebar-item active'
                : 'sidebar-item'
            }
            onClick={() =>
              handleNavigation(
                'community'
              )
            }
          >
            👥 Community
          </button>

        </aside>

      )}

      {/* =========================
          MAIN
      ========================= */}

      <main className="dashboard-content">
        {renderCurrentPage()}
      </main>

      {/* =========================
          CHANGE PHOTO MODAL
      ========================= */}

      {photoMenuOpen && (

        <div
          className="photo-modal-overlay"
          onClick={() => {
            if (!uploadingPhoto) {
              setPhotoMenuOpen(false)
            }
          }}
        >

          <div
            className="photo-modal"
            onClick={(event) =>
              event.stopPropagation()
            }
          >

            <h2>
              Change Photo
            </h2>

            <p>
              Choose which photo you want
              to change.
            </p>

            {photoError && (

              <div className="photo-error">
                {photoError}
              </div>

            )}

            <label className="photo-option">

              🖼️ Change Profile Picture

              <input
                type="file"
                accept="image/jpeg,image/png,image/webp"
                disabled={uploadingPhoto}
                onChange={
                  handleProfileImageChange
                }
              />

            </label>

            <label className="photo-option">

              🌄 Change Cover Photo

              <input
                type="file"
                accept="image/jpeg,image/png,image/webp"
                disabled={uploadingPhoto}
                onChange={
                  handleCoverImageChange
                }
              />

            </label>

            {uploadingPhoto && (

              <p className="uploading-text">
                Uploading image...
              </p>

            )}

            <button
              className="photo-cancel-button"
              disabled={uploadingPhoto}
              onClick={() =>
                setPhotoMenuOpen(false)
              }
            >
              Cancel
            </button>

          </div>

        </div>

      )}

      {/* =========================
          SUPPORT MODAL
      ========================= */}

      {supportMenuOpen && (

        <div
          className="support-modal-overlay"
          onClick={handleCloseSupport}
        >

          <div
            className="support-modal"
            onClick={(event) =>
              event.stopPropagation()
            }
          >

            <div className="support-modal-header">

              <div>
                <h2>
                  Report a Problem
                </h2>

                <p>
                  Send a support request to the
                  Film Lab Platform administrator.
                </p>
              </div>

              <button
                className="support-close-button"
                onClick={handleCloseSupport}
                disabled={supportSubmitting}
              >
                ×
              </button>

            </div>

            {supportError && (
              <div className="support-error">
                {supportError}
              </div>
            )}

            {supportSuccess && (
              <div className="support-success">
                {supportSuccess}
              </div>
            )}

            <div className="support-form">

              <label>
                Subject
              </label>

              <input
                type="text"
                value={supportSubject}
                onChange={(event) => {
                  setSupportSubject(
                    event.target.value
                  )
                  setSupportError('')
                  setSupportSuccess('')
                }}
                placeholder="Enter the problem subject"
                disabled={supportSubmitting}
              />

              <label>
                Message
              </label>

              <textarea
                value={supportMessage}
                onChange={(event) => {
                  setSupportMessage(
                    event.target.value
                  )
                  setSupportError('')
                  setSupportSuccess('')
                }}
                placeholder="Describe your problem..."
                disabled={supportSubmitting}
              />

            </div>

            {/* =========================
                PREVIOUS REQUESTS
                ========================= */}

            <div className="support-history">

              <div className="support-history-header">

                <h3>
                  My Support Requests
                </h3>

                <button
                  className="support-refresh-button"
                  onClick={loadSupportTickets}
                  disabled={supportLoading}
                >
                  {supportLoading
                    ? 'Loading...'
                    : '↻ Refresh'}
                </button>

              </div>

              {supportLoading ? (

                <div className="support-empty">
                  Loading requests...
                </div>

              ) : supportTickets.length === 0 ? (

                <div className="support-empty">
                  No support requests yet.
                </div>

              ) : (

                <div className="support-ticket-list">

                  {supportTickets.map(
                    (ticket) => (

                      <div
                        className="support-ticket"
                        key={ticket.id}
                      >

                        <div className="support-ticket-top">

                          <strong>
                            {ticket.subject}
                          </strong>

                          <span
                            className={`support-status support-status-${String(
                              ticket.status || ''
                            ).toLowerCase()}`}
                          >
                            {ticket.status
                              ? String(
                                  ticket.status
                                ).charAt(0).toUpperCase() +
                                String(
                                  ticket.status
                                ).slice(1)
                              : '-'}
                          </span>

                        </div>

                        <p>
                          {ticket.message}
                        </p>

                        {ticket.reply && (

                          <div className="support-reply">

                            <strong>
                              Admin Reply
                            </strong>

                            <span>
                              {ticket.reply}
                            </span>

                          </div>

                        )}

                        <small>
                          {ticket.created_at
                            ? new Date(
                                ticket.created_at
                              ).toLocaleString(
                                'vi-VN'
                              )
                            : '-'}
                        </small>

                      </div>

                    )
                  )}

                </div>

              )}

            </div>

            {/* =========================
                FOOTER
                ========================= */}

            <div className="support-modal-footer">

              <button
                className="support-cancel-button"
                onClick={handleCloseSupport}
                disabled={supportSubmitting}
              >
                Cancel
              </button>

              <button
                className="support-submit-button"
                onClick={
                  handleSubmitSupport
                }
                disabled={supportSubmitting}
              >
                {supportSubmitting
                  ? 'Sending...'
                  : 'Send Report'}
              </button>

            </div>

          </div>

        </div>

      )}

    </div>
  )
}

export default Dashboard