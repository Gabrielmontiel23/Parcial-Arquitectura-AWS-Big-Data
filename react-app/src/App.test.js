import React from 'react';
import { render, screen, fireEvent } from '@testing-library/react';
import App from './App';

// Mock de fetch
global.fetch = jest.fn(() =>
  Promise.resolve({
    json: () => Promise.resolve({
      status: 'success',
      data: [{ title: 'Inception', customerId: 5 }]
    })
  })
);

test('renderiza correctamente la caja de nombres y el botón para ver películas', () => {
  render(<App />);

  // Verificar que se renderiza el encabezado principal
  expect(screen.getByText('Gestión de Rentas')).toBeInTheDocument();

  // Verificar que se renderiza el botón para alternar la vista
  const toggleButton = screen.getByText('Ver Peliculas por Usuario');
  expect(toggleButton).toBeInTheDocument();

  // Simular clic para cambiar la vista
  fireEvent.click(toggleButton);
  expect(screen.getByText('Registrar Una Nueva Renta')).toBeInTheDocument();
});
