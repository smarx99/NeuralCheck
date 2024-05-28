import React from 'react';
import HeroCard from './components/HeroCard';
import Accuracy from './components/Accuracy';

const heroItems = [
  {
    title: 'Neural Network 1',
    initialLayers: 3,
    initialNodes: 10,
    initialActFunction: 'sigmoid',
  },
  {
    title: 'Neural Network 2',
    initialLayers: 2,
    initialNodes: 20,
    initialActFunction: 'relu',
  },
  {
    title: 'Neural Network 3',
    initialLayers: 1,
    initialNodes: 5,
    initialActFunction: 'tanh',
  },
];

const accuracyItems = [
  'Accuracy: 60%',
  'Accuracy: 75%',
  'Accuracy: 85%',
];

const App: React.FC = () => {
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
        {heroItems.map((item, index) => (
          <HeroCard
            key={index}
            title={item.title}
            initialLayers={item.initialLayers}
            initialNodes={item.initialNodes}
            initialActFunction={item.initialActFunction}
          />
        ))}
      </div>
      <div className='flex justify-center mb-8'>
        <button className='rounded-xl border border-primary mt-8 bg-primary text-white font-medium text-3xl px-8 py-2 transition transform hover:scale-105'>
          Start Training!
        </button>
      </div>
      <div className="flex justify-center space-x-16">
        {accuracyItems.map((accuracy, index) => (
          <Accuracy key={index} accuracy={accuracy} />
        ))}
      </div>
    </div>
  );
};

export default App;
