import { useEffect, useState, useRef } from 'react'
import './OrderManagement.css'

function OrderManagement() {
  const [orders, setOrders] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')
  const [selectedOrder, setSelectedOrder] = useState(null)
  const [statusFilter, setStatusFilter] = useState('all')
  const [updatingStatus, setUpdatingStatus] = useState(false)
  const [statusMessage, setStatusMessage] = useState('')
  const [resultFiles, setResultFiles] = useState([])
  const [uploadingResult, setUploadingResult] = useState(false)
  const [resultMessage, setResultMessage] = useState('')
  const [resultError, setResultError] = useState('')
  const resultInputRef = useRef(null)

  const getToken = () => {
    return localStorage.getItem('token')
  }

  const getUser = () => {
    const savedUser = localStorage.getItem('user')

    if (!savedUser) {
      return null
    }

    try {
      return JSON.parse(savedUser)
    } catch {
      return null
    }
  }

  const loadOrders = async () => {
    setLoading(true)
    setError('')

    try {
      const token = getToken()
      const user = getUser()

      if (!token || !user) {
        setError('Please login again.')
        return
      }

      const labResponse = await fetch(
        'http://127.0.0.1:9999/film-labs/',
        {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        }
      )

      const labData = await labResponse.json()

      if (!labResponse.ok) {
        throw new Error(
          labData.message ||
          'Cannot load film lab information.'
        )
      }

      const labs =
        labData.film_labs ||
        labData.data ||
        (Array.isArray(labData) ? labData : [])

      const ownLab = labs.find(
        (lab) => String(lab.owner_id) === String(user.id)
      )

      if (!ownLab) {
        setOrders([])
        setError('You do not have a film lab yet.')
        return
      }

      const response = await fetch(
        'http://127.0.0.1:9999/orders/',
        {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        }
      )

      const data = await response.json()

      if (!response.ok) {
        throw new Error(
          data.message || 'Cannot load orders.'
        )
      }

      const allOrders =
        data.orders ||
        data.data ||
        (Array.isArray(data) ? data : [])

      const ownOrders = allOrders.filter(
        (order) =>
          String(order.film_lab_id) === String(ownLab.id)
      )

      setOrders(ownOrders)
    } catch (err) {
      console.error(err)

      setError(
        err.message ||
        'Cannot connect to backend server.'
      )
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    loadOrders()
  }, [])

  // =========================================================
  // STATUS HELPERS
  // =========================================================

  const getStatusClass = (status) => {
    if (!status) {
      return 'status-default'
    }

    return `status-${String(status)
      .toLowerCase()
      .replace(/\s+/g, '-')}`
  }

  const formatStatus = (status) => {
    if (!status) {
      return 'Unknown'
    }

    const labels = {
      pending: 'Pending',
      confirmed: 'Confirmed',
      processing: 'Processing',
      start: 'Start',
      developing: 'Developing',
      scanning: 'Scanning',
      printing: 'Printing',
      quality_check: 'Quality Check',
      completed: 'Completed',
      ready_for_pickup: 'Ready for Pickup',
      delivering: 'Delivering',
      done: 'Done',
      cancelled: 'Cancelled',
    }

    return (
      labels[String(status).toLowerCase()] ||
      String(status)
    )
  }

  const formatDate = (value) => {
    if (!value) {
      return '—'
    }

    const date = new Date(value)

    if (Number.isNaN(date.getTime())) {
      return value
    }

    return date.toLocaleString()
  }

  const formatPrice = (value) => {
    if (
      value === null ||
      value === undefined ||
      value === ''
    ) {
      return '—'
    }

    const number = Number(value)

    if (Number.isNaN(number)) {
      return value
    }

    return `${number.toLocaleString()}`
  }

  const formatValue = (value) => {
    if (Array.isArray(value)) {
      return value.join(', ')
    }

    if (
      value === null ||
      value === undefined ||
      value === ''
    ) {
      return '—'
    }

    return value
  }

  // =========================================================
  // GET FORMAT
  // =========================================================

  const getOrderFormat = (order) => {
    const additionalRequests =
      order?.additional_requests

    if (!additionalRequests) {
      return '—'
    }

    const text = String(additionalRequests)

    const lines = text.split('\n')

    const formatLine = lines.find((line) =>
      line.trim().toLowerCase().startsWith('format:')
    )

    if (!formatLine) {
      return '—'
    }

    return (
      formatLine
        .substring(formatLine.indexOf(':') + 1)
        .trim() || '—'
    )
  }

  // =========================================================
  // FILTER
  // =========================================================

  const filteredOrders = orders.filter((order) => {
    if (statusFilter === 'all') {
      return true
    }

    return (
      String(order.status || '').toLowerCase() ===
      statusFilter.toLowerCase()
    )
  })

  const statuses = [
    ...new Set(
      orders
        .map((order) => order.status)
        .filter(Boolean)
    ),
  ]

  // =========================================================
  // NEXT STATUS
  // =========================================================

  const getNextStatuses = (order) => {
    if (!order) {
      return []
    }

    const currentStatus = String(
      order.status || ''
    ).toLowerCase()

    switch (currentStatus) {
      case 'processing':
        return [
          {
            value: 'start',
            label: 'Start Processing',
          },
        ]

      case 'start':
        return [
          {
            value: 'developing',
            label: 'Developing',
          },
        ]

      case 'developing':
        return [
          {
            value: 'scanning',
            label: 'Scanning',
          },
          {
            value: 'printing',
            label: 'Printing',
          },
          {
            value: 'quality_check',
            label: 'Quality Check',
          },
        ]

      case 'scanning':
        return [
          {
            value: 'printing',
            label: 'Printing',
          },
          {
            value: 'quality_check',
            label: 'Quality Check',
          },
        ]

      case 'printing':
        return [
          {
            value: 'quality_check',
            label: 'Quality Check',
          },
        ]

      case 'quality_check':
        return [
          {
            value: 'completed',
            label: 'Completed',
          },
        ]

      case 'completed':
        if (
          String(order.delivery_type).toLowerCase() ===
          'delivery'
        ) {
          return [
            {
              value: 'delivering',
              label: 'Delivering',
            },
          ]
        }

        return [
          {
            value: 'ready_for_pickup',
            label: 'Ready for Pickup',
          },
        ]

      case 'ready_for_pickup':
        return [
          {
            value: 'done',
            label: 'Done',
          },
        ]

      case 'delivering':
        return [
          {
            value: 'done',
            label: 'Done',
          },
        ]

      default:
        return []
    }
  }

  // =========================================================
  // UPDATE STATUS
  // =========================================================

  const updateOrderStatus = async (newStatus) => {
    if (!selectedOrder) {
      return
    }

    const currentStatus = String(
      selectedOrder.status || ''
    ).toLowerCase()

    // -------------------------------------------------------
    // PENDING
    // -------------------------------------------------------

    if (
      currentStatus === 'pending' &&
      !['confirmed', 'cancelled'].includes(newStatus)
    ) {
      setError(
        'A pending order can only be accepted or rejected.'
      )
      return
    }

    // -------------------------------------------------------
    // CONFIRMED
    // -------------------------------------------------------

    if (
      currentStatus === 'confirmed' &&
      newStatus !== 'processing'
    ) {
      setError(
        'A confirmed order must be paid before processing.'
      )
      return
    }

    // -------------------------------------------------------
    // OTHER INVALID OWNER ACTIONS
    // -------------------------------------------------------

    if (
      currentStatus !== 'pending' &&
      newStatus === 'cancelled'
    ) {
      setError(
        'This order can no longer be rejected.'
      )
      return
    }

    if (
      currentStatus !== 'pending' &&
      newStatus === 'confirmed'
    ) {
      setError(
        'This order has already been processed.'
      )
      return
    }

    setUpdatingStatus(true)
    setStatusMessage('')
    setError('')

    try {
      const token = getToken()

      if (!token) {
        throw new Error('Please login again.')
      }

      const response = await fetch(
        `http://127.0.0.1:9999/orders/${selectedOrder.id}`,
        {
          method: 'PUT',
          headers: {
            Authorization: `Bearer ${token}`,
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({
            status: newStatus,
          }),
        }
      )

      const data = await response.json()

      if (!response.ok) {
        throw new Error(
          data.message ||
          data.error ||
          'Cannot update order status.'
        )
      }

      const updatedOrder = data.order

      const newOrder = {
        ...selectedOrder,
        ...(updatedOrder || {}),
        status: newStatus,
      }

      setOrders((currentOrders) =>
        currentOrders.map((order) =>
          String(order.id) ===
          String(selectedOrder.id)
            ? newOrder
            : order
        )
      )

      setSelectedOrder(newOrder)

      if (
        String(newOrder.status || '').toLowerCase() ===
        'completed'
      ) {
        loadOrderResult(newOrder.id)
      }

      setStatusMessage(
        `Order status updated to ${formatStatus(
          newStatus
        )}.`
      )
    } catch (err) {
      console.error(err)

      setError(
        err.message ||
        'Cannot update order status.'
      )
    } finally {
      setUpdatingStatus(false)
    }
  }

  const handleAccept = () => {
    updateOrderStatus('confirmed')
  }

  const handleReject = () => {
    updateOrderStatus('cancelled')
  }

  // =========================================================
  // UPDATE STATUS BUTTONS
  // =========================================================

  const renderStatusActions = () => {
    if (!selectedOrder) {
      return null
    }

    const currentStatus = String(
      selectedOrder.status || ''
    ).toLowerCase()

    const nextStatuses =
      getNextStatuses(selectedOrder)

    if (nextStatuses.length === 0) {
      return null
    }

    return (
      <div>
        <label>Update Order Status</label>

        <div className="order-actions">
          {nextStatuses.map((nextStatus) => (
            <button
              key={nextStatus.value}
              className="accept-order-button"
              onClick={() =>
                updateOrderStatus(
                  nextStatus.value
                )
              }
              disabled={updatingStatus}
            >
              {updatingStatus
                ? 'Updating...'
                : nextStatus.label}
            </button>
          ))}
        </div>

        {currentStatus === 'developing' && (
          <small>
            Choose the next processing step based on
            the services selected by the customer.
          </small>
        )}
      </div>
    )
  }

  // =========================================================
  // ORDER RESULT
  // =========================================================

  const loadOrderResult = async (orderId) => {
    try {
      const token = getToken()

      if (!token) {
        throw new Error('Please login again.')
      }

      const response = await fetch(
        `http://127.0.0.1:9999/order-results/${orderId}`,
        {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        }
      )

      const data = await response.json()

      if (!response.ok) {
        throw new Error(
          data.message ||
          data.error ||
          'Cannot load order result.'
        )
      }

      setResultFiles(data.files || [])
    } catch (err) {
      console.error(err)
      setResultFiles([])
      setResultError(
        err.message || 'Cannot load order result.'
      )
    }
  }

  // =========================================================
  // UPLOAD ORDER RESULT
  // =========================================================

  const handleResultFilesSelected = async (event) => {
    const files = Array.from(event.target.files || [])

    if (!files.length || !selectedOrder) {
      return
    }

    setUploadingResult(true)
    setResultMessage('')
    setResultError('')

    try {
      const token = getToken()

      if (!token) {
        throw new Error('Please login again.')
      }

      const formData = new FormData()

      files.forEach((file) => {
        formData.append('files', file)
      })

      const response = await fetch(
        `http://127.0.0.1:9999/order-results/${selectedOrder.id}/upload`,
        {
          method: 'POST',
          headers: {
            Authorization: `Bearer ${token}`,
          },
          body: formData,
        }
      )

      let data = {}

      try {
        data = await response.json()
      } catch {
        data = {}
      }

      if (!response.ok) {
        // Backend của mình trả cả message và error.
        // Hiển thị error thật để biết chính xác lỗi 500.
        const backendError =
          data.error ||
          data.message ||
          'Cannot upload order result.'

        throw new Error(backendError)
      }

      const uploadedFiles = data.files || []

      setResultFiles((currentFiles) => [
        ...currentFiles,
        ...uploadedFiles,
      ])

      setResultMessage(
        `${uploadedFiles.length} result file${
          uploadedFiles.length !== 1 ? 's' : ''
        } uploaded successfully.`
      )
    } catch (err) {
      console.error(
        'ORDER RESULT UPLOAD ERROR:',
        err
      )

      setResultError(
        err.message ||
        'Cannot upload order result.'
      )
    } finally {
      setUploadingResult(false)

      if (resultInputRef.current) {
        resultInputRef.current.value = ''
      }
    }
  }

  const openResultFilePicker = () => {
    setResultMessage('')
    setResultError('')

    if (resultInputRef.current) {
      resultInputRef.current.click()
    }
  }

  const downloadOrderResult = async () => {
    if (!selectedOrder) {
      return
    }

    try {
      const token = getToken()

      if (!token) {
        throw new Error('Please login again.')
      }

      const response = await fetch(
        `http://127.0.0.1:9999/order-results/${selectedOrder.id}/download`,
        {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        }
      )

      if (!response.ok) {
        let data = {}

        try {
          data = await response.json()
        } catch {
          data = {}
        }

        throw new Error(
          data.error ||
          data.message ||
          'Cannot download order result.'
        )
      }

      const blob = await response.blob()
      const url = window.URL.createObjectURL(blob)
      const link = document.createElement('a')

      link.href = url
      link.download = `order_${selectedOrder.id}_results.zip`

      document.body.appendChild(link)
      link.click()
      link.remove()

      window.URL.revokeObjectURL(url)
    } catch (err) {
      console.error(err)

      setResultError(
        err.message || 'Cannot download order result.'
      )
    }
  }

  // =========================================================
  // RENDER
  // =========================================================

  return (
    <div className="order-management">

      {/* =====================================================
          HEADER
      ===================================================== */}

      <div className="order-header">
        <div>
          <h1>Order Management</h1>

          <p>
            View and manage orders received by your film lab.
          </p>
        </div>

        <button
          className="refresh-button"
          onClick={loadOrders}
          disabled={loading}
        >
          {loading ? 'Loading...' : 'Refresh'}
        </button>
      </div>

      {/* =====================================================
          ERROR
      ===================================================== */}

      {error && (
        <div className="order-error">
          {error}
        </div>
      )}

      {/* =====================================================
          TOOLBAR
      ===================================================== */}

      <div className="order-toolbar">

        <div className="order-count">
          {filteredOrders.length} order
          {filteredOrders.length !== 1
            ? 's'
            : ''}
        </div>

        <select
          value={statusFilter}
          onChange={(e) =>
            setStatusFilter(e.target.value)
          }
        >
          <option value="all">
            All Status
          </option>

          {statuses.map((status) => (
            <option
              key={status}
              value={status}
            >
              {formatStatus(status)}
            </option>
          ))}
        </select>

      </div>

      {/* =====================================================
          ORDER LIST
      ===================================================== */}

      {loading ? (
        <div className="order-loading">
          Loading orders...
        </div>
      ) : filteredOrders.length === 0 ? (
        <div className="order-empty">
          <h3>No orders found</h3>

          <p>
            There are currently no orders for your film lab.
          </p>
        </div>
      ) : (
        <div className="order-list">

          {filteredOrders.map((order) => (
            <div
              className="order-card"
              key={order.id}
            >

              {/* =================================================
                  CARD HEADER
              ================================================= */}

              <div className="order-card-header">

                <div>
                  <h3>
                    Order #{order.id}
                  </h3>

                  <p>
                    Created:{' '}
                    {formatDate(
                      order.created_at
                    )}
                  </p>
                </div>

                <span
                  className={`order-status ${getStatusClass(
                    order.status
                  )}`}
                >
                  {formatStatus(
                    order.status
                  )}
                </span>

              </div>

              {/* =================================================
                  ORDER INFO
              ================================================= */}

              <div className="order-info-grid">

                <div>
                  <span>Format</span>

                  <strong>
                    {getOrderFormat(order)}
                  </strong>
                </div>

                <div>
                  <span>Quantity</span>

                  <strong>
                    {order.quantity || 1}
                  </strong>
                </div>

                <div>
                  <span>Delivery</span>

                  <strong>
                    {order.delivery_type ||
                      'pickup'}
                  </strong>
                </div>

                <div>
                  <span>Price</span>

                  <strong>
                    {formatPrice(
                      order.total_amount
                    )}
                  </strong>
                </div>

                <div>
                  <span>Processing</span>

                  <strong>
                    {formatValue(
                      order.processing_options
                    )}
                  </strong>
                </div>

                <div>
                  <span>Scan Quality</span>

                  <strong>
                    {formatValue(
                      order.scanning_quality
                    )}
                  </strong>
                </div>

              </div>

              {/* =================================================
                  CARD FOOTER
              ================================================= */}

              <div className="order-card-footer">

                <button
                  className="view-order-button"
                  onClick={() => {
                    setSelectedOrder(order)
                    setStatusMessage('')
                    setError('')
                    setResultMessage('')
                    setResultError('')
                    setResultFiles([])

                    if (
                      String(order.status || '').toLowerCase() ===
                      'completed'
                    ) {
                      loadOrderResult(order.id)
                    }
                  }}
                >
                  View Details
                </button>

              </div>

            </div>
          ))}

        </div>
      )}

      {/* =======================================================
          ORDER DETAIL MODAL
      ======================================================= */}

      {selectedOrder && (
        <div
          className="order-modal-overlay"
          onClick={() =>
            setSelectedOrder(null)
          }
        >

          <div
            className="order-modal"
            onClick={(e) =>
              e.stopPropagation()
            }
          >

            {/* =================================================
                MODAL HEADER
            ================================================= */}

            <div className="order-modal-header">

              <div>
                <h2>
                  Order #{selectedOrder.id}
                </h2>

                <p>
                  {formatDate(
                    selectedOrder.created_at
                  )}
                </p>
              </div>

              <button
                className="close-modal-button"
                onClick={() =>
                  setSelectedOrder(null)
                }
              >
                ×
              </button>

            </div>

            <div className="order-detail-list">

              {/* =================================================
                  STATUS
              ================================================= */}

              <div>
                <label>Status</label>

                <p>
                  <span
                    className={`order-status ${getStatusClass(
                      selectedOrder.status
                    )}`}
                  >
                    {formatStatus(
                      selectedOrder.status
                    )}
                  </span>
                </p>
              </div>

              {/* =================================================
                  PENDING ACTION
              ================================================= */}

              {String(
                selectedOrder.status || ''
              ).toLowerCase() ===
                'pending' && (
                <div>

                  <label>
                    Owner Action
                  </label>

                  <div className="order-actions">

                    <button
                      className="accept-order-button"
                      onClick={handleAccept}
                      disabled={
                        updatingStatus
                      }
                    >
                      {updatingStatus
                        ? 'Updating...'
                        : 'Accept Order'}
                    </button>

                    <button
                      className="reject-order-button"
                      onClick={handleReject}
                      disabled={
                        updatingStatus
                      }
                    >
                      {updatingStatus
                        ? 'Updating...'
                        : 'Reject Order'}
                    </button>

                  </div>

                  <small>
                    Accepting the order allows
                    the customer to proceed with
                    payment.
                  </small>

                </div>
              )}

              {/* =================================================
                  CONFIRMED
              ================================================= */}

              {String(
                selectedOrder.status || ''
              ).toLowerCase() ===
                'confirmed' && (
                <div>

                  <label>
                    Payment
                  </label>

                  <p>
                    Waiting for customer payment.
                  </p>

                </div>
              )}

              {/* =================================================
                  PROCESSING
              ================================================= */}

              {String(
                selectedOrder.status || ''
              ).toLowerCase() ===
                'processing' && (
                <div>

                  <label>
                    Processing
                  </label>

                  <p>
                    Payment has been completed
                    and this order is ready to
                    start processing.
                  </p>

                </div>
              )}

              {/* =================================================
                  PROCESSING STATUS ACTIONS
              ================================================= */}

              {renderStatusActions()}

              {/* =================================================
                  ORDER RESULT
              ================================================= */}

              {String(
                selectedOrder.status || ''
              ).toLowerCase() === 'completed' && (
                <div className="order-result-section">

                  <label>
                    Order Result
                  </label>

                  <input
                    ref={resultInputRef}
                    type="file"
                    accept="image/*"
                    multiple
                    webkitdirectory="true"
                    directory=""
                    onChange={handleResultFilesSelected}
                    style={{ display: 'none' }}
                  />

                  <div className="order-actions">

                    <button
                      type="button"
                      className="accept-order-button"
                      onClick={openResultFilePicker}
                      disabled={uploadingResult}
                    >
                      {uploadingResult
                        ? 'Uploading...'
                        : 'Upload Result Folder'}
                    </button>

                    {resultFiles.length > 0 && (
                      <button
                        type="button"
                        className="view-order-button"
                        onClick={downloadOrderResult}
                      >
                        Download ZIP
                      </button>
                    )}

                  </div>

                  <small>
                    Upload is optional. Select a folder containing
                    multiple images. Uploading the result does not
                    change the order status.
                  </small>

                  {resultFiles.length > 0 && (
                    <div>
                      <small>
                        {resultFiles.length} result file
                        {resultFiles.length !== 1 ? 's' : ''} uploaded.
                      </small>

                      <div>
                        {resultFiles.map((file) => (
                          <div key={file.id}>
                            {file.file_name}
                          </div>
                        ))}
                      </div>
                    </div>
                  )}

                  {resultMessage && (
                    <small>
                      {resultMessage}
                    </small>
                  )}

                  {resultError && (
                    <small>
                      {resultError}
                    </small>
                  )}

                </div>
              )}

              {/* =================================================
                  STATUS MESSAGE
              ================================================= */}

              {updatingStatus && (
                <small>
                  Updating order...
                </small>
              )}

              {statusMessage && (
                <small>
                  {statusMessage}
                </small>
              )}

              {/* =================================================
                  CUSTOMER
              ================================================= */}

              <div>
                <label>
                  Customer ID
                </label>

                <p>
                  {selectedOrder.customer_id ||
                    '—'}
                </p>
              </div>

              {/* =================================================
                  FORMAT
              ================================================= */}

              <div>
                <label>
                  Format
                </label>

                <p>
                  {getOrderFormat(
                    selectedOrder
                  )}
                </p>
              </div>

              {/* =================================================
                  SERVICE
              ================================================= */}

              <div>
                <label>
                  Service ID
                </label>

                <p>
                  {selectedOrder.service_id ||
                    '—'}
                </p>
              </div>

              {/* =================================================
                  QUANTITY
              ================================================= */}

              <div>
                <label>
                  Quantity
                </label>

                <p>
                  {selectedOrder.quantity ||
                    1}
                </p>
              </div>

              {/* =================================================
                  DELIVERY
              ================================================= */}

              <div>
                <label>
                  Delivery Type
                </label>

                <p>
                  {selectedOrder.delivery_type ||
                    'pickup'}
                </p>
              </div>

              {/* =================================================
                  PROCESSING OPTIONS
              ================================================= */}

              <div>
                <label>
                  Processing Options
                </label>

                <p>
                  {formatValue(
                    selectedOrder.processing_options
                  )}
                </p>
              </div>

              {/* =================================================
                  SCAN QUALITY
              ================================================= */}

              <div>
                <label>
                  Scan Quality
                </label>

                <p>
                  {formatValue(
                    selectedOrder.scanning_quality
                  )}
                </p>
              </div>

              {/* =================================================
                  PRINTING
              ================================================= */}

              <div>
                <label>
                  Printing Requirements
                </label>

                <p>
                  {selectedOrder
                    .printing_requirements ||
                    '—'}
                </p>
              </div>

              {/* =================================================
                  ADDITIONAL REQUESTS
              ================================================= */}

              <div>
                <label>
                  Additional Requests
                </label>

                <p>
                  {selectedOrder
                    .additional_requests ||
                    '—'}
                </p>
              </div>

              {/* =================================================
                  NOTES
              ================================================= */}

              <div>
                <label>
                  Notes
                </label>

                <p>
                  {selectedOrder.notes ||
                    '—'}
                </p>
              </div>

              {/* =================================================
                  TOTAL
              ================================================= */}

              <div>
                <label>
                  Total Amount
                </label>

                <p>
                  {formatPrice(
                    selectedOrder.total_amount
                  )}
                </p>
              </div>

            </div>

          </div>

        </div>
      )}

    </div>
  )
}

export default OrderManagement