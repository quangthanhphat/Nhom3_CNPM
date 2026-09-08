import { useEffect, useState } from 'react'
import './ServiceManagement.css'

const FILM_FORMAT_OPTIONS = [
  '35mm / 135',
  '120',
  '220',
  '110',
  '126 / Instamatic',
  '127',
  '620',
  'APS / Advantix',
  '116',
  '616',
  '828',
  'Minox',
  '4×5',
  '5×7',
  '8×10',
  '11×14',
  '16×20',
  'Disposable Camera',
  'Panoramic / XPan',
  'Instant Film',
  'Motion Picture Film',
]

const PROCESSING_OPTIONS = [
  'C-41',
  'B&W',
  'E-6',
  'ECN-2',
]

const SPECIALIZED_TECHNIQUES = [
  'Push Processing',
  'Pull Processing',
  'Cross Processing',
  'Stand Development',
  'Semi-Stand Development',
  'C-41 Bleach Bypass',
  'Double Development',
]

const SCANNING_QUALITY_OPTIONS = [
  'Full HD',
  '2K',
  '4K',
  '6K',
  '8K',
]

const PRINTING_OPTIONS = [
  '4×6 Print',
  '5×7 Print',
  '8×10 Print',
  '11×14 Print',
  '16×20 Print',
  'Contact Sheet',
  'Borderless Print',
  'Matte Finish',
  'Glossy Finish',
]

function ServiceManagement() {
  const [services, setServices] = useState([])
  const [categories, setCategories] = useState([])

  const [filmLabId, setFilmLabId] = useState(null)

  const [loading, setLoading] = useState(true)
  const [saving, setSaving] = useState(false)

  const [editingId, setEditingId] = useState(null)
  const [showForm, setShowForm] = useState(false)

  const [message, setMessage] = useState('')
  const [error, setError] = useState('')

  const [formData, setFormData] = useState({
    category_id: '',
    name: '',
    description: '',
    price: '',
    turnaround_time_min: '',
    turnaround_time_max: '',
    processing_capacity: '',
    supported_film_formats: [],
    processing_options: [],
    scanning_quality: [],
    printing_options: [],
    specialized_techniques: [],
  })

  /* =========================
     LOAD DATA
  ========================= */

  useEffect(() => {
    const loadData = async () => {
      try {
        const token = localStorage.getItem('token')
        const user = JSON.parse(
          localStorage.getItem('user')
        )

        if (!token || !user) {
          setError('User is not logged in.')
          setLoading(false)
          return
        }

        /* =========================
           GET FILM LAB
        ========================= */

        const filmLabResponse = await fetch(
          'http://127.0.0.1:9999/film-labs/',
          {
            method: 'GET',
            headers: {
              Authorization: `Bearer ${token}`,
            },
          }
        )

        const filmLabData =
          await filmLabResponse.json()

        if (!filmLabResponse.ok) {
          setError(
            filmLabData.message ||
            'Failed to load film lab information.'
          )
          setLoading(false)
          return
        }

        const myLab = filmLabData.find(
          (lab) => lab.owner_id === user.id
        )

        if (!myLab) {
          setError(
            'Film lab information was not found.'
          )
          setLoading(false)
          return
        }

        setFilmLabId(myLab.id)

        /* =========================
           GET CATEGORIES
        ========================= */

        const categoryResponse = await fetch(
          'http://127.0.0.1:9999/service-categories/',
          {
            method: 'GET',
            headers: {
              Authorization: `Bearer ${token}`,
            },
          }
        )

        const categoryData =
          await categoryResponse.json()

        if (!categoryResponse.ok) {
          setError(
            categoryData.message ||
            'Failed to load service categories.'
          )
          setLoading(false)
          return
        }

        setCategories(categoryData)

        /* =========================
           GET SERVICES
        ========================= */

        const serviceResponse = await fetch(
          'http://127.0.0.1:9999/services/',
          {
            method: 'GET',
            headers: {
              Authorization: `Bearer ${token}`,
            },
          }
        )

        const serviceData =
          await serviceResponse.json()

        if (!serviceResponse.ok) {
          setError(
            serviceData.message ||
            'Failed to load services.'
          )
          setLoading(false)
          return
        }

        const myServices = serviceData.filter(
          (service) =>
            service.film_lab_id === myLab.id
        )

        setServices(myServices)
        setLoading(false)

      } catch (err) {
        setError(
          'Cannot connect to backend server.'
        )
        setLoading(false)
      }
    }

    loadData()
  }, [])

  /* =========================
     FORM CHANGE
  ========================= */

  const handleChange = (e) => {
    const { name, value } = e.target

    setFormData({
      ...formData,
      [name]: value,
    })

    setMessage('')
    setError('')
  }

  /* =========================
     CHECKBOX CHANGE
  ========================= */

  const handleCheckboxChange = (
    fieldName,
    option,
    checked
  ) => {
    const currentValues =
      formData[fieldName] || []

    const newValues = checked
      ? [...currentValues, option]
      : currentValues.filter(
          (item) => item !== option
        )

    setFormData({
      ...formData,
      [fieldName]: newValues,
    })

    setMessage('')
    setError('')
  }

  /* =========================
     RESET FORM
  ========================= */

  const resetForm = () => {
    setFormData({
      category_id: '',
      name: '',
      description: '',
      price: '',
      turnaround_time_min: '',
      turnaround_time_max: '',
      processing_capacity: '',
      supported_film_formats: [],
      processing_options: [],
      scanning_quality: [],
      printing_options: [],
      specialized_techniques: [],
    })

    setEditingId(null)
    setShowForm(false)
  }

  /* =========================
     ADD SERVICE
  ========================= */

  const handleAdd = () => {
    resetForm()
    setShowForm(true)
    setMessage('')
    setError('')
  }

  /* =========================
     EDIT SERVICE
  ========================= */

  const handleEdit = (service) => {
    setFormData({
      category_id: service.category_id || '',
      name: service.name || '',
      description: service.description || '',
      price: service.price ?? '',
      turnaround_time_min:
        service.turnaround_time_min ?? '',
      turnaround_time_max:
        service.turnaround_time_max ?? '',
      processing_capacity:
        service.processing_capacity ?? '',
      supported_film_formats:
        Array.isArray(service.supported_film_formats)
          ? service.supported_film_formats
          : [],
      processing_options:
        Array.isArray(service.processing_options)
          ? service.processing_options
          : [],
      scanning_quality:
        Array.isArray(service.scanning_quality)
          ? service.scanning_quality
          : [],
      printing_options:
        Array.isArray(service.printing_options)
          ? service.printing_options
          : [],
      specialized_techniques:
        Array.isArray(
          service.specialized_techniques
        )
          ? service.specialized_techniques
          : [],
    })

    setEditingId(service.id)
    setShowForm(true)
    setMessage('')
    setError('')
  }

  /* =========================
     GET SELECTED CATEGORY
  ========================= */

  const getSelectedCategoryName = () => {
    const category = categories.find(
      (item) => item.id === formData.category_id
    )

    return category
      ? category.name
      : ''
  }

  /* =========================
     SAVE SERVICE
  ========================= */

  const handleSave = async (e) => {
    e.preventDefault()

    setMessage('')
    setError('')
    setSaving(true)

    try {
      const token = localStorage.getItem('token')

      if (!token) {
        setError('User is not logged in.')
        setSaving(false)
        return
      }

      if (!filmLabId) {
        setError(
          'Film lab information was not found.'
        )
        setSaving(false)
        return
      }

      const categoryName =
        getSelectedCategoryName()

      if (
        formData.turnaround_time_min !== '' &&
        formData.turnaround_time_max !== '' &&
        Number(formData.turnaround_time_min) >
          Number(formData.turnaround_time_max)
      ) {
        setError(
          'Minimum turnaround time cannot be greater than maximum turnaround time.'
        )
        setSaving(false)
        return
      }

      const requestData = {
        film_lab_id: filmLabId,
        category_id: formData.category_id,
        name: formData.name,
        description: formData.description,

        price:
          formData.price === ''
            ? null
            : Number(formData.price),

        turnaround_time_min:
          formData.turnaround_time_min === ''
            ? null
            : Number(formData.turnaround_time_min),

        turnaround_time_max:
          formData.turnaround_time_max === ''
            ? null
            : Number(formData.turnaround_time_max),

        processing_capacity:
          formData.processing_capacity === ''
            ? null
            : Number(formData.processing_capacity),

        supported_film_formats:
          formData.supported_film_formats,

        processing_options:
          categoryName === 'Film Development'
            ? formData.processing_options
            : null,

        scanning_quality:
          categoryName === 'Film Scanning'
            ? formData.scanning_quality
            : null,

        printing_options:
          categoryName === 'Film Printing'
            ? formData.printing_options
            : null,

        specialized_techniques:
          categoryName === 'Film Development'
            ? formData.specialized_techniques
            : null,
      }

      let response

      if (editingId) {
        response = await fetch(
          `http://127.0.0.1:9999/services/${editingId}`,
          {
            method: 'PUT',
            headers: {
              'Content-Type': 'application/json',
              Authorization: `Bearer ${token}`,
            },
            body: JSON.stringify(requestData),
          }
        )
      } else {
        response = await fetch(
          'http://127.0.0.1:9999/services/',
          {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json',
              Authorization: `Bearer ${token}`,
            },
            body: JSON.stringify(requestData),
          }
        )
      }

      const data = await response.json()

      if (!response.ok) {
        setError(
          data.message ||
          'Failed to save service.'
        )
        setSaving(false)
        return
      }

      /* =========================
         UPDATE LOCAL LIST
      ========================= */

      if (editingId) {
        setServices(
          services.map((service) =>
            service.id === editingId
              ? data.service
              : service
          )
        )

        setMessage(
          'Service updated successfully.'
        )
      } else {
        setServices([
          ...services,
          data.service,
        ])

        setMessage(
          'Service created successfully.'
        )
      }

      resetForm()

    } catch (err) {
      setError(
        'Cannot connect to backend server.'
      )
    }

    setSaving(false)
  }

  /* =========================
     DELETE SERVICE
  ========================= */

  const handleDelete = async (serviceId) => {
    const confirmed = window.confirm(
      'Are you sure you want to delete this service?'
    )

    if (!confirmed) {
      return
    }

    setMessage('')
    setError('')

    try {
      const token = localStorage.getItem('token')

      if (!token) {
        setError('User is not logged in.')
        return
      }

      const response = await fetch(
        `http://127.0.0.1:9999/services/${serviceId}`,
        {
          method: 'DELETE',
          headers: {
            Authorization: `Bearer ${token}`,
          },
        }
      )

      const data = await response.json()

      if (!response.ok) {
        setError(
          data.message ||
          'Failed to delete service.'
        )
        return
      }

      setServices(
        services.filter(
          (service) =>
            service.id !== serviceId
        )
      )

      setMessage(
        'Service deleted successfully.'
      )

    } catch (err) {
      setError(
        'Cannot connect to backend server.'
      )
    }
  }

  /* =========================
     CATEGORY NAME
  ========================= */

  const getCategoryName = (categoryId) => {
    const category = categories.find(
      (item) => item.id === categoryId
    )

    return category
      ? category.name
      : 'Unknown Category'
  }

  /* =========================
     LOADING
  ========================= */

  if (loading) {
    return (
      <div className="service-management-page">
        <div className="service-management-card">

          <h1>
            Service Management
          </h1>

          <p className="service-management-subtitle">
            Loading service information...
          </p>

        </div>
      </div>
    )
  }

  /* =========================
     PAGE
  ========================= */

  return (
    <div className="service-management-page">

      <div className="service-management-card">

        <h1>
          Service Management
        </h1>

        <p className="service-management-subtitle">
          Manage your film lab services
        </p>

        {/* =========================
            MESSAGES
        ========================= */}

        {error && (
          <p className="service-error-message">
            {error}
          </p>
        )}

        {message && (
          <p className="service-success-message">
            {message}
          </p>
        )}

        {/* =========================
            ADD BUTTON
        ========================= */}

        {!showForm && (
          <button
            type="button"
            className="add-service-button"
            onClick={handleAdd}
          >
            Add Service
          </button>
        )}

        {/* =========================
            FORM
        ========================= */}

        {showForm && (
          <form
            className="service-form"
            onSubmit={handleSave}
          >

            <div className="service-form-group">

              <label>
                Service Category
              </label>

              <select
                name="category_id"
                value={formData.category_id}
                onChange={handleChange}
                required
              >

                <option value="">
                  Select a category
                </option>

                {categories.map((category) => (
                  <option
                    key={category.id}
                    value={category.id}
                  >
                    {category.name}
                  </option>
                ))}

              </select>

            </div>

            <div className="service-form-group">

              <label>
                Service Name
              </label>

              <input
                type="text"
                name="name"
                value={formData.name}
                onChange={handleChange}
                placeholder="Enter service name"
                required
              />

            </div>

            <div className="service-form-group">

              <label>
                Description
              </label>

              <textarea
                name="description"
                value={formData.description}
                onChange={handleChange}
                placeholder="Enter service description"
                rows="4"
              />

            </div>

            <div className="service-form-group">

              <label>
                Price
              </label>

              <input
                type="number"
                name="price"
                value={formData.price}
                onChange={handleChange}
                placeholder="Enter price"
                min="0"
                step="0.01"
                required
              />

            </div>

            {/* =========================
                TURNAROUND TIME
            ========================= */}

            <div className="service-form-group">

              <label>
                Turnaround Time
              </label>

              <div className="turnaround-time-fields">

                <select
                  name="turnaround_time_min"
                  value={formData.turnaround_time_min}
                  onChange={handleChange}
                >

                  <option value="">
                    From
                  </option>

                  {Array.from(
                    { length: 30 },
                    (_, index) => index + 1
                  ).map((day) => (
                    <option
                      key={day}
                      value={day}
                    >
                      {day} day{day > 1 ? 's' : ''}
                    </option>
                  ))}

                </select>

                <span>
                  to
                </span>

                <select
                  name="turnaround_time_max"
                  value={formData.turnaround_time_max}
                  onChange={handleChange}
                >

                  <option value="">
                    To
                  </option>

                  {Array.from(
                    { length: 30 },
                    (_, index) => index + 1
                  ).map((day) => (
                    <option
                      key={day}
                      value={day}
                    >
                      {day} day{day > 1 ? 's' : ''}
                    </option>
                  ))}

                </select>

              </div>

            </div>

            <div className="service-form-group">

              <label>
                Processing Capacity
              </label>

              <input
                type="number"
                name="processing_capacity"
                value={formData.processing_capacity}
                onChange={handleChange}
                placeholder="Enter processing capacity"
                min="0"
              />

            </div>

            {/* =========================
                SUPPORTED FILM FORMATS
            ========================= */}

            <div className="service-form-group">

              <label>
                Supported Film Formats
              </label>

              <div className="service-checkbox-list">

                {FILM_FORMAT_OPTIONS.map((option) => (
                  <label
                    key={option}
                    className="service-checkbox-item"
                  >

                    <input
                      type="checkbox"
                      checked={formData.supported_film_formats.includes(
                        option
                      )}
                      onChange={(e) =>
                        handleCheckboxChange(
                          'supported_film_formats',
                          option,
                          e.target.checked
                        )
                      }
                    />

                    <span>
                      {option}
                    </span>

                  </label>
                ))}

              </div>

            </div>

            {/* =========================
                DEVELOPMENT ONLY
            ========================= */}

            {getSelectedCategoryName() ===
              'Film Development' && (
              <>

                <div className="service-form-group">

                  <label>
                    Processing Options
                  </label>

                  <div className="service-checkbox-list">

                    {PROCESSING_OPTIONS.map(
                      (option) => (
                        <label
                          key={option}
                          className="service-checkbox-item"
                        >

                          <input
                            type="checkbox"
                            checked={formData.processing_options.includes(
                              option
                            )}
                            onChange={(e) =>
                              handleCheckboxChange(
                                'processing_options',
                                option,
                                e.target.checked
                              )
                            }
                          />

                          <span>
                            {option}
                          </span>

                        </label>
                      )
                    )}

                  </div>

                </div>

                <div className="service-form-group">

                  <label>
                    Specialized Techniques
                  </label>

                  <div className="service-checkbox-list">

                    {SPECIALIZED_TECHNIQUES.map(
                      (option) => (
                        <label
                          key={option}
                          className="service-checkbox-item"
                        >

                          <input
                            type="checkbox"
                            checked={formData.specialized_techniques.includes(
                              option
                            )}
                            onChange={(e) =>
                              handleCheckboxChange(
                                'specialized_techniques',
                                option,
                                e.target.checked
                              )
                            }
                          />

                          <span>
                            {option}
                          </span>

                        </label>
                      )
                    )}

                  </div>

                </div>

              </>
            )}

            {/* =========================
                SCANNING ONLY
            ========================= */}

            {getSelectedCategoryName() ===
              'Film Scanning' && (
              <div className="service-form-group">

                <label>
                  Scanning Quality
                </label>

                <div className="service-checkbox-list">

                  {SCANNING_QUALITY_OPTIONS.map(
                    (option) => (
                      <label
                        key={option}
                        className="service-checkbox-item"
                      >

                        <input
                          type="checkbox"
                          checked={formData.scanning_quality.includes(
                            option
                          )}
                          onChange={(e) =>
                            handleCheckboxChange(
                              'scanning_quality',
                              option,
                              e.target.checked
                            )
                          }
                        />

                        <span>
                          {option}
                        </span>

                      </label>
                    )
                  )}

                </div>

              </div>
            )}

            {/* =========================
                PRINTING ONLY
            ========================= */}

            {getSelectedCategoryName() ===
              'Film Printing' && (
              <div className="service-form-group">

                <label>
                  Printing Options
                </label>

                <div className="service-checkbox-list">

                  {PRINTING_OPTIONS.map(
                    (option) => (
                      <label
                        key={option}
                        className="service-checkbox-item"
                      >

                        <input
                          type="checkbox"
                          checked={formData.printing_options.includes(
                            option
                          )}
                          onChange={(e) =>
                            handleCheckboxChange(
                              'printing_options',
                              option,
                              e.target.checked
                            )
                          }
                        />

                        <span>
                          {option}
                        </span>

                      </label>
                    )
                  )}

                </div>

              </div>
            )}

            <div className="service-action-buttons">

              <button
                type="submit"
                className="save-service-button"
                disabled={saving}
              >
                {saving
                  ? 'Saving...'
                  : editingId
                    ? 'Save Changes'
                    : 'Create Service'}
              </button>

              <button
                type="button"
                className="cancel-service-button"
                onClick={resetForm}
                disabled={saving}
              >
                Cancel
              </button>

            </div>

          </form>
        )}

        {/* =========================
            SERVICE LIST
        ========================= */}

        {!showForm && (
          <div className="service-list">

            {services.length === 0 ? (

              <div className="service-item">

                <h3>
                  No services found
                </h3>

                <p>
                  Your film lab does not have any
                  services yet.
                </p>

              </div>

            ) : (

              services.map((service) => {

                const categoryName =
                  getCategoryName(
                    service.category_id
                  )

                return (
                  <div
                    className="service-item"
                    key={service.id}
                  >

                    <h3>
                      {service.name}
                    </h3>

                    <p>
                      <strong>
                        Category:
                      </strong>{' '}
                      {categoryName}
                    </p>

                    <p>
                      <strong>
                        Price:
                      </strong>{' '}
                      {service.price}
                    </p>

                    <p>
                      <strong>
                        Turnaround Time:
                      </strong>{' '}
                      {service.turnaround_time_min &&
                      service.turnaround_time_max
                        ? `${service.turnaround_time_min}-${service.turnaround_time_max} days`
                        : 'Not provided'}
                    </p>

                    <p>
                      <strong>
                        Processing Capacity:
                      </strong>{' '}
                      {service.processing_capacity ??
                        'Not provided'}
                    </p>

                    <p>
                      <strong>
                        Supported Film Formats:
                      </strong>{' '}
                      {Array.isArray(
                        service.supported_film_formats
                      )
                        ? service.supported_film_formats.join(
                            ', '
                          )
                        : 'Not provided'}
                    </p>

                    {categoryName ===
                      'Film Development' && (
                      <>

                        <p>
                          <strong>
                            Processing Options:
                          </strong>{' '}
                          {Array.isArray(
                            service.processing_options
                          )
                            ? service.processing_options.join(
                                ', '
                              )
                            : 'Not provided'}
                        </p>

                        <p>
                          <strong>
                            Specialized Techniques:
                          </strong>{' '}
                          {Array.isArray(
                            service.specialized_techniques
                          )
                            ? service.specialized_techniques.join(
                                ', '
                              )
                            : 'Not provided'}
                        </p>

                      </>
                    )}

                    {categoryName ===
                      'Film Scanning' && (
                      <p>
                        <strong>
                          Scanning Quality:
                        </strong>{' '}
                        {Array.isArray(
                          service.scanning_quality
                        )
                          ? service.scanning_quality.join(
                              ', '
                            )
                          : 'Not provided'}
                      </p>
                    )}

                    {categoryName ===
                      'Film Printing' && (
                      <p>
                        <strong>
                          Printing Options:
                        </strong>{' '}
                        {Array.isArray(
                          service.printing_options
                        )
                          ? service.printing_options.join(
                              ', '
                            )
                          : 'Not provided'}
                      </p>
                    )}

                    <p>
                      <strong>
                        Description:
                      </strong>{' '}
                      {service.description ||
                        'Not provided'}
                    </p>

                    <div className="service-action-buttons">

                      <button
                        type="button"
                        className="edit-service-button"
                        onClick={() =>
                          handleEdit(service)
                        }
                      >
                        Edit
                      </button>

                      <button
                        type="button"
                        className="delete-service-button"
                        onClick={() =>
                          handleDelete(service.id)
                        }
                      >
                        Delete
                      </button>

                    </div>

                  </div>
                )
              })

            )}

          </div>
        )}

      </div>

    </div>
  )
}

export default ServiceManagement