import React, { useEffect, useState, useRef } from 'react';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';
import { Link } from 'react-router-dom';
import Sidebar from './Sidebar'; 

interface UserData {
  username: string;
  first_name: string;
  last_name: string;
}

const Account: React.FC = () => {
  const [userData, setUserData] = useState<UserData | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [isSidebarOpen, setSidebarOpen] = useState(false); // Sidebar Zustand
  const navigate = useNavigate();
  const fileInputRef = useRef<HTMLInputElement>(null);

  useEffect(() => {
    const fetchUserData = async () => {
      try {
        const token = localStorage.getItem('token');
        if (!token) {
          setError('No token found');
          return;
        }

        const response = await axios.get('http://localhost:8003/user', {
          headers: {
            Authorization: token
          }
        });

        setUserData(response.data);
      } catch (err) {
        console.error('Error fetching user data:', err);
        setError('Failed to fetch user data');
      }
    };

    fetchUserData();
  }, []);

  const handleLogout = () => {
    localStorage.removeItem('token');
    navigate('/login');
  };

  const toggleSidebar = () => {
    setSidebarOpen(!isSidebarOpen);
  };

  const handleUploadDataset = (event: React.ChangeEvent<HTMLInputElement>) => {

  };

  if (error) {
    return <div>Error: {error}</div>;
  }

  if (!userData) {
    return <div>Loading...</div>;
  }

  return (
    <div className="flex">
      <Sidebar
        isOpen={isSidebarOpen}
        toggleSidebar={toggleSidebar}
        datasets={[]} // Ihre Datensätze hier übergeben
        onUploadDataset={handleUploadDataset}
        fileInputRef={fileInputRef}
      />
      <div className={`flex-1 transition-all duration-300 ${isSidebarOpen ? 'ml-60' : 'ml-16'}`}>
        <div className="min-h-screen flex items-center justify-center">
          <div className="bg-white border-gray shadow-lg rounded-lg p-8 w-full max-w-md border-4">
            <h2 className="text-2xl font-bold mb-6 text-center text-primary">Account Information</h2>
            <p className="mb-4">
              <strong className="font-bold">Username:</strong> {userData.username}
            </p>
            <p className="mb-4">
              <strong className="font-bold">First Name:</strong> {userData.first_name}
            </p>
            <p className="mb-4">
              <strong className="font-bold">Last Name:</strong> {userData.last_name}
            </p>
            <button
              onClick={handleLogout}
              className="bg-red-500 text-white font-bold py-2 px-4 rounded w-full transition transform hover:scale-105"
            >
              Logout
            </button>
            <p className="text-center mt-4">
              Want to change your account?{' '}
              <Link to="/edit-account" className="text-blue-500 hover:underline">
                Edit here
              </Link>
            </p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Account;
