import React from 'react';
import { render, screen, fireEvent } from '@testing-library/react';
import RegisterForm from './RegisterForm';

// Mock de fetch
global.fetch = jest.fn(() =>
  Promise.resolve({
    json: () => Promise.resolve({
      status: 'success',
      data: [{ id: 1, name: 'Inception' }]
    })
  })
);

test('renderiza correctamente el formulario', async () => {
  render(<RegisterForm />);
  
  // Verificar que los elementos básicos se renderizan
  expect(screen.getByLabelText(/Fecha y Hora de Renta/i)).toBeInTheDocument();
  expect(screen.getByLabelText(/ID de Cliente/i)).toBeInTheDocument();
  expect(screen.getByLabelText(/Película/i)).toBeInTheDocument();
});

test('envía el formulario correctamente', async () => {
  render(<RegisterForm />);

  // Completar los campos del formulario
  fireEvent.change(screen.getByLabelText(/Fecha y Hora de Renta/i), { target: { value: '2024-10-30T10:00' } });
  fireEvent.change(screen.getByLabelText(/ID de Cliente/i), { target: { value: '5' } });
  fireEvent.change(screen.getByLabelText(/Película/i), { target: { value: '1' } });

  // Simular el envío del formulario
  fireEvent.click(screen.getByText(/Registrar Renta/i));
});
