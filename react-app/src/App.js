import React from 'react';
import RegisterForm from './components/RegisterForm';
import UserList from './components/UserList';

function App() {
  const [showUsers, setShowUsers] = React.useState(false);

  return (
    <div className="App">
      {showUsers ? <UserList /> : <RegisterForm />}
      <button onClick={() => setShowUsers(!showUsers)}>
        {showUsers ? 'Registrar Nuevo Usuario' : 'Ver Usuarios Registrados'}
      </button>
    </div>
  );
}

export default App;
