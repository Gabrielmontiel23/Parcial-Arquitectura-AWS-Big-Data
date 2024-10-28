import React from 'react';
import { render, screen } from '@testing-library/react';
import MovieList from './components/MovieList';

test('renderiza el componente MovieList', () => {
  // Simula una lista de películas simple
  const mockMovies = [{ title: 'Inception' }, { title: 'The Matrix' }];

  render(<MovieList movies={mockMovies} />);

  // Verifica que las películas se muestran
  expect(screen.getByText('Inception')).toBeInTheDocument();
  expect(screen.getByText('The Matrix')).toBeInTheDocument();
});
