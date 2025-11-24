import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { useCarrito } from '../hooks/useCarrito';

const CarritoItem = ({ item, onUpdateCantidad, onRemove, isUpdating }) => {
  const [cantidad, setCantidad] = useState(item.cantidad);

  useEffect(() => {
    console.log('CarritoItem recibido:', item);
    setCantidad(item.cantidad);
  }, [item]);

  const handleIncrement = () => {
    if (cantidad < item.producto_stock) {
      const newCantidad = cantidad + 1;
      setCantidad(newCantidad);
      console.log('Incrementando - item.id:', item.id, 'nueva cantidad:', newCantidad);
      onUpdateCantidad(item.id, newCantidad);
    }
  };

  const handleDecrement = () => {
    if (cantidad > 1) {
      const newCantidad = cantidad - 1;
      setCantidad(newCantidad);
      console.log('Decrementando - item.id:', item.id, 'nueva cantidad:', newCantidad);
      onUpdateCantidad(item.id, newCantidad);
    }
  };

  return (
    <div className="card mb-3">
      <div className="row g-0">
        <div className="col-md-3">
          <img
            src={item.producto_imagen || `https://via.placeholder.com/200x200?text=${encodeURIComponent(item.producto_nombre)}`}
            className="img-fluid rounded-start"
            alt={item.producto_nombre}
            style={{ height: '200px', objectFit: 'cover' }}
          />
        </div>
        <div className="col-md-9">
          <div className="card-body">
            <div className="d-flex justify-content-between align-items-start">
              <div>
                <h5 className="card-title">{item.producto_nombre}</h5>
                <small className="text-muted">ID: {item.id}</small>
              </div>
              <button
                className="btn btn-sm btn-danger"
                onClick={() => onRemove(item.id)}
                disabled={isUpdating}
              >
                <i className="fas fa-trash"></i>
              </button>
            </div>

            <p className="card-text">
              <strong>Precio unitario:</strong> S/. {item.producto_precio}
            </p>

            <p className="text-muted small">
              <i className="fas fa-box"></i> Stock disponible: {item.producto_stock}
            </p>

            <div className="d-flex align-items-center gap-2 mb-3">
              <div className="input-group" style={{ width: '180px' }}>
                <button
                  className="btn btn-outline-secondary"
                  type="button"
                  onClick={handleDecrement}
                  disabled={isUpdating || cantidad <= 1}
                >
                  <i className="fas fa-minus"></i>
                </button>
                <input
                  type="number"
                  className="form-control text-center"
                  value={cantidad}
                  readOnly
                />
                <button
                  className="btn btn-outline-secondary"
                  type="button"
                  onClick={handleIncrement}
                  disabled={isUpdating || cantidad >= item.producto_stock}
                >
                  <i className="fas fa-plus"></i>
                </button>
              </div>
              {isUpdating && (
                <div className="spinner-border spinner-border-sm text-primary" role="status">
                  <span className="visually-hidden">Actualizando...</span>
                </div>
              )}
            </div>

            <p className="mt-3 mb-0">
              <strong>Subtotal:</strong>{' '}
              <span className="precio" style={{ fontSize: '1.3rem' }}>
                S/. {item.subtotal}
              </span>
            </p>
          </div>
        </div>
      </div>
    </div>
  );
};

const Carrito = () => {
  const { carrito, isLoading, updateCantidad, removeItem, isUpdating, isRemoving } = useCarrito();

  console.log('Carrito completo:', carrito);
  console.log('Items:', carrito?.items);

  if (isLoading) {
    return (
      <div className="container mt-5 text-center">
        <div className="spinner-border text-primary" role="status">
          <span className="visually-hidden">Cargando...</span>
        </div>
      </div>
    );
  }

  const items = carrito?.items || [];
  const total = carrito?.total || 0;

  if (items.length === 0) {
    return (
      <div className="container my-4">
        <div className="row">
          <div className="col-12">
            <h1 className="mb-4">
              <i className="fas fa-shopping-cart"></i> Mi Carrito de Compras
            </h1>
          </div>
        </div>
        <div className="row">
          <div className="col-12">
            <div className="alert alert-info text-center py-5">
              <i className="fas fa-shopping-cart fa-3x mb-3"></i>
              <h3>Tu carrito está vacío</h3>
              <p>¡Agrega algunos productos para comenzar!</p>
              <Link to="/" className="btn btn-primary mt-3">
                <i className="fas fa-book"></i> Explorar Productos
              </Link>
            </div>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="container my-4">
      <div className="row">
        <div className="col-12">
          <h1 className="mb-4">
            <i className="fas fa-shopping-cart"></i> Mi Carrito de Compras
          </h1>
        </div>
      </div>

      <div className="row">
        <div className="col-md-8">
          {items.map((item) => (
            <CarritoItem
              key={item.id}
              item={item}
              onUpdateCantidad={updateCantidad}
              onRemove={removeItem}
              isUpdating={isUpdating || isRemoving}
            />
          ))}
        </div>

        <div className="col-md-4">
          <div className="card sticky-top" style={{ top: '20px' }}>
            <div className="card-header bg-primary text-white">
              <h5 className="mb-0">Resumen del Pedido</h5>
            </div>
            <div className="card-body">
              <div className="d-flex justify-content-between mb-2">
                <span>Productos:</span>
                <span>{items.length}</span>
              </div>
              <div className="d-flex justify-content-between mb-2">
                <span>Subtotal:</span>
                <span>S/. {total}</span>
              </div>
              <div className="d-flex justify-content-between mb-2">
                <span>Envío:</span>
                <span className="text-success">Gratis</span>
              </div>
              <hr />
              <div className="d-flex justify-content-between mb-3">
                <strong>Total:</strong>
                <strong className="precio">S/. {total}</strong>
              </div>

              <div className="alert alert-info">
                <i className="fas fa-truck"></i>{' '}
                <small>Envío gratis en todas las compras</small>
              </div>

              <div className="d-grid gap-2">
                <button className="btn btn-success btn-lg" disabled>
                  <i className="fas fa-lock"></i> Proceder al Pago
                  <small className="d-block">(Próximamente)</small>
                </button>
                <Link to="/" className="btn btn-outline-primary">
                  <i className="fas fa-arrow-left"></i> Seguir Comprando
                </Link>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Carrito;