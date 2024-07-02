import React, { useState } from 'react';
import axios from 'axios';
import { useNavigate, Link } from 'react-router-dom';

const Login: React.FC = () => {
  const [password, setPassword] = useState('');
  const [username, setUsername] = useState('');
  const [error, setError] = useState<string | null>(null);
  const navigate = useNavigate();

  const handleLogin = async () => {
    try {
      const response = await axios.post('http://localhost:8003/login', { username, password });
      const token = response.data.token;


      if (token) {
        localStorage.setItem('token', token);
        localStorage.setItem("username", username);
        navigate('/app'); // Weiterleitung zur Haupt-App-Seite
      } else {
        setError('Login failed. Please try again.');
      }
    } catch (error) {
      console.error('Error during login:', error);
      setError('Login failed. Please check your login details.');
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center">
      <div className="bg-white border-gray shadow-lg rounded-lg p-8 w-full max-w-md border-4">
        <h2 className="text-2xl font-bold mb-6 text-center text-primary">Login</h2>
        {error && <p className="text-red-500 text-center mb-4">{error}</p>}
        <input
          type="text"
          placeholder="Username"
          value={username}
          onChange={e => setUsername(e.target.value)}
          className="mb-4 px-4 py-2 border rounded w-full text-center"
        />
        <input
          type="password"
          placeholder="Password"
          value={password}
          onChange={e => setPassword(e.target.value)}
          className="mb-4 px-4 py-2 border rounded w-full text-center"
        />
        <button
          onClick={handleLogin}
          className="bg-blue-500 text-white font-bold py-2 px-4 rounded w-full transition transform hover:scale-105"
        >
          Login
        </button>
        <p className="text-center mt-4">
          Don't have an account?{' '}
          <Link to="/register" className="text-blue-500 hover:underline">
            Register here
          </Link>
        </p>
      </div>
    </div>
  );
};

export default Login;