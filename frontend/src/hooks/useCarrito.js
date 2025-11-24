import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { carritoAPI } from '../services/api';

export const useCarrito = () => {
  const queryClient = useQueryClient();

  const { data: carrito, isLoading } = useQuery({
    queryKey: ['carrito'],
    queryFn: carritoAPI.getCarrito,
    select: (response) => response.data,
  });

  const addItemMutation = useMutation({
    mutationFn: carritoAPI.addItem,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['carrito'] });
    },
  });

  const updateCantidadMutation = useMutation({
    mutationFn: ({ id, cantidad }) => carritoAPI.updateCantidad(id, cantidad),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['carrito'] });
    },
  });

  const removeItemMutation = useMutation({
    mutationFn: carritoAPI.removeItem,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['carrito'] });
    },
  });

  const limpiarMutation = useMutation({
    mutationFn: carritoAPI.limpiar,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['carrito'] });
    },
  });

  return {
    carrito,
    isLoading,
    addItem: (data, options) => addItemMutation.mutate(data, options),
    updateCantidad: (id, cantidad) => updateCantidadMutation.mutate({ id, cantidad }),
    removeItem: (id) => removeItemMutation.mutate(id),
    limpiar: () => limpiarMutation.mutate(),
    isAddingItem: addItemMutation.isPending,
    isUpdating: updateCantidadMutation.isPending,
    isRemoving: removeItemMutation.isPending,
  };
};