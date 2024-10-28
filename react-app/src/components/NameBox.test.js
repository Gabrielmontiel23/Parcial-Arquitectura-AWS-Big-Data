import React from 'react';
import { render, screen } from '@testing-library/react';
import NameBox from './components/NameBox';

test('renderiza el componente NameBox', () => {
  render(<NameBox />);
  
  // Verifica que el título se muestra
  expect(screen.getByText(/nombre del usuario/i)).toBeInTheDocument();
});
