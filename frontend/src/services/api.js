import axios from 'axios';

const api = axios.create({
  baseURL: '/api',
  headers: {
    'Content-Type': 'application/json',
  },
});

export const categoriasAPI = {
  getAll: () => api.get('/categorias/'),
  getById: (id) => api.get(`/categorias/${id}/`),
  getProductos: (id) => api.get(`/categorias/${id}/productos/`),
};

export const productosAPI = {
  getAll: (params) => api.get('/productos/', { params }),
  getById: (id) => api.get(`/productos/${id}/`),
};

export const carritoAPI = {
  getCarrito: () => api.get('/carrito/'),
  addItem: (data) => api.post('/carrito/', data),
  updateCantidad: (id, cantidad) => api.put(`/carrito/${id}/actualizar_cantidad/`, { cantidad }),
  removeItem: (id) => api.delete(`/carrito/${id}/`),
  limpiar: () => api.delete('/carrito/limpiar/'),
};

export default api;