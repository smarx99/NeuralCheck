import React, { useState } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';

const Register: React.FC = () => {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState<string | null>(null);
  const [success, setSuccess] = useState<string | null>(null);
  const navigate = useNavigate();

  const handleRegister = async () => {
    try {
      const response = await axios.post('http://localhost:8001/register', { email, password });
      
      if (response.status === 201) { // Annahme: Erfolgreiche Registrierung gibt Status 201 zurück
        setSuccess('Registrierung erfolgreich! Sie werden in Kürze weitergeleitet.');
        setTimeout(() => {
          navigate('/login'); // Weiterleitung zur Login-Seite nach erfolgreicher Registrierung
        }, 2000); // Warte 2 Sekunden, bevor weitergeleitet wird
      } else {
        setError('Registrierung fehlgeschlagen. Bitte versuchen Sie es erneut.');
      }
    } catch (error) {
      console.error('Error during registration:', error);
      setError('Registrierung fehlgeschlagen. Bitte versuchen Sie es erneut.');
    }
  };

  return (
    <div className="register-container">
      <h2>Register</h2>
      {error && <p style={{ color: 'red' }}>{error}</p>}
      {success && <p style={{ color: 'green' }}>{success}</p>}
      <input
        type="email"
        placeholder="Email"
        value={email}
        onChange={e => setEmail(e.target.value)}
      />
      <input
        type="password"
        placeholder="Password"
        value={password}
        onChange={e => setPassword(e.target.value)}
      />
      <button onClick={handleRegister}>Register</button>
    </div>
  );
};

export default Register;
