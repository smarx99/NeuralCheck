import React, { useState } from 'react';


interface HeroCardProps {
    title: string
    layers: string
    nodes: string
    actfunction: string
}

/**
 * Cards to configure networks
 */
const HeroCard: React.FC<HeroCardProps> = ({ 
  title,
  layers,
  nodes,
  actfunction,
}) => {
  const [layerCount, setLayerCount] = useState(layers);
  const [nodeCount, setNodeCount] = useState(nodes);
  const [activation, setActivation] = useState(actfunction);

  const handleLayerChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setLayerCount(e.target.value);
  };

  const handleNodeChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setNodeCount(e.target.value);
  };

  const handleActivationChange = (e: React.ChangeEvent<HTMLSelectElement>) => {
    setActivation(e.target.value);
  };

  return (
    <div className="bg-white border-4 border-gray-200 shadow-lg rounded-lg p-4 w-80 h-auto flex flex-col justify-center items-center text-center">
      <div className="flex-grow flex justify-center items-center text-center">
        <div className="font-bold text-xl text-primary mb-4">{title}</div>
      </div>
      <div className="flex-grow flex flex-col items-start w-full">
        <label className="text-lg text-primary mb-2 w-full">
          Number of hidden layers:
          <input
            type="number"
            value={layerCount}
            onChange={handleLayerChange}
            className="w-full mt-1 px-2 py-1 border rounded"
          />
        </label>
        <label className="text-lg text-primary mb-2 w-full">
          Number of nodes per layer:
          <input
            type="number"
            value={nodeCount}
            onChange={handleNodeChange}
            className="w-full mt-1 px-2 py-1 border rounded"
          />
        </label>
        <label className="text-lg text-primary w-full">
          Activation function:
          <select
            value={activation}
            onChange={handleActivationChange}
            className="w-full mt-1 px-2 py-1 border rounded"
          >
            <option value="sigmoid">Sigmoid</option>
            <option value="relu">ReLU</option>
            <option value="tanh">Tanh</option>
            <option value="leakyrelu">Leaky ReLU</option>
            <option value="softmax">Softmax</option>
          </select>
        </label>
      </div>
    </div>
  );
};

export default HeroCard
