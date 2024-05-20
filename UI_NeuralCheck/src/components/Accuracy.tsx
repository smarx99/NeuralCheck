import React from 'react';

interface AccuracyProps {
  accuracy: string;
}

const Accuracy: React.FC<AccuracyProps> = ({ accuracy }) => {
  return (
    <div className="bg-white border-4 shadow-lg border-gray-200 shadow-lg rounded-lg p-4 w-32 h-16 flex justify-center items-center text-center">
      <div className="font-bold text-xl text-primary">{accuracy}</div>
    </div>
  );
}

export default Accuracy;
