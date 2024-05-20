import HeroCard from './components/HeroCard';
import Accuracy from './components/Accuracy';

const heroItems = [
  {
    title: 'Neural Network 1',
    layers: '4',
    nodes: '10',
    actfunction: 'sigmoid',
  },
  {
    title: 'Neural Network 2',
    layers: '6',
    nodes: '20',
    actfunction: 'sigmoid',
  },
  {
    title: 'Neural Network 3',
    layers: '1',
    nodes: '5',
    actfunction: 'sigmoid',
  },
];

const accuracy = [
  'Accuracy: 60%',
  'Accuracy: 73%',
  'Accuracy: 96%',
];

function App() {
  return (
    <>
      <p className="text-5xl w-full font-bold mt-10 mb-10 flex justify-center text-primary font-poppins">
        NeuralCheck
      </p>
      <div className="w-full flex justify-center gap-4 mb-8">
        {heroItems.map((item) => (
          <HeroCard
            key={item.title}
            title={item.title}
            layers={item.layers}
            nodes={item.nodes}
            actfunction={item.actfunction}
          />
        ))}
      </div>
      <div className="flex justify-center mb-8">
        <button className="rounded-lg border-4 shadow-lg bg-transparent font-medium text-3xl px-6 py-2 hover:bg-secondary hover:text-primary transition-colors">
          Start Training!
        </button>
      </div>
      <div className="w-full flex justify-center gap-4">
        {accuracy.map((acc, index) => (
          <Accuracy key={index} accuracy={acc} />
        ))}
      </div>
    </>
  );
}

export default App;
