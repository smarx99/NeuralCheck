import React, { useRef, useState, useEffect } from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate, useLocation, useNavigate } from 'react-router-dom';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faSignOutAlt } from '@fortawesome/free-solid-svg-icons';
import HeroCard, { HeroCardRef } from './components/HeroCard';
import Login from './components/Login';
import Register from './components/Register';
import Sidebar from './components/Sidebar';
import Account from './components/Account';
import PrivateRoute from './components/PrivateRoute';
import axios from 'axios';

const initialHeroItems = [
  {
    title: 'Neural Network 1',
    layersCount: 0,
    nodesCount: 0,
    activationFunction: '',
  },
  {
    title: 'Neural Network 2',
    layersCount: 0,
    nodesCount: 0,
    activationFunction: '',
  },
  {
    title: 'Neural Network 3',
    layersCount: 0,
    nodesCount: 0,
    activationFunction: '',
  },
];

interface Result {
  result: number;
}

const App: React.FC = () => {
  const location = useLocation();
  const navigate = useNavigate();
  const heroCardRefs = useRef<(HeroCardRef | null)[]>([]);
  const [results, setResults] = useState<Record<string, Result>>({});
  const [isTraining, setIsTraining] = useState<boolean>(false);
  const [isSidebarOpen, setIsSidebarOpen] = useState<boolean>(false);
  const [datasets, setDatasets] = useState<string[]>([]);
  const fileInputRef = useRef<HTMLInputElement>(null);

  useEffect(() => {
    const fetchDatasets = async () => {
      const username = localStorage.getItem('username');
      const token = localStorage.getItem('token');
      if (username && token) {
        try {
          const response = await axios.get(`http://localhost:8004/datasets/${username}`, {
            headers: {
              'Authorization': `Bearer ${token}`
            }
          });
          if (response.status === 200) {
            setDatasets(response.data[0].datasets.map((dataset: any) => dataset.dataset_name));
          }
        } catch (error) {
          console.error('Error fetching datasets:', error);
        }
      }
    };
    fetchDatasets();
  }, []);

  const handleStartTraining = async () => {
    const configs = heroCardRefs.current.map(ref => ref?.getConfig());
    const selectElement = document.getElementById("dataset-select") as HTMLSelectElement | null;
    const selectedIndex = selectElement?.selectedIndex ?? 0;
    const selectedDataset = datasets[selectedIndex];

    const dataToSend = {
      dataset_name: selectedDataset,
      configurations: configs.map(config => ({
        layers: config?.layersCount,
        nodes_per_layer: config?.layerConfigs.map(layer => layer.nodes),
        activation_functions: config?.layerConfigs.map(layer => layer.actFunction),
      }))
    };

    setIsTraining(true);

    try {
      const token = localStorage.getItem('token');
      const response = await axios.post('http://localhost:8001/orch', dataToSend, {
        headers: {
          'Authorization': `Bearer ${token}`
        }
      });
      console.log('Response:', response.data);
      setResults(response.data.results || {});
    } catch (error) {
      console.error('Error sending configuration:', error);
    } finally {
      setIsTraining(false);
    }
  };

  const toggleSidebar = () => {
    setIsSidebarOpen(!isSidebarOpen);
  };

  const handleLogout = () => {
    navigate('/login');
    window.location.reload();
  };

  const handleUploadDataset = async (event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0];
    if (file) {
      const formData = new FormData();
      formData.append('file', file);
      // Benutzernamen aus dem localStorage abrufen
      const username = localStorage.getItem('username');
      if (username) {
        formData.append('username', username);

        try {
          const token = localStorage.getItem('token');
          const response = await axios.post('http://localhost:8004/upload_dataset', formData, {
            headers: {
              'Authorization': `Bearer ${token}`,
              'Content-Type': 'multipart/form-data'
            }
          });

          console.log('Upload Response:', response.data);

          if (response.status === 200) {
            setDatasets(prevDatasets => [...prevDatasets, file.name]);

            if (fileInputRef.current) {
              fileInputRef.current.value = '';
            }
            return { success: true };
          } else {
            return { success: false, message: 'Error uploading dataset' };
          }
        } catch (error) {
          return { success: false, message: 'Error uploading dataset' };
        }
      } else {
        return { success: false, message: 'No username found in localStorage' };
      }
    }
    return { success: false, message: 'No file selected' };
  };

  const getBestResultIndex = () => {
    let bestIndex = -1;
    let bestResult = -Infinity;

    Object.keys(results).forEach((key, index) => {
      if (results[key].result > bestResult) {
        bestResult = results[key].result;
        bestIndex = index;
      }
    });

    return bestIndex;
  };

  const bestResultIndex = getBestResultIndex();

  return (
    <div className={`flex-1 transition-all duration-300 ${location.pathname === '/app' && isSidebarOpen ? 'mr-4': 'ml-4'}`}>
      {location.pathname === '/app' && (
        <button
          onClick={handleLogout}
          className="absolute top-4 right-4 text-gray-700 hover:text-gray-900"
        >
          <FontAwesomeIcon icon={faSignOutAlt} size="2x" />
        </button>
      )}
      {(location.pathname === '/app' || location.pathname === '/account') && (
        <Sidebar 
          isOpen={isSidebarOpen} 
          toggleSidebar={toggleSidebar} 
          datasets={datasets} 
          onUploadDataset={handleUploadDataset}
          fileInputRef={fileInputRef}
        />
      )}
      <div className={`flex-1 transition-all duration-300 ${location.pathname === '/app' && isSidebarOpen ? 'ml-64' : 'ml-16'}`}>
        <Routes>
          <Route path="/register" element={<Register />} />
          <Route path="/login" element={<Login />} />  
          <Route path="/account" element={<PrivateRoute element={<Account />} />} />     
          <Route path="/app" element={<PrivateRoute element={
            <div className="relative min-h-screen">
              <div className="absolute top-4 left-4 text-sm text-gray-700">
                <label htmlFor="dataset-select" className="mr-2">Used dataset:</label>
                <select id="dataset-select" className="border rounded p-1">
                  {datasets.map((dataset, index) => (
                    <option key={index} value={dataset}>{dataset}</option>
                  ))}
                </select>
              </div>
              <p className="text-5xl w-full font-bold mt-10 mb-10 flex justify-center text-primary">
                NeuralCheck
              </p>
              <div className="flex justify-center space-x-16 mb-8">
                {initialHeroItems.map((item, index) => (
                  <HeroCard
                    key={index}
                    ref={el => heroCardRefs.current[index] = el}
                    title={item.title}
                    initialLayersCount={item.layersCount}
                    initialNodesCount={item.nodesCount}
                    initialActivationFunction={item.activationFunction}
                    result={isTraining ? 'Training in progress...' : results[`Config${index + 1}`]?.result}
                    highlight={index === bestResultIndex}  // Highlight the best card
                  />
                ))}
              </div>
              <div className='flex justify-center mb-8'>
                <button
                  onClick={handleStartTraining}
                  className='bg-white border-gray border-4 shadow-lg rounded-lg mt-8 font-medium text-3xl px-8 py-2 transition transform hover:scale-105'
                >
                  Start!
                </button>
              </div>
            </div>
          } />} />
          <Route path="*" element={<Navigate to="/login" />} />
        </Routes>
      </div>
    </div>
  );
};

const AppWithRouter: React.FC = () => (
  <Router>
    <App />
  </Router>
);

export default AppWithRouter;
