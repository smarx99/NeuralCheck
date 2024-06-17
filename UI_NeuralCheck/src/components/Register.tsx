import React, { useState } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';

const Register: React.FC = () => {
  const [password, setPassword] = useState('');
  const [username, setUsername] = useState('');
  const [firstName, setFirstName] = useState('');
  const [lastName, setLastName] = useState('');
  const [error, setError] = useState<string | null>(null);
  const [message, setMessage] = useState('')
  const navigate = useNavigate();

  const handleRegistration = async () => {
    try {
      const response = await axios.post('http://localhost:8003/register', { username, first_name: firstName, last_name: lastName, password });
      if (response.status === 201) {
        setMessage("Registration successful! You will be redirected shortly.");
        setTimeout(() => {
          navigate('/login'); // Weiterleitung zur Login-Seite nach erfolgreicher Registrierung
        }, 2000); // Warte 2 Sekunden, bevor weitergeleitet wird
      } else {
        setMessage('')
        setError('Registration failed. Please try again.');
      }
    } catch (error) {
      console.error('Error during registration:', error);
      setError('Registration failed. Please check your login details.');
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center">
      <div className="bg-white border-gray shadow-lg rounded-lg p-8 w-full max-w-md border-4">
        <h2 className="text-2xl font-bold mb-6 text-center">Registration</h2>
        {error && <p className="text-red-500 mb-4">{error}</p>}
        {message && <p className="text-green-500 mb-4">{message}</p>}
        <div className="space-y-4">
          <input
            type="text"
            placeholder="First Name"
            value={firstName}
            onChange={e => setFirstName(e.target.value)}
            className="w-full px-4 py-2 border rounded focus:outline-none focus:ring-2 focus:ring-blue-500"
          />
          <input
            type="text"
            placeholder="Last Name"
            value={lastName}
            onChange={e => setLastName(e.target.value)}
            className="w-full px-4 py-2 border rounded focus:outline-none focus:ring-2 focus:ring-blue-500"
          />
          <input
            type="text"
            placeholder="Username"
            value={username}
            onChange={e => setUsername(e.target.value)}
            className="w-full px-4 py-2 border rounded focus:outline-none focus:ring-2 focus:ring-blue-500"
          />
          <input
            type="password"
            placeholder="Password"
            value={password}
            onChange={e => setPassword(e.target.value)}
            className="w-full px-4 py-2 border rounded focus:outline-none focus:ring-2 focus:ring-blue-500"
          />
          <button
            onClick={handleRegistration}
            className="w-full bg-blue-500 text-white py-2 rounded hover:bg-blue-600 transition duration-300"
          >
            Register
          </button>
        </div>
      </div>
    </div>
  );
};

export default Register;
