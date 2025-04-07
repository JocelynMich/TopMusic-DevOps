import React, { useState, useContext } from 'react';
import UserContext from './auth';
import '../styles/spotify.css';


const LoginForm = () => {
  const { loginUser } = useContext(UserContext);
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [role, setRole] = useState('user');
  const [isRegister, setIsRegister] = useState(false);
  const [message, setMessage] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();
    const url = isRegister
      ? 'http://127.0.0.1:8000/register/'
      : 'http://127.0.0.1:8000/login/';

    try {
      const response = await fetch(url, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(
          isRegister ? { username, password, role } : { username, password }
        ),
      });
      const data = await response.json();

      if (response.ok) {
        if (isRegister) {
          setMessage('Registro exitoso. Ahora inicia sesión.');
          setIsRegister(false);
        } else {
          loginUser(data.access_token, data.role);
          setMessage('Inicio de sesión exitoso.');
        }
      } else {
        setMessage(data.detail || 'Error en la solicitud');
      }
    } catch (err) {
      setMessage('Error de red');
    }
  };

  return (
    <div className="spotify-container full-height">
      <div className="banner-contentS no-shadow">
        <h1 className="title-white">{isRegister ? 'Crear cuenta' : 'Iniciar Sesión'}</h1>
        {message && <p className="error-message">{message}</p>}
        <form
          onSubmit={handleSubmit}
          className="login-form-style"
        >
          <input
            className="text-input"
            type="text"
            placeholder="Username"
            value={username}
            onChange={(e) => setUsername(e.target.value)}
            required
          />
          <input
            className="text-input"
            type="password"
            placeholder="Password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            required
          />
          {isRegister && (
            <select className="text-input" value={role} onChange={(e) => setRole(e.target.value)}>
              <option value="user">Usuario</option>
              <option value="admin">Administrador</option>
            </select>
          )}
          <button className="green-button" type="submit">
            {isRegister ? 'Registrar' : 'Ingresar'}
          </button>
        </form>
        <button className="green-button outline" onClick={() => setIsRegister(!isRegister)}>
          {isRegister ? 'Ya tengo cuenta' : 'Crear Cuenta'}
        </button>
      </div>
    </div>
  );
};

export default LoginForm;