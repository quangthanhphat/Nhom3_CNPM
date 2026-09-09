import { useEffect, useState } from 'react'

import './Community.css'

const API_URL = 'http://127.0.0.1:9999'

function Community() {
  const [posts, setPosts] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')

  const [comments, setComments] = useState({})
  const [commentInputs, setCommentInputs] = useState({})
  const [commentLoading, setCommentLoading] = useState({})

  /*
   * ratings[postId] sẽ lưu:
   *
   * {
   *   ratings: [],
   *   average: 4.5,
   *   count: 2,
   *   my_rating: {...}
   * }
   */
  const [ratings, setRatings] = useState({})
  const [ratingInputs, setRatingInputs] = useState({})
  const [ratingLoading, setRatingLoading] = useState({})

  const token = localStorage.getItem('token')

  const getHeaders = () => ({
    Authorization: `Bearer ${token}`,
    'Content-Type': 'application/json',
  })

  // =========================================================
  // IMAGE URL
  // =========================================================

  const getPostImageUrl = (imagePath) => {
    if (!imagePath) return ''

    const storagePath = String(imagePath)
      .replace(/\\/g, '/')
      .replace(/^\/+/, '')

    if (
      storagePath.startsWith('http://') ||
      storagePath.startsWith('https://')
    ) {
      return storagePath
    }

    return `${API_URL}/posts/images/${storagePath}`
  }

  // =========================================================
  // LOAD POSTS
  // =========================================================

  const loadPosts = async () => {
    try {
      setLoading(true)
      setError('')

      const response = await fetch(`${API_URL}/posts/`, {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      })

      if (!response.ok) {
        throw new Error('Không thể tải Community')
      }

      const data = await response.json()

      const postList = Array.isArray(data)
        ? data
        : data.posts || data.data || []

      setPosts(postList)
    } catch (err) {
      console.error('Load community error:', err)
      setError(err.message || 'Không thể tải Community')
    } finally {
      setLoading(false)
    }
  }

  // =========================================================
  // LOAD COMMENTS
  // =========================================================

  const loadComments = async (postId) => {
    try {
      /*
       * Backend hiện tại đã có:
       *
       * GET /comments/
       *
       * Web lấy toàn bộ comment rồi lọc theo post_id.
       */
      const response = await fetch(
        `${API_URL}/comments/`,
        {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        }
      )

      if (!response.ok) {
        console.error(
          'Load comments failed:',
          response.status
        )
        return
      }

      const data = await response.json()

      const allComments = Array.isArray(data)
        ? data
        : data.comments || data.data || []

      /*
       * Chỉ lấy comment thuộc bài viết hiện tại.
       */
      const commentList = allComments.filter(
        (comment) =>
          String(comment.post_id) === String(postId)
      )

      setComments((prev) => ({
        ...prev,
        [postId]: commentList,
      }))
    } catch (err) {
      console.error('Load comments error:', err)
    }
  }

  // =========================================================
  // LOAD RATINGS
  // =========================================================

  const loadRating = async (postId) => {
    try {
      const response = await fetch(
        `${API_URL}/ratings/post/${postId}`,
        {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        }
      )

      if (!response.ok) {
        console.error(
          'Load rating failed:',
          response.status
        )
        return
      }

      const data = await response.json()

      /*
       * Backend trả:
       *
       * {
       *   ratings: [],
       *   average: 4.5,
       *   count: 2,
       *   my_rating: {...}
       * }
       */

      const ratingData = {
        ratings: Array.isArray(data?.ratings)
          ? data.ratings
          : [],
        average: Number(data?.average) || 0,
        count: Number(data?.count) || 0,
        my_rating: data?.my_rating || null,
      }

      setRatings((prev) => ({
        ...prev,
        [postId]: ratingData,
      }))

      // =====================================================
      // RESTORE CURRENT USER RATING
      // =====================================================

      const mine = ratingData.my_rating

      if (mine) {
        setRatingInputs((prev) => ({
          ...prev,
          [postId]: {
            rating: Number(mine.rating) || 0,
            review: mine.review || '',
          },
        }))
      } else {
        setRatingInputs((prev) => ({
          ...prev,
          [postId]: {
            rating: 0,
            review: '',
          },
        }))
      }
    } catch (err) {
      console.error('Load rating error:', err)
    }
  }

  // =========================================================
  // INITIAL LOAD
  // =========================================================

  useEffect(() => {
    if (!token) {
      setError('Bạn chưa đăng nhập')
      setLoading(false)
      return
    }

    loadPosts()
  }, [])

  // =========================================================
  // LOAD COMMENTS + RATINGS FOR EVERY POST
  // =========================================================

  useEffect(() => {
    if (!posts.length) return

    posts.forEach((post) => {
      if (!post?.id) return

      loadComments(post.id)
      loadRating(post.id)
    })
  }, [posts])

  // =========================================================
  // COMMENT INPUT
  // =========================================================

  const handleCommentChange = (postId, value) => {
    setCommentInputs((prev) => ({
      ...prev,
      [postId]: value,
    }))
  }

  // =========================================================
  // SUBMIT COMMENT
  // =========================================================

  const handleSubmitComment = async (postId) => {
    const content = (commentInputs[postId] || '').trim()

    if (!content) return

    try {
      setCommentLoading((prev) => ({
        ...prev,
        [postId]: true,
      }))

      const response = await fetch(
        `${API_URL}/comments/`,
        {
          method: 'POST',
          headers: getHeaders(),
          body: JSON.stringify({
            post_id: postId,
            content,
          }),
        }
      )

      const data = await response.json().catch(() => ({}))

      if (!response.ok) {
        alert(
          data.message ||
            'Không thể đăng bình luận'
        )
        return
      }

      // Clear input
      setCommentInputs((prev) => ({
        ...prev,
        [postId]: '',
      }))

      /*
       * Load lại comment thật từ DB.
       */
      await loadComments(postId)
    } catch (err) {
      console.error(
        'Create comment error:',
        err
      )

      alert('Không thể đăng bình luận')
    } finally {
      setCommentLoading((prev) => ({
        ...prev,
        [postId]: false,
      }))
    }
  }

  // =========================================================
  // RATING INPUT
  // =========================================================

  const handleRatingChange = (postId, value) => {
    setRatingInputs((prev) => ({
      ...prev,
      [postId]: {
        ...(prev[postId] || {}),
        rating: value,
      },
    }))
  }

  const handleReviewChange = (postId, value) => {
    setRatingInputs((prev) => ({
      ...prev,
      [postId]: {
        ...(prev[postId] || {}),
        review: value,
      },
    }))
  }

  // =========================================================
  // SUBMIT RATING
  // =========================================================

  const handleSubmitRating = async (postId) => {
    const input = ratingInputs[postId] || {}

    const rating = Number(input.rating || 0)
    const review = (input.review || '').trim()

    if (rating < 1 || rating > 5) {
      alert('Vui lòng chọn từ 1 đến 5 sao')
      return
    }

    try {
      setRatingLoading((prev) => ({
        ...prev,
        [postId]: true,
      }))

      const response = await fetch(
        `${API_URL}/ratings/`,
        {
          method: 'POST',
          headers: getHeaders(),
          body: JSON.stringify({
            target_type: 'post',
            target_id: postId,
            rating,
            review,
          }),
        }
      )

      const data = await response.json().catch(() => ({}))

      if (!response.ok) {
        alert(
          data.message ||
            'Không thể đánh giá bài viết'
        )
        return
      }

      await loadRating(postId)

      alert(
        'Đánh giá bài viết đã được lưu'
      )
    } catch (err) {
      console.error(
        'Rating error:',
        err
      )

      alert(
        'Không thể đánh giá bài viết'
      )
    } finally {
      setRatingLoading((prev) => ({
        ...prev,
        [postId]: false,
      }))
    }
  }

  // =========================================================
  // AUTHOR
  // =========================================================

  const getAuthorName = (post) => {
    if (post.author_name) {
      return post.author_name
    }

    if (post.author?.full_name) {
      return post.author.full_name
    }

    if (post.author?.username) {
      return post.author.username
    }

    return 'Photography Expert'
  }

  const getAuthorAvatar = (post) => {
    return (
      post.author_avatar_url ||
      post.author?.avatar_url ||
      post.author?.avatar ||
      null
    )
  }

  // =========================================================
  // DATE
  // =========================================================

  const formatDate = (date) => {
    if (!date) return ''

    try {
      return new Date(date).toLocaleString(
        'vi-VN'
      )
    } catch {
      return ''
    }
  }

  // =========================================================
  // RATING HELPERS
  // =========================================================

  const getAverageRating = (ratingData) => {
    if (!ratingData) return 0

    return (
      Number(ratingData.average) ||
      Number(ratingData.average_rating) ||
      Number(ratingData.avg_rating) ||
      0
    )
  }

  const getRatingCount = (ratingData) => {
    if (!ratingData) return 0

    return (
      Number(ratingData.count) ||
      Number(ratingData.total_ratings) ||
      Number(ratingData.rating_count) ||
      0
    )
  }

  // =========================================================
  // STARS
  // =========================================================

  const renderStars = (
    value,
    size = 'normal'
  ) => {
    const rating = Number(value) || 0

    return (
      <div
        className={`community-stars ${size}`}
      >
        {[1, 2, 3, 4, 5].map((star) => (
          <span
            key={star}
            className={
              rating >= star
                ? 'filled'
                : ''
            }
          >
            ★
          </span>
        ))}
      </div>
    )
  }

  // =========================================================
  // LOADING
  // =========================================================

  if (loading) {
    return (
      <div className="community-page">
        <div className="community-hero">
          <div className="community-hero-content">
            <div>
              <span className="community-kicker">
                FILM COMMUNITY
              </span>

              <h1>Community</h1>

              <p>
                Chia sẻ kiến thức, kinh nghiệm
                và những câu chuyện thú vị về
                nhiếp ảnh.
              </p>
            </div>
          </div>
        </div>

        <div className="community-loading">
          <div className="community-loading-spinner" />

          <span>
            Đang tải Community...
          </span>
        </div>
      </div>
    )
  }

  // =========================================================
  // MAIN
  // =========================================================

  return (
    <div className="community-page">

      {/* =====================================================
          HERO
      ===================================================== */}

      <div className="community-hero">
        <div className="community-hero-content">
          <div>
            <span className="community-kicker">
              FILM COMMUNITY
            </span>

            <h1>Community</h1>

            <p>
              Khám phá những chia sẻ từ
              Photography Expert, cùng thảo
              luận và đánh giá những bài viết
              hữu ích.
            </p>
          </div>

          <button
            className="community-refresh-button"
            onClick={loadPosts}
            disabled={loading}
          >
            ↻ Làm mới
          </button>
        </div>
      </div>

      {/* =====================================================
          ERROR
      ===================================================== */}

      {error && (
        <div className="community-error">
          <strong>
            Không thể tải Community
          </strong>

          <span>{error}</span>
        </div>
      )}

      {/* =====================================================
          EMPTY
      ===================================================== */}

      {!error && posts.length === 0 && (
        <div className="community-empty">
          <div className="community-empty-icon">
            ✦
          </div>

          <h2>
            Chưa có bài viết
          </h2>

          <p>
            Hiện tại chưa có bài viết nào
            trong Community.
          </p>
        </div>
      )}

      {/* =====================================================
          FEED
      ===================================================== */}

      <div className="community-feed">

        {posts.map((post) => {
          const postComments =
            comments[post.id] || []

          const postRating =
            ratings[post.id] || null

          const currentRating =
            ratingInputs[post.id] || {
              rating: 0,
              review: '',
            }

          const postImages =
            Array.isArray(post.images)
              ? post.images
              : []

          const authorName =
            getAuthorName(post)

          const authorAvatar =
            getAuthorAvatar(post)

          const averageRating =
            getAverageRating(postRating)

          const ratingCount =
            getRatingCount(postRating)

          const myRating =
            Number(
              currentRating.rating || 0
            )

          return (
            <article
              key={post.id}
              className="community-post"
            >

              {/* =================================================
                  POST HEADER
              ================================================= */}

              <div className="community-post-header">
                <div className="community-author">

                  {authorAvatar ? (
                    <img
                      className="community-author-avatar"
                      src={authorAvatar}
                      alt={authorName}
                    />
                  ) : (
                    <div className="community-author-avatar community-author-avatar-placeholder">
                      {authorName
                        .charAt(0)
                        .toUpperCase()}
                    </div>
                  )}

                  <div className="community-author-info">
                    <strong>
                      {authorName}
                    </strong>

                    <span>
                      Photography Expert

                      {post.created_at && (
                        <>
                          {' • '}
                          {formatDate(
                            post.created_at
                          )}
                        </>
                      )}
                    </span>
                  </div>
                </div>

                {post.type && (
                  <span className="community-post-type">
                    {String(
                      post.type
                    ).replaceAll(
                      '_',
                      ' '
                    )}
                  </span>
                )}
              </div>

              {/* =================================================
                  POST CONTENT
              ================================================= */}

              <div className="community-post-content">
                {post.title && (
                  <h2>
                    {post.title}
                  </h2>
                )}

                <p>
                  {post.content}
                </p>
              </div>

              {/* =================================================
                  POST IMAGES
              ================================================= */}

              {postImages.length > 0 && (
                <div
                  className={`community-post-images ${
                    postImages.length === 1
                      ? 'one-image'
                      : postImages.length === 2
                      ? 'two-images'
                      : 'many-images'
                  }`}
                >
                  {postImages.map(
                    (image) => (
                      <img
                        key={
                          image.id ||
                          image.image_path
                        }
                        src={getPostImageUrl(
                          image.image_path
                        )}
                        alt={
                          post.title ||
                          'Community post'
                        }
                        loading="lazy"
                      />
                    )
                  )}
                </div>
              )}

              {/* =================================================
                  PUBLIC RATING
              ================================================= */}

              <div className="community-rating-summary">

                <div className="community-average-rating">

                  <span className="community-rating-number">
                    {averageRating.toFixed(1)}
                  </span>

                  {renderStars(
                    averageRating
                  )}

                  <span className="community-rating-count">
                    {ratingCount}{' '}
                    đánh giá
                  </span>

                </div>

              </div>

              {/* =================================================
                  COMMENTS
              ================================================= */}

              <div className="community-comments-section">

                <div className="community-section-title">
                  <h3>
                    Bình luận
                  </h3>

                  <span>
                    {postComments.length}
                  </span>
                </div>

                {postComments.length === 0 ? (
                  <div className="community-no-comments">
                    Chưa có bình luận.
                    Hãy là người đầu tiên
                    chia sẻ suy nghĩ của
                    bạn.
                  </div>
                ) : (
                  <div className="community-comments-list">

                    {postComments.map(
                      (comment) => {
                        

                        const commentName =
                          comment.author_name ||
                          comment.author_username ||
                          comment.user?.full_name ||
                          comment.user?.username ||
                          comment.username ||
                          'User'

                        const commentAvatar =
                         
                          comment.user?.avatar_url ||
                          comment.author_avatar_url ||
                          comment.user?.avatar ||
                          comment.avatar_url ||
                          null

                        return (
                          <div
                            key={
                              comment.id
                            }
                            className="community-comment"
                          >

                            {commentAvatar ? (
                              <img
                                className="community-comment-avatar"
                                src={
                                  commentAvatar
                                }
                                alt={
                                  commentName
                                }
                              />
                            ) : (
                              <div className="community-comment-avatar community-comment-avatar-placeholder">
                                {commentName
                                  .charAt(
                                    0
                                  )
                                  .toUpperCase()}
                              </div>
                            )}

                            <div className="community-comment-body">

                              <div className="community-comment-bubble">
                                <strong>
                                  {
                                    commentName
                                  }
                                </strong>

                                <p>
                                  {
                                    comment.content
                                  }
                                </p>
                              </div>

                              {comment.created_at && (
                                <small>
                                  {formatDate(
                                    comment.created_at
                                  )}
                                </small>
                              )}

                            </div>

                          </div>
                        )
                      }
                    )}

                  </div>
                )}

                {/* COMMENT FORM */}

                <div className="community-comment-form">

                  <input
                    type="text"
                    placeholder="Viết bình luận..."
                    value={
                      commentInputs[
                        post.id
                      ] || ''
                    }
                    onChange={(e) =>
                      handleCommentChange(
                        post.id,
                        e.target.value
                      )
                    }
                    onKeyDown={(e) => {
                      if (
                        e.key ===
                        'Enter'
                      ) {
                        handleSubmitComment(
                          post.id
                        )
                      }
                    }}
                  />

                  <button
                    onClick={() =>
                      handleSubmitComment(
                        post.id
                      )
                    }
                    disabled={
                      commentLoading[
                        post.id
                      ]
                    }
                  >
                    {commentLoading[
                      post.id
                    ]
                      ? 'Đang gửi...'
                      : 'Gửi'}
                  </button>

                </div>
              </div>

              {/* =================================================
                  MY RATING
              ================================================= */}

              <div className="community-my-rating">

                <div className="community-section-title">

                  <div>
                    <h3>
                      Đánh giá của bạn
                    </h3>

                    <p>
                      Chỉ bạn nhìn thấy
                      số sao mình đã
                      đánh giá.
                    </p>
                  </div>

                  {myRating > 0 && (
                    <span className="community-my-rating-value">
                      {myRating}/5
                    </span>
                  )}

                </div>

                {/* STAR PICKER */}

                <div className="community-rating-picker">

                  {[1, 2, 3, 4, 5].map(
                    (star) => (
                      <button
                        key={star}
                        type="button"
                        className={
                          myRating >= star
                            ? 'selected'
                            : ''
                        }
                        onClick={() =>
                          handleRatingChange(
                            post.id,
                            star
                          )
                        }
                        aria-label={`${star} sao`}
                      >
                        ★
                      </button>
                    )
                  )}

                </div>

                {/* REVIEW */}

                <textarea
                  placeholder="Nhận xét về bài viết (không bắt buộc)..."
                  value={
                    currentRating.review ||
                    ''
                  }
                  onChange={(e) =>
                    handleReviewChange(
                      post.id,
                      e.target.value
                    )
                  }
                />

                {/* SUBMIT */}

                <button
                  className="community-rating-submit"
                  onClick={() =>
                    handleSubmitRating(
                      post.id
                    )
                  }
                  disabled={
                    ratingLoading[
                      post.id
                    ]
                  }
                >
                  {ratingLoading[
                    post.id
                  ]
                    ? 'Đang lưu...'
                    : myRating > 0
                    ? 'Cập nhật đánh giá'
                    : 'Gửi đánh giá'}
                </button>

              </div>

            </article>
          )
        })}

      </div>
    </div>
  )
}

export default Community