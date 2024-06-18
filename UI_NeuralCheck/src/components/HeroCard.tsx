import { useState, forwardRef, useImperativeHandle } from 'react';

interface LayerConfig {
  nodes: number;
  actFunction: string;
}

export interface HeroCardRef {
  getConfig: () => { layersCount: number; layerConfigs: LayerConfig[] };
}

interface HeroCardProps {
  title: string;
  initialLayersCount: number;
  initialNodesCount: number;
  initialActivationFunction: string;
  result?: string | number;
}

const HeroCard = forwardRef<HeroCardRef, HeroCardProps>(({
  title,
  initialLayersCount,
  initialNodesCount,
  initialActivationFunction,
  result
}, ref) => {
  const maxLayers = 20;
  const maxNodes = 50;

  const [layers, setLayers] = useState(Math.min(initialLayersCount || 1, maxLayers));
  const [layerConfigs, setLayerConfigs] = useState<LayerConfig[]>(
    Array(Math.min(initialLayersCount || 1, maxLayers)).fill({ nodes: Math.min(initialNodesCount || 1, maxNodes), actFunction: initialActivationFunction || 'sigmoid' })
  );

  const activationFunctions = ['sigmoid', 'relu', 'tanh', 'linear'];

  const handleLayerChange = (index: number, field: string, value: string | number) => {
    const newLayerConfigs = [...layerConfigs];
    newLayerConfigs[index] = { ...newLayerConfigs[index], [field]: value };
    setLayerConfigs(newLayerConfigs);
  };

  const handleLayersInputChange = (value: number) => {
    const newValue = Math.min(value, maxLayers);
    setLayers(newValue);
    const newLayerConfigs = Array(newValue).fill({ nodes: Math.min(initialNodesCount || 1, maxNodes), actFunction: initialActivationFunction || 'sigmoid' });
    setLayerConfigs(newLayerConfigs);
  };

  useImperativeHandle(ref, () => ({
    getConfig: () => ({
      layersCount: layers,
      layerConfigs: layerConfigs,
    }),
  }));

  // Formatieren des Result-Werts als Prozentzahl
  const formattedResult = typeof result === 'number' ? `${(result * 100).toFixed(2)}%` : result;

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
            max={maxLayers} // max layers set to 20
          />
        </div>
        {layerConfigs.map((config, layerIndex) => (
          <div key={layerIndex} className="border-t pt-4 mt-4">
            <div>
              <label className="block mb-1 text-secondary">Nodes in Layer {layerIndex + 1}</label>
              <input 
                type="number" 
                value={config.nodes} 
                onChange={(e) => handleLayerChange(layerIndex, 'nodes', Math.min(Number(e.target.value), maxNodes))} 
                className="border rounded p-2 w-full text-center" 
                min="1"
                max={maxNodes} // max nodes set to 50
              />
            </div>
            <div>
              <label className="block mb-1 text-secondary">Activation Function {layerIndex + 1}</label>
              <select 
                value={config.actFunction} 
                onChange={(e) => handleLayerChange(layerIndex, 'actFunction', e.target.value)} 
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
      {result !== undefined && (
        <div className="mt-4 p-4 border-t w-full text-left">
          <p className="text-xl font-semibold">Accuracy: {formattedResult}</p>
        </div>
      )}
    </div>
  );
});

export default HeroCard;
