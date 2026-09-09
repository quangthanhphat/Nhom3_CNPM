import { useEffect, useState } from 'react'

const API_URL = 'http://127.0.0.1:9999'

function DeliveryManagement() {
  const [selectedCarrier, setSelectedCarrier] = useState(null)
  const [orders, setOrders] = useState([])
  const [selectedOrder, setSelectedOrder] = useState(null)

  const [assignedDeliveries, setAssignedDeliveries] =
    useState([])

  const [loading, setLoading] = useState(false)
  const [assigning, setAssigning] = useState(false)
  const [error, setError] = useState('')

  // =========================
  // SHIPPING CARRIERS
  // =========================

  const carriers = [
    {
      id: 'ghn',
      name: 'Giao Hàng Nhanh',
      shortName: 'GHN',
      icon: '🚚',
      description: 'Fast and convenient delivery',
    },
    {
      id: 'ghtk',
      name: 'Giao Hàng Tiết Kiệm',
      shortName: 'GHTK',
      icon: '📦',
      description: 'Affordable delivery service',
    },
    {
      id: 'viettel-post',
      name: 'Viettel Post',
      shortName: 'Viettel Post',
      icon: '🚛',
      description: 'Nationwide delivery',
    },
    {
      id: 'vnpost',
      name: 'VNPost',
      shortName: 'VNPost',
      icon: '📮',
      description: 'Postal delivery service',
    },
  ]

  // =========================
  // LOAD ORDERS
  // =========================

  const loadOrders = async () => {
    try {
      setLoading(true)
      setError('')

      const token = localStorage.getItem('token')

      if (!token) {
        throw new Error(
          'Authentication token not found.'
        )
      }

      const response = await fetch(
        `${API_URL}/orders/`,
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
          'Failed to load orders.'
        )
      }

      const orderList =
        Array.isArray(data)
          ? data
          : data.orders ||
            data.data ||
            []

      // Chỉ lấy order đã hoàn thành
      // và chọn delivery.
      const deliveryOrders =
        orderList.filter((order) => {
          const status =
            String(
              order.status || ''
            ).toLowerCase()

          const deliveryType =
            String(
              order.delivery_type || ''
            ).toLowerCase()

          return (
            status === 'completed' &&
            deliveryType === 'delivery'
          )
        })

      setOrders(deliveryOrders)

    } catch (err) {
      console.error(
        'Failed to load delivery orders:',
        err
      )

      setError(
        err.message ||
        'Failed to load orders.'
      )

    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    loadOrders()
  }, [])

  // =========================
  // SELECT CARRIER
  // =========================

  const handleSelectCarrier = (
    carrier
  ) => {
    setSelectedCarrier(carrier)
    setSelectedOrder(null)
  }

  // =========================
  // SELECT ORDER
  // =========================

  const handleSelectOrder = (
    order
  ) => {
    setSelectedOrder(order)
  }

  // =========================
  // FORMAT MONEY
  // =========================

  const formatCurrency = (
    amount
  ) => {
    return new Intl.NumberFormat(
      'vi-VN',
      {
        style: 'currency',
        currency: 'VND',
        maximumFractionDigits: 0,
      }
    ).format(
      Number(amount || 0)
    )
  }

  // =========================
  // FORMAT STATUS
  // =========================

  const formatStatus = (
    status
  ) => {
    return String(
      status || ''
    )
      .replaceAll('_', ' ')
      .replace(/\b\w/g, (char) =>
        char.toUpperCase()
      )
  }

  // =========================
  // ASSIGN ORDER
  // =========================

  const handleAssignOrder = async () => {
    if (
      !selectedCarrier ||
      !selectedOrder
    ) {
      return
    }

    try {
      setAssigning(true)
      setError('')

      const token =
        localStorage.getItem('token')

      const response = await fetch(
        `${API_URL}/orders/${selectedOrder.id}`,
        {
          method: 'PUT',
          headers: {
            'Content-Type':
              'application/json',
            Authorization:
              `Bearer ${token}`,
          },
          body: JSON.stringify({
            status: 'delivering',
          }),
        }
      )

      const data =
        await response.json()

      if (!response.ok) {
        throw new Error(
          data.message ||
          'Failed to update order.'
        )
      }

      // ==========================================
      // ADD TO ASSIGNED DELIVERIES
      // ==========================================

      const assignedDelivery = {
        order: selectedOrder,
        carrier: selectedCarrier,
      }

      setAssignedDeliveries(
        (previous) => [
          ...previous,
          assignedDelivery,
        ]
      )

      // ==========================================
      // REMOVE FROM AVAILABLE ORDERS
      // ==========================================

      setOrders(
        (previousOrders) =>
          previousOrders.filter(
            (order) =>
              String(order.id) !==
              String(
                selectedOrder.id
              )
          )
      )

      setSelectedOrder(null)

    } catch (err) {
      console.error(
        'Failed to assign delivery:',
        err
      )

      setError(
        err.message ||
        'Failed to assign order.'
      )

    } finally {
      setAssigning(false)
    }
  }

  // =========================
  // CONFIRM DELIVERY
  // =========================

  const handleConfirmDelivery = (
    index
  ) => {
    setAssignedDeliveries(
      (previous) =>
        previous.filter(
          (_, deliveryIndex) =>
            deliveryIndex !== index
        )
    )
  }

  return (
    <div className="delivery-page">

      {/* =========================
          HEADER
          ========================= */}

      <div className="delivery-header">

        <div>
          <h1>
            Delivery
          </h1>

          <p>
            Choose a shipping carrier and
            assign an order for delivery.
          </p>
        </div>

        <button
          className="delivery-refresh-button"
          onClick={loadOrders}
          disabled={loading}
        >
          {loading
            ? 'Loading...'
            : '↻ Refresh'}
        </button>

      </div>

      {/* =========================
          ERROR
          ========================= */}

      {error && (
        <div className="delivery-error">
          {error}
        </div>
      )}

      {/* =========================
          STEP 1
          ========================= */}

      <div className="delivery-section">

        <div className="delivery-section-title">

          <div className="delivery-step">
            1
          </div>

          <div>
            <h2>
              Choose Shipping Carrier
            </h2>

            <p>
              Select the delivery company
              you want to use.
            </p>
          </div>

        </div>

        <div className="carrier-grid">

          {carriers.map(
            (carrier) => {

              const selected =
                selectedCarrier?.id ===
                carrier.id

              return (
                <button
                  key={carrier.id}
                  className={
                    selected
                      ? 'carrier-card selected'
                      : 'carrier-card'
                  }
                  onClick={() =>
                    handleSelectCarrier(
                      carrier
                    )
                  }
                >

                  <div className="carrier-icon">
                    {carrier.icon}
                  </div>

                  <div className="carrier-info">

                    <strong>
                      {carrier.name}
                    </strong>

                    <span>
                      {carrier.description}
                    </span>

                  </div>

                  {selected && (
                    <div className="carrier-check">
                      ✓
                    </div>
                  )}

                </button>
              )
            }
          )}

        </div>

      </div>

      {/* =========================
          STEP 2
          ========================= */}

      {selectedCarrier && (

        <div className="delivery-section">

          <div className="delivery-section-title">

            <div className="delivery-step">
              2
            </div>

            <div>
              <h2>
                Choose Order
              </h2>

              <p>
                Orders ready for delivery
                with{' '}
                <strong>
                  {selectedCarrier.name}
                </strong>
              </p>
            </div>

          </div>

          {loading ? (

            <div className="delivery-empty">
              Loading orders...
            </div>

          ) : orders.length === 0 ? (

            <div className="delivery-empty">

              <div className="delivery-empty-icon">
                📦
              </div>

              <strong>
                No orders ready for delivery
              </strong>

              <p>
                Completed delivery orders
                will appear here.
              </p>

            </div>

          ) : (

            <div className="delivery-order-list">

              {orders.map(
                (order) => {

                  const selected =
                    selectedOrder?.id ===
                    order.id

                  return (
                    <button
                      key={order.id}
                      className={
                        selected
                          ? 'delivery-order-card selected'
                          : 'delivery-order-card'
                      }
                      onClick={() =>
                        handleSelectOrder(
                          order
                        )
                      }
                    >

                      <div className="delivery-order-main">

                        <div className="delivery-order-icon">
                          📦
                        </div>

                        <div>

                          <strong>
                            Order #
                            {String(
                              order.id
                            ).slice(
                              0,
                              8
                            )}
                          </strong>

                          <span>
                            Quantity:{' '}
                            {order.quantity ||
                              1}
                          </span>

                          <span>
                            Delivery:{' '}
                            {order.delivery_type ||
                              'delivery'}
                          </span>

                        </div>

                      </div>

                      <div className="delivery-order-right">

                        <strong>
                          {formatCurrency(
                            order.total_amount
                          )}
                        </strong>

                        <span className="delivery-status">
                          {formatStatus(
                            order.status
                          )}
                        </span>

                        {selected && (
                          <span className="order-selected-check">
                            ✓
                          </span>
                        )}

                      </div>

                    </button>
                  )
                }
              )}

            </div>

          )}

        </div>
      )}

      {/* =========================
          SELECTED ORDER
          ========================= */}

      {selectedCarrier &&
        selectedOrder && (

        <div className="delivery-confirmation">

          <div>

            <span className="delivery-confirmation-label">
              Selected Carrier
            </span>

            <strong>
              {selectedCarrier.icon}{' '}
              {selectedCarrier.name}
            </strong>

          </div>

          <div>

            <span className="delivery-confirmation-label">
              Selected Order
            </span>

            <strong>
              #
              {String(
                selectedOrder.id
              ).slice(0, 8)}
            </strong>

          </div>

          <button
            className="assign-delivery-button"
            onClick={
              handleAssignOrder
            }
            disabled={assigning}
          >
            {assigning
              ? 'Assigning...'
              : 'Assign Order to Carrier'}
          </button>

        </div>
      )}

      {/* =========================
          ASSIGNED DELIVERIES
          ========================= */}

      {assignedDeliveries.length > 0 && (

        <div className="assigned-deliveries-section">

          <div className="delivery-section-title">

            <div className="delivery-step">
              3
            </div>

            <div>
              <h2>
                Assigned Deliveries
              </h2>

              <p>
                Orders that have been assigned
                to a shipping carrier.
              </p>
            </div>

          </div>

          <div className="assigned-delivery-list">

            {assignedDeliveries.map(
              (
                delivery,
                index
              ) => {

                const order =
                  delivery.order

                const carrier =
                  delivery.carrier

                return (
                  <div
                    className="assigned-delivery-card"
                    key={`${order.id}-${index}`}
                  >

                    <div className="assigned-delivery-info">

                      <div className="assigned-delivery-icon">
                        📦
                      </div>

                      <div className="assigned-delivery-details">

                        <strong>
                          Order #
                          {String(
                            order.id
                          ).slice(
                            0,
                            8
                          )}
                        </strong>

                        <span>
                          🚚 Giao bởi:{' '}
                          {carrier.name}
                        </span>

                      </div>

                    </div>

                    <button
                      className="confirm-delivery-button"
                      onClick={() =>
                        handleConfirmDelivery(
                          index
                        )
                      }
                    >
                      ✓ Confirm
                    </button>

                  </div>
                )
              }
            )}

          </div>

        </div>
      )}

    </div>
  )
}

export default DeliveryManagement