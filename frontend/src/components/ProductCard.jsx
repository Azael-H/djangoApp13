import React from 'react';
import { Link } from 'react-router-dom';
import { toast } from 'react-toastify';
import { usePrefetchProducto } from '../hooks/useProductos';
import { useCarrito } from '../hooks/useCarrito';

const ProductCard = ({ producto }) => {
  const prefetchProducto = usePrefetchProducto();
  const { addItem, isAddingItem } = useCarrito();

  const handleAddToCart = () => {
    addItem(
      { producto_id: producto.id, cantidad: 1 },
      {
        onSuccess: () => {
          toast.success(`${producto.nombre} agregado al carrito`, {
            position: "top-right",
            autoClose: 2000,
          });
        },
        onError: (error) => {
          toast.error('Error al agregar el producto', {
            position: "top-right",
            autoClose: 2000,
          });
        }
      }
    );
  };

  return (
    <div className="col-md-6 col-lg-3 mb-4">
      <div className="card h-100">
        <img
          src={producto.imagen || `https://via.placeholder.com/300x400/cccccc/666666?text=Sin+Imagen`}
          className="card-img-top"
          alt={producto.nombre}
        />

        {producto.nuevo && (
          <span className="badge bg-success position-absolute top-0 start-0 m-2">
            Nuevo
          </span>
        )}

        {producto.destacado && (
          <span
            className="badge bg-warning position-absolute top-0 start-0 m-2"
            style={{ marginTop: producto.nuevo ? '45px' : '10px' }}
          >
            <i className="fas fa-star"></i> Destacado
          </span>
        )}

        {producto.tiene_descuento && (
          <span className="badge bg-danger position-absolute top-0 end-0 m-2">
            -{producto.porcentaje_descuento}%
          </span>
        )}

        <div className="card-body d-flex flex-column">
          <span className="badge bg-info mb-2">{producto.categoria_nombre}</span>
          <h5
            className="card-title"
            onMouseEnter={() => prefetchProducto(producto.id)}
          >
            <Link
              to={`/producto/${producto.id}`}
              className="text-decoration-none text-dark"
            >
              {producto.nombre}
            </Link>
          </h5>

          {producto.autor && (
            <p className="text-muted mb-2">
              <i className="fas fa-user"></i> {producto.autor}
            </p>
          )}

          <div className="mt-auto">
            {producto.tiene_descuento ? (
              <>
                <p className="mb-1">
                  <span className="text-decoration-line-through text-muted">
                    S/. {producto.precio}
                  </span>
                </p>
                <p className="precio mb-3">S/. {producto.precio_final}</p>
              </>
            ) : (
              <p className="precio mb-3">S/. {producto.precio}</p>
            )}

            {producto.stock > 0 ? (
              <p className="text-success mb-2">
                <i className="fas fa-check-circle"></i> Stock: {producto.stock}
              </p>
            ) : (
              <p className="text-danger mb-2">
                <i className="fas fa-times-circle"></i> Agotado
              </p>
            )}

            <div className="d-grid gap-2">
              <Link
                to={`/producto/${producto.id}`}
                className="btn btn-outline-primary btn-sm"
              >
                <i className="fas fa-info-circle"></i> Ver Detalles
              </Link>
              {producto.stock > 0 ? (
                <button
                  className="btn btn-primary btn-sm"
                  onClick={handleAddToCart}
                  disabled={isAddingItem}
                >
                  {isAddingItem ? (
                    <>
                      <span className="spinner-border spinner-border-sm me-1"></span>
                      Agregando...
                    </>
                  ) : (
                    <>
                      <i className="fas fa-cart-plus"></i> Agregar
                    </>
                  )}
                </button>
              ) : (
                <button className="btn btn-secondary btn-sm" disabled>
                  <i className="fas fa-ban"></i> No Disponible
                </button>
              )}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default ProductCard;