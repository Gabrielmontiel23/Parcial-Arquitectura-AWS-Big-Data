import React, { useState, useEffect } from 'react';

const RegisterForm = () => {
    const [movies, setMovies] = useState([]);
    const [selectedFilmId, setSelectedFilmId] = useState(null);
    const [formData, setFormData] = useState({
        rental_date: '',
        customer_id: '',
        film_id: ''
    });

    // Obtener la lista de películas desde el backend
    useEffect(() => {
        fetch('http://ec2-34-236-249-156.compute-1.amazonaws.com:5000/movies')
            .then(response => response.json())
            .then(data => {
                if (data.status === 'success') {
                    setMovies(data.data); // Guardar las películas en el estado
                    console.log(data.data)
                }
            })
            .catch(error => console.error('Error al obtener las películas:', error));
    }, []);

    // Manejar el cambio en la lista desplegable (selección de película)
    const handleMovieChange = (e) => {
        const filmId = e.target.value; // Obtener el film_id seleccionado
        setSelectedFilmId(filmId);
        setFormData({ ...formData, film_id: filmId }); // Actualizar el formData
    };

    // Manejar el envío del formulario
    const handleSubmit = (e) => {
        e.preventDefault();
        // Enviar los datos al backend, incluyendo film_id
        fetch('http://ec2-34-236-249-156.compute-1.amazonaws.com:5000/add-rental', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(formData)
        })
        .then(response => response.json())
        .then(data => {
            if (data.status === 'success') {
                alert('Renta registrada con éxito');
            } else {
                alert(`Error: ${data.message}`);
            }
        })
        .catch(error => console.error('Error al enviar los datos:', error));
    };

    return (
        <form onSubmit={handleSubmit}>
            <label>
                Fecha de Renta:
                <input
                    type="date"
                    value={formData.rental_date}
                    onChange={(e) => setFormData({ ...formData, rental_date: e.target.value })}
                    required
                />
            </label>
            <br />
            <label>
                ID de Cliente:
                <input
                    type="number"
                    value={formData.customer_id}
                    onChange={(e) => setFormData({ ...formData, customer_id: e.target.value })}
                    required
                />
            </label>
            <br />
            <label>
                Película:
                <select value={selectedFilmId} onChange={handleMovieChange} required>
                    <option value="">Seleccione una película</option>
                    {movies.map(movie => (
                        <option key={movie.film_id} value={movie.film_id}>
                            {movie.title}
                        </option>
                    ))}
                </select>
            </label>
            <br />
            <button type="submit">Registrar Renta</button>
        </form>
    );
};

export default RegisterForm;
