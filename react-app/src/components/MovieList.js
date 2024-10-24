import React, { useEffect, useState } from 'react';
import './MovieList.css'; // Importar los estilos

const MovieList = () => {
  const [movies, setMovies] = useState([]);

  // Asume que el id del cliente está disponible (puedes cambiar '1' por el ID real)
  const idCustomer = 49;

  useEffect(() => {
    const fetchMovies = async () => {
      try {
        const response = await fetch('http://127.0.0.1:5000/get-movies/${idCustomer}');
        const data = await response.json();
        setMovies(data.data);
      } catch (error) {
        console.error('Error fetching movies:', error);
      }
    };

    fetchMovies();
  }, []);

  return (
    <div>
      <h2>Películas Rentadas</h2>
      <ul>
        {movies.map((movie, index) => (
          <li key={index}>
            {movie.title} - Film ID: {movie.film_id}
          </li>
        ))}
      </ul>
    </div>
  );
};

export default MovieList;