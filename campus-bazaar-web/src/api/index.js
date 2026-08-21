import request from '../utils/request'

export const userApi = {
  register: (data) => request.post('/users/register', data),
  login: (data) => request.post('/users/login', data),
  logout: () => request.post('/users/logout'),
  getMe: () => request.get('/users/me'),
  updateMe: (data) => request.put('/users/me', data),
  getUserById: (id) => request.get(`/users/${id}`),
  getMyFavorites: () => request.get('/users/me/favorites')
}

export const itemApi = {
  getList: (params) => request.get('/items', { params }),
  getDetail: (id) => request.get(`/items/${id}`),
  publish: (data) => request.post('/items', data),
  update: (id, data) => request.put(`/items/${id}`, data),
  takeDown: (id) => request.delete(`/items/${id}`),
  addFavorite: (id) => request.post(`/items/${id}/favorite`),
  removeFavorite: (id) => request.delete(`/items/${id}/favorite`),
  getBySeller: (sellerId) => request.get(`/items/seller/${sellerId}`),
  getBySellerOnSale: (sellerId) => request.get(`/items/seller/${sellerId}/onsale`)
}

export const categoryApi = {
  getAll: () => request.get('/categories')
}

export const orderApi = {
  submit: (data) => request.post('/orders', data),
  getMyBuyOrders: () => request.get('/orders/buy'),
  getMySellOrders: () => request.get('/orders/sell'),
  getByItem: (itemId) => request.get(`/orders/item/${itemId}`),
  confirm: (id) => request.put(`/orders/${id}/confirm`),
  finish: (id) => request.put(`/orders/${id}/finish`),
  cancel: (id) => request.put(`/orders/${id}/cancel`)
}

export const adminApi = {
  listUsers: (page, size) => request.get('/admin/users', { params: { page, size } }),
  updateUserStatus: (id, status) => request.put(`/admin/users/${id}/status`, { status }),
  listItems: (page, size, status, keyword) => request.get('/admin/items', { params: { page, size, status, keyword } }),
  updateItemStatus: (id, status) => request.put(`/admin/items/${id}/status`, { status })
}

export const commentApi = {
  listByItem: (itemId) => request.get(`/comments/item/${itemId}`),
  add: (data) => request.post('/comments', data),
  reply: (id, data) => request.post(`/comments/${id}/reply`, data)
}

export const reviewApi = {
  getByItem: (itemId) => request.get(`/reviews/item/${itemId}`),
  checkCanReview: (orderId) => request.get(`/reviews/check/${orderId}`),
  create: (data) => request.post('/reviews', data)
}
