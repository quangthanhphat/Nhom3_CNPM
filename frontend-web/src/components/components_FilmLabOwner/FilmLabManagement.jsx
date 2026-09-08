import { useEffect, useState } from 'react'
import './FilmLabManagement.css'

function FilmLabManagement() {
  const [labData, setLabData] = useState({
    labName: '',
    address: '',
    city: '',
    district: '',
    phone: '',
    description: '',
  })

  const [filmLabId, setFilmLabId] = useState(null)
  const [message, setMessage] = useState('')
  const [error, setError] = useState('')
  const [loading, setLoading] = useState(true)
  const [saving, setSaving] = useState(false)
  const [editing, setEditing] = useState(false)

  useEffect(() => {
    const loadFilmLab = async () => {
      try {
        const token = localStorage.getItem('token')
        const user = JSON.parse(localStorage.getItem('user'))

        if (!token || !user) {
          setError('User is not logged in.')
          setLoading(false)
          return
        }

        const response = await fetch(
          'http://127.0.0.1:9999/film-labs/',
          {
            method: 'GET',
            headers: {
              Authorization: `Bearer ${token}`,
            },
          }
        )

        const data = await response.json()

        if (!response.ok) {
          setError(
            data.message ||
            'Failed to load film lab information.'
          )
          setLoading(false)
          return
        }

        const myLab = data.find(
          (lab) => lab.owner_id === user.id
        )

        if (myLab) {
          setFilmLabId(myLab.id)

          setLabData({
            labName: myLab.name || '',
            address: myLab.address || '',
            city: myLab.city || '',
            district: myLab.district || '',
            phone: myLab.phone || '',
            description: myLab.description || '',
          })
        }

        setLoading(false)

      } catch (err) {
        setError('Cannot connect to backend server.')
        setLoading(false)
      }
    }

    loadFilmLab()
  }, [])

  const handleChange = (e) => {
    const { name, value } = e.target

    setLabData({
      ...labData,
      [name]: value,
    })

    setMessage('')
    setError('')
  }

  const handleEdit = () => {
    setEditing(true)
    setMessage('')
    setError('')
  }

  const handleCancel = () => {
    setEditing(false)
    setMessage('')
    setError('')
  }

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

      const requestData = {
        name: labData.labName,
        address: labData.address,
        city: labData.city,
        district: labData.district,
        phone: labData.phone,
        description: labData.description,
      }

      let response

      if (filmLabId) {
        response = await fetch(
          `http://127.0.0.1:9999/film-labs/${filmLabId}`,
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
          'http://127.0.0.1:9999/film-labs/',
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
          'Failed to save film lab information.'
        )
        setSaving(false)
        return
      }

      if (!filmLabId && data.film_lab) {
        setFilmLabId(data.film_lab.id)
      }

      setMessage(
        'Film lab information saved successfully.'
      )

      setEditing(false)

    } catch (err) {
      setError('Cannot connect to backend server.')
    }

    setSaving(false)
  }

  if (loading) {
    return (
      <div className="film-lab-page">

        <div className="film-lab-card">

          <h1>Film Lab Management</h1>

          <p className="film-lab-subtitle">
            Loading film lab information...
          </p>

        </div>

      </div>
    )
  }

  return (
    <div className="film-lab-page">

      <div className="film-lab-card">

        <h1>Film Lab Management</h1>

        <p className="film-lab-subtitle">
          Manage your film lab information
        </p>

        <form onSubmit={handleSave}>

          <div className="film-lab-section">

            <h2>Lab Information</h2>

            <div className="film-lab-form">

              {/* LAB NAME */}

              <div className="film-lab-form-group">

                <label>
                  Lab Name
                </label>

                {editing ? (
                  <input
                    id="labName"
                    name="labName"
                    type="text"
                    value={labData.labName}
                    onChange={handleChange}
                    placeholder="Enter lab name"
                    required
                  />
                ) : (
                  <div className="film-lab-value">
                    {labData.labName || 'Not provided'}
                  </div>
                )}

              </div>


              {/* ADDRESS */}

              <div className="film-lab-form-group">

                <label>
                  Address
                </label>

                {editing ? (
                  <input
                    id="address"
                    name="address"
                    type="text"
                    value={labData.address}
                    onChange={handleChange}
                    placeholder="Enter address"
                    required
                  />
                ) : (
                  <div className="film-lab-value">
                    {labData.address || 'Not provided'}
                  </div>
                )}

              </div>


              {/* CITY */}

              <div className="film-lab-form-group">

                <label>
                  City
                </label>

                {editing ? (
                  <input
                    id="city"
                    name="city"
                    type="text"
                    value={labData.city}
                    onChange={handleChange}
                    placeholder="Enter city"
                    required
                  />
                ) : (
                  <div className="film-lab-value">
                    {labData.city || 'Not provided'}
                  </div>
                )}

              </div>


              {/* DISTRICT */}

              <div className="film-lab-form-group">

                <label>
                  District
                </label>

                {editing ? (
                  <input
                    id="district"
                    name="district"
                    type="text"
                    value={labData.district}
                    onChange={handleChange}
                    placeholder="Enter district"
                    required
                  />
                ) : (
                  <div className="film-lab-value">
                    {labData.district || 'Not provided'}
                  </div>
                )}

              </div>


              {/* PHONE */}

              <div className="film-lab-form-group">

                <label>
                  Phone
                </label>

                {editing ? (
                  <input
                    id="phone"
                    name="phone"
                    type="text"
                    value={labData.phone}
                    onChange={handleChange}
                    placeholder="Enter phone number"
                    required
                  />
                ) : (
                  <div className="film-lab-value">
                    {labData.phone || 'Not provided'}
                  </div>
                )}

              </div>


              {/* DESCRIPTION */}

              <div className="film-lab-form-group">

                <label>
                  Description
                </label>

                {editing ? (
                  <textarea
                    id="description"
                    name="description"
                    value={labData.description}
                    onChange={handleChange}
                    placeholder="Enter lab description"
                    rows="5"
                  />
                ) : (
                  <div className="film-lab-value film-lab-description">
                    {labData.description || 'Not provided'}
                  </div>
                )}

              </div>

            </div>


            {/* ERROR */}

            {error && (
              <p className="error-message">
                {error}
              </p>
            )}


            {/* SUCCESS */}

            {message && (
              <p className="save-message">
                {message}
              </p>
            )}


            {/* BUTTONS */}

            {editing ? (

              <div className="film-lab-action-buttons">

                <button
                  type="submit"
                  className="save-lab-button"
                  disabled={saving}
                >
                  {saving
                    ? 'Saving...'
                    : 'Save Changes'}
                </button>

                <button
                  type="button"
                  className="cancel-lab-button"
                  onClick={handleCancel}
                  disabled={saving}
                >
                  Cancel
                </button>

              </div>

            ) : (

              <button
                type="button"
                className="edit-lab-button"
                onClick={handleEdit}
              >
                Edit
              </button>

            )}

          </div>

        </form>

      </div>

    </div>
  )
}

export default FilmLabManagement