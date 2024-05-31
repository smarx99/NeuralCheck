import React, { useRef, useState } from 'react';
import HeroCard, { HeroCardRef } from './components/HeroCard';
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
  const heroCardRefs = useRef<(HeroCardRef | null)[]>([]);
  const [results, setResults] = useState<Record<string, Result>>({});
  const [isTraining, setIsTraining] = useState<boolean>(false);

  const handleStartTraining = async () => {
    const configs = heroCardRefs.current.map(ref => ref?.getConfig());
    const dataToSend = configs.map(config => ({
      layers: config?.layersCount,
      nodes_per_layer: config?.layerConfigs.map(layer => layer.nodes),
      activation_functions: config?.layerConfigs.map(layer => layer.actFunction),
    }));

    setIsTraining(true);  // Setze den Trainingsstatus auf "true"

    try {
      const response = await axios.post('http://localhost:8001/orch', dataToSend);
      console.log('Response:', response.data); // Logge die gesamte Response
      setResults(response.data.results || {});
    } catch (error) {
      console.error('Error sending configuration:', error);
    } finally {
      setIsTraining(false);  // Setze den Trainingsstatus auf "false"
    }
  };

  return (
    <div className="relative min-h-screen">
      <div className="absolute top-4 left-4 text-sm text-gray-700">
        <label htmlFor="dataset-select" className="mr-2">Used dataset:</label>
        <select id="dataset-select" className="border rounded p-1">
          <option value="breast_cancer.csv">breast_cancer.csv</option>
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

          />
        ))}
      </div>
      <div className='flex justify-center mb-8'>
        <button
          onClick={handleStartTraining}
          className='bg-white border-gray border-4 shadow-lg rounded-lg mt-8 font-medium text-3xl px-8 py-2 transition transform hover:scale-105'
        >
          Start Training!
        </button>
      </div>
    </div>
  );
};

export default App;
