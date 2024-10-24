import React, { useState } from 'react';
import './MovieList.css'; // Importar los estilos

const MovieList = () => {
  const [movies, setMovies] = useState([]);
  const [idCustomer, setIdCustomer] = useState('');
  const [errorMessage, setErrorMessage] = useState('');

  const fetchMovies = async () => {
    if (!idCustomer) {
      setErrorMessage('Por favor ingresa un ID.');
      return;
    }

    try {
      const response = await fetch(`http://ec2-52-203-160-255.compute-1.amazonaws.com:5000/get-movies/${idCustomer}`);
      if (!response.ok) {
        throw new Error('Error en la respuesta del servidor');
      }
      const data = await response.json();
      setMovies(data.data); // Asignar la lista de películas desde el campo 'data'
      setErrorMessage(''); // Limpiar mensaje de error
    } catch (error) {
      console.error('Error fetching movies:', error);
      setErrorMessage('Hubo un problema al obtener las películas.');
    }
  };

  const handleInputChange = (event) => {
    setIdCustomer(event.target.value);
  };

  const handleSearch = () => {
    fetchMovies();
  };

  return (
    <div>
      <h2>Películas Rentadas</h2>
      <div>
        <input
          type="text"
          value={idCustomer}
          onChange={handleInputChange}
          placeholder="Ingresa el ID del cliente"
        />
        <button onClick={handleSearch}>Buscar</button>
      </div>
      {errorMessage && <p className="error">{errorMessage}</p>}
      <div className="movie-list">
        {movies.map((movie, index) => (
          <div className="movie-item" key={index}>
            <div className="movie-title">{movie.title}</div>
            <div className="movie-id">Film ID: {movie.film_id}</div>
            <div className="rental-date">FA: {movie.rental_date}</div>
          </div>
        ))}
      </div>
    </div>
  );
};

export default MovieList;
