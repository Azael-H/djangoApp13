import { useQuery, useQueryClient } from '@tanstack/react-query';
import { productosAPI } from '../services/api';

export const useProductos = (params = {}) => {
  return useQuery({
    queryKey: ['productos', params],
    queryFn: () => productosAPI.getAll(params),
    select: (response) => response.data,
  });
};

export const useProducto = (id) => {
  return useQuery({
    queryKey: ['producto', id],
    queryFn: () => productosAPI.getById(id),
    select: (response) => response.data,
    enabled: !!id,
  });
};

export const usePrefetchProducto = () => {
  const queryClient = useQueryClient();

  return (id) => {
    queryClient.prefetchQuery({
      queryKey: ['producto', id],
      queryFn: () => productosAPI.getById(id),
    });
  };
};