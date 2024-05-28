import React, { useState } from 'react';

interface LayerConfig {
    nodes: number;
    actFunction: string;
}

interface HeroCardProps {
    title: string;
    initialLayers: number;
    initialNodes: number;
    initialActFunction: string;
}

const HeroCard: React.FC<HeroCardProps> = ({ 
  title,
  initialLayers,
  initialNodes,
  initialActFunction
}) => {
    const [layers, setLayers] = useState(initialLayers);
    const [layerConfigs, setLayerConfigs] = useState<LayerConfig[]>(
        Array(initialLayers).fill({ nodes: initialNodes, actFunction: initialActFunction })
    );

    const activationFunctions = ['sigmoid', 'relu', 'tanh', 'linear'];

    const handleLayerChange = (index: number, field: string, value: string | number) => {
        const newLayerConfigs = [...layerConfigs];
        newLayerConfigs[index] = { ...newLayerConfigs[index], [field]: value };
        setLayerConfigs(newLayerConfigs);
    };

    const handleLayersInputChange = (value: number) => {
        setLayers(value);
        const newLayerConfigs = Array(value).fill({ nodes: initialNodes, actFunction: initialActFunction });
        setLayerConfigs(newLayerConfigs);
    };

    return (
        <div className="bg-white border-gray shadow-lg rounded-lg p-6 w-96 flex flex-col border-4 justify-center items-center text-center transition transform hover:scale-105">
          <div className="font-bold text-2xl mb-4 text-primary">{title}</div>
          <div className="flex flex-col space-y-4 w-full">
            <div>
              <label className="block mb-1 text-secondary">Hidden Layers</label>
              <input 
                type="number" 
                value={layers} 
                onChange={(e) => handleLayersInputChange(Number(e.target.value))} 
                className="border rounded p-2 w-full text-center" 
                min="1"
              />
            </div>
            {layerConfigs.map((config, index) => (
              <div key={index} className="border-t pt-4 mt-4">
                <div>
                  <label className="block mb-1 text-secondary">Nodes in Layer {index + 1}</label>
                  <input 
                    type="number" 
                    value={config.nodes} 
                    onChange={(e) => handleLayerChange(index, 'nodes', Number(e.target.value))} 
                    className="border rounded p-2 w-full text-center" 
                    min="1"
                  />
                </div>
                <div>
                  <label className="block mb-1 text-secondary">Activation Function</label>
                  <select 
                    value={config.actFunction} 
                    onChange={(e) => handleLayerChange(index, 'actFunction', e.target.value)} 
                    className="border rounded p-2 w-full text-center"
                  >
                    {activationFunctions.map((func, funcIndex) => (
                      <option key={funcIndex} value={func}>{func}</option>
                    ))}
                  </select>
                </div>
              </div>
            ))}
          </div>
        </div>
    );
}

export default HeroCard;
