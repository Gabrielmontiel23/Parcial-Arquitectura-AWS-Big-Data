import React from 'react';
import { render, screen, fireEvent } from '@testing-library/react';
import App from './App';

test('renderiza el componente App', () => {
  render(<App />);
  
  // Verifica que el título se muestra
  expect(screen.getByText('Gestión de Rentas')).toBeInTheDocument();

  // Verifica el botón de alternar
  const toggleButton = screen.getByRole('button');
  expect(toggleButton).toBeInTheDocument();

  // Alterna a la lista de películas
  fireEvent.click(toggleButton);
  expect(screen.getByText('Registrar Una Nueva Renta')).toBeInTheDocument();
});
